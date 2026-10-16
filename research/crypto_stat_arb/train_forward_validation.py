"""Train/forward validation workflow for cluster-PCA crypto stat-arb.

This module is deliberately small and conservative. It optimizes only two
parameters on the train set:

1. PCA rolling window length.
2. Entry s-score threshold.

All other settings are fixed research assumptions. This follows the practical
Chan-style rule that every extra optimized parameter increases data-snooping
risk.
"""

from __future__ import annotations

import argparse
import html
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl

from research.crypto_stat_arb.binance_ohlc import load_ohlc_dir
from research.crypto_stat_arb.pca_residual_backtest import (
    BacktestResult,
    ClusterPcaBacktestConfig,
    backtest_cluster_pca_stat_arb,
    resample_ohlc_frame,
)


@dataclass(frozen=True)
class ParameterGrid:
    pca_window_days: tuple[int, ...] = (90, 180, 270)
    entry_scores: tuple[float, ...] = (1.25, 1.5, 1.75, 2.0)

    @property
    def optimized_parameter_count(self) -> int:
        return 2

    @property
    def search_count(self) -> int:
        return len(self.pca_window_days) * len(self.entry_scores)


@dataclass(frozen=True)
class TrainForwardConfig:
    train_ratio: float = 0.80
    bar_hours: int = 4
    n_factors: int = 1
    ar_window_days: int = 60
    rebalance_hours: int = 24
    exit_score: float = 0.35
    stop_score: float = 4.0
    max_positions: int = 20
    target_gross: float = 1.0
    fee_bps: float = 6.0
    max_turnover_per_rebalance: float = 0.05
    target_annual_volatility: float | None = 0.20
    cluster_count: int = 10
    min_cluster_assets: int = 6
    min_half_life_bars: float = 4.0
    max_half_life_bars: float | None = None
    use_half_life_filter: bool = True
    min_average_gross_exposure: float = 0.05

    @property
    def periods_per_year(self) -> float:
        return 365.0 * 24.0 / self.bar_hours


def _bars_from_days(days: int, bar_hours: int) -> int:
    return max(1, int(round(days * 24 / bar_hours)))


def _bars_from_hours(hours: int, bar_hours: int) -> int:
    return max(1, int(round(hours / bar_hours)))


def _split_timestamp_by_ratio(frame: pl.DataFrame, train_ratio: float) -> tuple[Any, int, list[Any]]:
    if not 0.0 < train_ratio < 1.0:
        raise ValueError("train_ratio must be between 0 and 1")
    timestamps = frame.select("timestamp").unique().sort("timestamp").get_column("timestamp").to_list()
    if len(timestamps) < 3:
        raise ValueError("Need at least three timestamps to split train/forward")
    split_index = int(len(timestamps) * train_ratio)
    split_index = min(max(split_index, 1), len(timestamps) - 1)
    return timestamps[split_index], split_index, timestamps


def _make_cluster_config(
    validation_config: TrainForwardConfig,
    *,
    pca_window_days: int,
    entry_score: float,
) -> ClusterPcaBacktestConfig:
    return ClusterPcaBacktestConfig(
        n_factors=validation_config.n_factors,
        pca_window=_bars_from_days(pca_window_days, validation_config.bar_hours),
        ar_window=_bars_from_days(validation_config.ar_window_days, validation_config.bar_hours),
        rebalance_hours=_bars_from_hours(
            validation_config.rebalance_hours,
            validation_config.bar_hours,
        ),
        entry_score=entry_score,
        exit_score=validation_config.exit_score,
        stop_score=validation_config.stop_score,
        max_positions=validation_config.max_positions,
        target_gross=validation_config.target_gross,
        fee_bps=validation_config.fee_bps,
        bar_hours=float(validation_config.bar_hours),
        min_half_life_bars=validation_config.min_half_life_bars,
        max_half_life_bars=validation_config.max_half_life_bars,
        use_half_life_filter=validation_config.use_half_life_filter,
        max_turnover_per_rebalance=validation_config.max_turnover_per_rebalance,
        target_annual_volatility=validation_config.target_annual_volatility,
        factor_neutralize=True,
        cluster_count=validation_config.cluster_count,
        min_cluster_assets=validation_config.min_cluster_assets,
    )


def _curve_metrics(
    equity_curve: pl.DataFrame,
    *,
    periods_per_year: float,
) -> dict[str, float | int | str]:
    if equity_curve.is_empty():
        return {"rows": 0}
    returns = equity_curve.get_column("net_return").to_numpy()
    cumulative = np.cumprod(1.0 + returns)
    total_return = float(cumulative[-1] - 1.0)
    years = len(returns) / periods_per_year
    annualized_return = (
        float(cumulative[-1] ** (1.0 / years) - 1.0)
        if years > 0 and cumulative[-1] > 0
        else float("nan")
    )
    volatility = float(np.std(returns, ddof=1)) if len(returns) > 1 else 0.0
    annualized_volatility = volatility * math.sqrt(periods_per_year)
    sharpe = (
        float(np.mean(returns) / volatility * math.sqrt(periods_per_year))
        if volatility > 1e-12
        else float("nan")
    )
    drawdown = cumulative / np.maximum.accumulate(cumulative) - 1.0
    return {
        "start": str(equity_curve.get_column("timestamp")[0]),
        "end": str(equity_curve.get_column("timestamp")[-1]),
        "rows": equity_curve.height,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe": sharpe,
        "max_drawdown": float(drawdown.min()),
        "annualized_turnover": float(equity_curve.get_column("turnover").mean() * periods_per_year),
        "transaction_cost_usdt": float(equity_curve.get_column("transaction_cost_usdt").sum()),
        "average_gross_exposure": float(equity_curve.get_column("gross_exposure").mean()),
        "average_active_positions": float(equity_curve.get_column("active_positions").mean()),
    }


def _selection_score(metrics: dict[str, float | int | str], config: TrainForwardConfig) -> float:
    if not metrics or int(metrics.get("rows", 0)) == 0:
        return float("-inf")
    sharpe = float(metrics.get("sharpe", float("nan")))
    avg_gross = float(metrics.get("average_gross_exposure", 0.0))
    if not math.isfinite(sharpe):
        return float("-inf")
    if avg_gross < config.min_average_gross_exposure:
        return float("-inf")
    return sharpe


def _run_grid_search(
    train_frame: pl.DataFrame,
    *,
    validation_config: TrainForwardConfig,
    grid: ParameterGrid,
) -> tuple[dict[str, Any], BacktestResult, pl.DataFrame]:
    results: list[dict[str, Any]] = []
    best_record: dict[str, Any] | None = None
    best_result: BacktestResult | None = None
    best_score = float("-inf")

    for pca_window_days, entry_score in product(grid.pca_window_days, grid.entry_scores):
        model_config = _make_cluster_config(
            validation_config,
            pca_window_days=pca_window_days,
            entry_score=entry_score,
        )
        try:
            result = backtest_cluster_pca_stat_arb(train_frame, model_config)
            metrics = _curve_metrics(
                result.equity_curve,
                periods_per_year=validation_config.periods_per_year,
            )
            error = ""
        except Exception as exc:  # pragma: no cover - defensive research report path
            result = None
            metrics = {"rows": 0}
            error = f"{type(exc).__name__}: {exc}"

        score = _selection_score(metrics, validation_config)
        record = {
            "pca_window_days": pca_window_days,
            "entry_score": entry_score,
            "selection_score": score,
            "error": error,
            **{f"train_{key}": value for key, value in metrics.items()},
        }
        results.append(record)
        if result is not None and score > best_score:
            best_score = score
            best_record = record
            best_result = result

    if best_record is None or best_result is None:
        raise RuntimeError("No valid train parameter set found")
    return best_record, best_result, pl.DataFrame(results)


def _forward_frame_with_warmup(
    frame: pl.DataFrame,
    *,
    timestamps: list[Any],
    split_index: int,
    pca_window_bars: int,
) -> pl.DataFrame:
    start_index = max(0, split_index - pca_window_bars - 1)
    start_timestamp = timestamps[start_index]
    return frame.filter(pl.col("timestamp") >= start_timestamp)


def _timestamp_for_frame(frame: pl.DataFrame, timestamp: Any) -> Any:
    """Coerce timezone-aware split timestamps for timezone-naive result frames."""
    dtype = frame.schema.get("timestamp")
    if isinstance(timestamp, datetime) and timestamp.tzinfo is not None and "UTC" not in str(dtype):
        return timestamp.replace(tzinfo=None)
    return timestamp


def _write_split_plot(
    train_curve: pl.DataFrame,
    forward_curve: pl.DataFrame,
    *,
    output_path: Path,
    title: str,
    train_metrics: dict[str, Any],
    forward_metrics: dict[str, Any],
) -> None:
    width, height = 1180, 640
    left, right, top, bottom = 88, 36, 70, 95
    plot_width = width - left - right
    plot_height = height - top - bottom

    def rebased(frame: pl.DataFrame) -> tuple[list[float], list[float]]:
        timestamps = frame.get_column("timestamp").to_list()
        returns = frame.get_column("net_return").to_list()
        value = 1.0
        cumulative = []
        for item in returns:
            value *= 1.0 + item
            cumulative.append(value - 1.0)
        elapsed = [(timestamp - timestamps[0]).total_seconds() / 86400.0 for timestamp in timestamps]
        return elapsed, cumulative

    train_x, train_y = rebased(train_curve)
    forward_x, forward_y = rebased(forward_curve)
    xmax = max(max(train_x), max(forward_x))
    ymin = min(min(train_y), min(forward_y), 0.0)
    ymax = max(max(train_y), max(forward_y), 0.0)
    pad = (ymax - ymin) * 0.08 or 0.01
    ymin -= pad
    ymax += pad

    def sx(value: float) -> float:
        return left + value / xmax * plot_width

    def sy(value: float) -> float:
        return top + plot_height - (value - ymin) / (ymax - ymin) * plot_height

    def points(xs: list[float], ys: list[float]) -> str:
        return " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in zip(xs, ys, strict=True))

    yticks = [ymin + index * (ymax - ymin) / 5 for index in range(6)]
    xticks = [0, 180, 360, 540, 720, 900]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933}.title{font-size:22px;font-weight:700}.sub{font-size:13px;fill:#52606d}.axis{stroke:#9aa5b1;stroke-width:1}.grid{stroke:#e4e7eb;stroke-width:1}.zero{stroke:#d64545;stroke-width:1.1;stroke-dasharray:5 5}.train{fill:none;stroke:#0f766e;stroke-width:2.4}.forward{fill:none;stroke:#c2410c;stroke-width:2.4}</style>',
        f'<text x="{left}" y="32" class="title">{html.escape(title)}</text>',
        '<text x="88" y="54" class="sub">Both curves are rebased to zero at the start of their own segment.</text>',
    ]
    for y in yticks:
        yy = sy(y)
        svg.append(f'<line x1="{left}" y1="{yy:.2f}" x2="{width - right}" y2="{yy:.2f}" class="grid"/>')
        svg.append(
            f'<text x="{left - 10}" y="{yy + 4:.2f}" text-anchor="end" font-size="12">{y:.0%}</text>'
        )
    for x in xticks:
        if x <= xmax:
            xx = sx(x)
            svg.append(f'<line x1="{xx:.2f}" y1="{top}" x2="{xx:.2f}" y2="{top + plot_height}" class="grid"/>')
            svg.append(
                f'<text x="{xx:.2f}" y="{top + plot_height + 22}" text-anchor="middle" font-size="12">{x}d</text>'
            )
    svg.extend(
        [
            f'<line x1="{left}" y1="{sy(0):.2f}" x2="{width - right}" y2="{sy(0):.2f}" class="zero"/>',
            f'<polyline points="{points(train_x, train_y)}" class="train"/>',
            f'<polyline points="{points(forward_x, forward_y)}" class="forward"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" class="axis"/>',
            f'<line x1="{left}" y1="{top + plot_height}" x2="{width - right}" y2="{top + plot_height}" class="axis"/>',
        ]
    )
    legend_y = height - 45
    svg.append(
        f'<line x1="88" y1="{legend_y}" x2="124" y2="{legend_y}" class="train"/>'
        f'<text x="132" y="{legend_y + 4}" font-size="13">Train best: '
        f'{float(train_metrics["total_return"]):.1%}, Sharpe {float(train_metrics["sharpe"]):.2f}</text>'
    )
    svg.append(
        f'<line x1="430" y1="{legend_y}" x2="466" y2="{legend_y}" class="forward"/>'
        f'<text x="474" y="{legend_y + 4}" font-size="13">Forward frozen params: '
        f'{float(forward_metrics["total_return"]):.1%}, Sharpe {float(forward_metrics["sharpe"]):.2f}</text>'
    )
    svg.append("</svg>")
    output_path.write_text("\n".join(svg), encoding="utf-8")


def run_train_forward_validation(
    frame: pl.DataFrame,
    *,
    validation_config: TrainForwardConfig,
    grid: ParameterGrid,
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    split_timestamp, split_index, timestamps = _split_timestamp_by_ratio(
        frame,
        validation_config.train_ratio,
    )
    train_frame = frame.filter(pl.col("timestamp") < split_timestamp)
    best_record, train_result, grid_results = _run_grid_search(
        train_frame,
        validation_config=validation_config,
        grid=grid,
    )

    best_pca_days = int(best_record["pca_window_days"])
    best_entry_score = float(best_record["entry_score"])
    best_model_config = _make_cluster_config(
        validation_config,
        pca_window_days=best_pca_days,
        entry_score=best_entry_score,
    )
    forward_frame = _forward_frame_with_warmup(
        frame,
        timestamps=timestamps,
        split_index=split_index,
        pca_window_bars=best_model_config.pca_window,
    )
    forward_result = backtest_cluster_pca_stat_arb(forward_frame, best_model_config)
    forward_split_timestamp = _timestamp_for_frame(forward_result.equity_curve, split_timestamp)
    forward_curve = forward_result.equity_curve.filter(pl.col("timestamp") >= forward_split_timestamp)
    forward_metrics = _curve_metrics(
        forward_curve,
        periods_per_year=validation_config.periods_per_year,
    )
    train_metrics = _curve_metrics(
        train_result.equity_curve,
        periods_per_year=validation_config.periods_per_year,
    )

    grid_results.write_parquet(output_dir / "train_grid_results.parquet")
    train_result.equity_curve.write_parquet(output_dir / "train_best_equity_curve.parquet")
    train_result.weights.write_parquet(output_dir / "train_best_weights.parquet")
    forward_curve.write_parquet(output_dir / "forward_equity_curve.parquet")
    weights_split_timestamp = _timestamp_for_frame(forward_result.weights, split_timestamp)
    forward_result.weights.filter(pl.col("timestamp") >= weights_split_timestamp).write_parquet(
        output_dir / "forward_weights.parquet"
    )

    report = {
        "validation_config": asdict(validation_config),
        "parameter_grid": asdict(grid),
        "parameter_budget": {
            "optimized_parameter_count": grid.optimized_parameter_count,
            "optimized_parameters": ["pca_window_days", "entry_score"],
            "chan_style_rule": (
                "Fewer parameters is better; this workflow optimizes only two knobs "
                "and treats all other settings as fixed research assumptions."
            ),
            "search_count": grid.search_count,
        },
        "split": {
            "train_ratio": validation_config.train_ratio,
            "split_timestamp": str(split_timestamp),
            "train_rows": train_frame.height,
            "forward_rows_with_warmup": forward_frame.height,
        },
        "selected_parameters": {
            "pca_window_days": best_pca_days,
            "entry_score": best_entry_score,
            "pca_window_bars": best_model_config.pca_window,
            "ar_window_bars": best_model_config.ar_window,
        },
        "train_metrics": train_metrics,
        "forward_metrics": forward_metrics,
        "notes": [
            "Forward run starts flat after a warmup prefix so rolling PCA uses past data only.",
            "This is a single 80/20 chronological validation, not a full walk-forward study.",
            "Universe is current Binance TRADING USDT perps, so survivorship bias remains.",
        ],
    }
    (output_dir / "train_forward_report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    _write_split_plot(
        train_result.equity_curve,
        forward_curve,
        output_path=output_dir / "train_forward_return_curves.svg",
        title="Cluster-PCA train vs forward return curves",
        train_metrics=train_metrics,
        forward_metrics=forward_metrics,
    )
    return report


def _parse_int_grid(raw: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in raw.split(",") if item.strip())


def _parse_float_grid(raw: str) -> tuple[float, ...]:
    return tuple(float(item.strip()) for item in raw.split(",") if item.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Run 80/20 train-forward validation for cluster-PCA.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/binance_um_1h_onboard_20230101_all"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/reports/cluster_pca_train_forward_80_20"))
    parser.add_argument("--train-ratio", type=float, default=TrainForwardConfig.train_ratio)
    parser.add_argument("--bar-hours", type=int, default=TrainForwardConfig.bar_hours)
    parser.add_argument("--pca-window-days-grid", default="90,180,270")
    parser.add_argument("--entry-score-grid", default="1.25,1.5,1.75,2.0")
    parser.add_argument("--cluster-count", type=int, default=TrainForwardConfig.cluster_count)
    parser.add_argument("--min-cluster-assets", type=int, default=TrainForwardConfig.min_cluster_assets)
    parser.add_argument("--max-turnover-per-rebalance", type=float, default=TrainForwardConfig.max_turnover_per_rebalance)
    parser.add_argument("--max-positions", type=int, default=TrainForwardConfig.max_positions)
    parser.add_argument("--fee-bps", type=float, default=TrainForwardConfig.fee_bps)
    args = parser.parse_args()

    validation_config = TrainForwardConfig(
        train_ratio=args.train_ratio,
        bar_hours=args.bar_hours,
        cluster_count=args.cluster_count,
        min_cluster_assets=args.min_cluster_assets,
        max_turnover_per_rebalance=args.max_turnover_per_rebalance,
        max_positions=args.max_positions,
        fee_bps=args.fee_bps,
    )
    grid = ParameterGrid(
        pca_window_days=_parse_int_grid(args.pca_window_days_grid),
        entry_scores=_parse_float_grid(args.entry_score_grid),
    )
    frame = resample_ohlc_frame(load_ohlc_dir(args.data_dir), bar_hours=args.bar_hours)
    report = run_train_forward_validation(
        frame,
        validation_config=validation_config,
        grid=grid,
        output_dir=args.output_dir,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
