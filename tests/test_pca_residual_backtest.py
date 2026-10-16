from __future__ import annotations

from datetime import UTC, datetime, timedelta

import numpy as np
import polars as pl

from research.crypto_stat_arb.pca_residual_backtest import (
    BacktestConfig,
    ClusterPcaBacktestConfig,
    ReengineeredBacktestConfig,
    WaveletFactorBacktestConfig,
    backtest_cluster_pca_stat_arb,
    backtest_pca_stat_arb,
    backtest_pca_stat_arb_reengineered,
    backtest_wavelet_factor_stat_arb,
    build_hysteresis_target_weights,
    build_target_weights,
    resample_ohlc_frame,
    _correlation_clusters,
    _project_active_factor_neutral,
)


def _synthetic_ohlc(hours: int = 260, assets: int = 10) -> pl.DataFrame:
    rng = np.random.default_rng(7)
    common_factor = rng.normal(0.0, 0.004, size=(hours, 2))
    loadings = rng.normal(0.0, 0.7, size=(assets, 2))
    residual_state = np.zeros((hours, assets))
    residual_noise = rng.normal(0.0, 0.003, size=(hours, assets))
    for idx in range(1, hours):
        residual_state[idx] = 0.85 * residual_state[idx - 1] + residual_noise[idx]
    returns = common_factor @ loadings.T + np.diff(residual_state, axis=0, prepend=0.0)
    close = 100.0 * np.exp(np.cumsum(returns, axis=0))

    start = datetime(2023, 1, 1, tzinfo=UTC)
    rows = []
    for asset_index in range(assets):
        symbol = (
            "BTCUSDT"
            if asset_index == 0
            else "ETHUSDT"
            if asset_index == 1
            else f"COIN{asset_index:02d}USDT"
        )
        previous_close = close[0, asset_index]
        for hour_index in range(hours):
            timestamp = start + timedelta(hours=hour_index)
            close_price = float(close[hour_index, asset_index])
            open_price = float(previous_close)
            high_price = max(open_price, close_price) * 1.001
            low_price = min(open_price, close_price) * 0.999
            rows.append(
                {
                    "timestamp": timestamp,
                    "symbol": symbol,
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "volume": 10_000.0,
                }
            )
            previous_close = close_price
    return pl.DataFrame(rows)


def test_build_target_weights_is_dollar_neutral_and_capped() -> None:
    scores = np.array([-2.2, -1.4, -0.4, 0.0, 1.3, 2.5, 0.2])
    config = BacktestConfig(
        pca_window=80,
        ar_window=30,
        entry_score=1.0,
        max_positions=4,
        target_gross=1.0,
        use_half_life_filter=False,
    )

    weights = build_target_weights(scores, config)

    assert np.count_nonzero(weights) <= 4
    assert np.isclose(weights.sum(), 0.0)
    assert np.isclose(np.abs(weights).sum(), 1.0)
    assert weights[0] > 0.0
    assert weights[5] < 0.0


def test_half_life_filter_rejects_assets_slower_than_half_pca_window() -> None:
    scores = np.array([-3.0, 3.0, -2.5, 2.5])
    config = BacktestConfig(
        pca_window=80,
        ar_window=30,
        entry_score=2.0,
        max_positions=4,
        min_half_life_bars=0.0,
        max_half_life_bars=None,
    )

    slow_weights = build_target_weights(
        scores,
        config,
        half_life_bars=np.array([41.0, 41.0, 41.0, 41.0]),
    )
    fast_weights = build_target_weights(
        scores,
        config,
        half_life_bars=np.array([39.0, 39.0, 39.0, 39.0]),
    )

    assert np.count_nonzero(slow_weights) == 0
    assert np.count_nonzero(fast_weights) == 4


def test_resample_ohlc_frame_to_4h_bars() -> None:
    frame = _synthetic_ohlc(hours=24, assets=2)

    resampled = resample_ohlc_frame(frame, bar_hours=4)

    assert resampled.height == 12
    assert resampled.get_column("symbol").n_unique() == 2
    bars_by_symbol = (
        resampled.group_by("symbol")
        .agg(pl.len().alias("bars"))
        .sort("symbol")
        .get_column("bars")
        .to_list()
    )
    assert bars_by_symbol == [6, 6]


def test_pca_backtest_outputs_metrics_costs_and_position_limits() -> None:
    frame = _synthetic_ohlc()
    config = BacktestConfig(
        n_factors=2,
        pca_window=96,
        ar_window=36,
        rebalance_hours=6,
        entry_score=0.25,
        max_positions=6,
        fee_bps=6.0,
        use_half_life_filter=False,
        min_assets=8,
    )

    result = backtest_pca_stat_arb(frame, config)

    assert result.equity_curve.height > 0
    assert result.metrics["total_transaction_cost_usdt"] >= 0.0
    assert np.isfinite(result.metrics["total_return"])
    assert result.equity_curve.get_column("active_positions").max() <= config.max_positions
    assert np.isclose(result.equity_curve.get_column("net_exposure").abs().max(), 0.0)
    if result.weights.height > 0:
        grouped = result.weights.group_by("timestamp").agg(pl.col("weight").sum().alias("net"))
        assert grouped.get_column("net").abs().max() < 1e-12


def test_hysteresis_weights_keep_positions_and_cap_turnover() -> None:
    scores = np.array([-2.4, -0.8, 0.1, 2.7, 0.7, -2.2])
    current = np.array([0.25, 0.25, 0.0, -0.25, -0.25, 0.0])
    config = ReengineeredBacktestConfig(
        n_factors=1,
        pca_window=80,
        ar_window=30,
        entry_score=2.0,
        exit_score=0.5,
        stop_score=4.0,
        max_positions=4,
        max_turnover_per_rebalance=0.20,
        use_half_life_filter=False,
        target_annual_volatility=None,
        factor_neutralize=False,
    )
    loadings = np.ones((len(scores), 1))
    return_window = np.ones((80, len(scores))) * 0.001

    weights = build_hysteresis_target_weights(
        scores,
        current,
        config,
        loadings=loadings,
        return_window=return_window,
    )

    assert np.abs(weights - current).sum() <= config.max_turnover_per_rebalance + 1e-12
    assert weights[0] > 0.0
    assert weights[3] < 0.0


def test_hysteresis_forces_exit_when_half_life_too_slow() -> None:
    scores = np.array([-3.0, 3.0, -2.5, 2.5])
    current = np.array([0.5, -0.5, 0.0, 0.0])
    config = ReengineeredBacktestConfig(
        n_factors=1,
        pca_window=80,
        ar_window=30,
        entry_score=2.0,
        exit_score=0.5,
        stop_score=4.0,
        max_positions=4,
        max_turnover_per_rebalance=0.01,
        min_half_life_bars=0.0,
        target_annual_volatility=None,
        factor_neutralize=False,
    )
    loadings = np.ones((len(scores), 1))
    return_window = np.ones((80, len(scores))) * 0.001

    weights = build_hysteresis_target_weights(
        scores,
        current,
        config,
        loadings=loadings,
        return_window=return_window,
        half_life_bars=np.array([41.0, 41.0, 20.0, 20.0]),
    )

    assert weights[0] == 0.0
    assert weights[1] == 0.0


def test_hysteresis_does_not_add_entries_while_old_positions_are_pending_exit() -> None:
    scores = np.array([-1.0, -0.9, -0.8, -0.7, 1.0, 0.9, 2.5])
    current = np.array([1 / 6, 1 / 6, 1 / 6, 1 / 6, -1 / 6, -1 / 6, 0.0])
    config = ReengineeredBacktestConfig(
        n_factors=1,
        pca_window=80,
        ar_window=30,
        entry_score=2.0,
        exit_score=0.5,
        stop_score=4.0,
        max_positions=6,
        max_turnover_per_rebalance=0.01,
        use_half_life_filter=False,
        target_annual_volatility=None,
        factor_neutralize=False,
    )
    loadings = np.ones((len(scores), 1))
    return_window = np.ones((80, len(scores))) * 0.001

    weights = build_hysteresis_target_weights(
        scores,
        current,
        config,
        loadings=loadings,
        return_window=return_window,
    )

    assert np.count_nonzero(np.abs(weights) > 1e-12) <= config.max_positions
    assert weights[6] == 0.0


def test_projection_enforces_dollar_and_factor_neutrality() -> None:
    raw = np.array([0.25, 0.25, -0.25, -0.25, 0.0])
    beta = np.array(
        [
            [1.0, 0.2],
            [0.3, 0.8],
            [0.5, -0.1],
            [-0.2, 0.4],
            [0.0, 0.0],
        ]
    )

    projected = _project_active_factor_neutral(raw, beta, target_gross=1.0)

    active = np.flatnonzero(np.abs(projected) > 1e-12)
    assert active.size == 4
    assert np.isclose(projected.sum(), 0.0, atol=1e-10)
    assert np.allclose(beta.T @ projected, np.zeros(beta.shape[1]), atol=1e-10)
    assert np.isclose(np.abs(projected).sum(), 1.0)


def test_correlation_clusters_keep_minimum_cluster_size() -> None:
    frame = _synthetic_ohlc(hours=180, assets=12)
    close_wide = (
        frame.select(["timestamp", "symbol", "close"])
        .pivot(index="timestamp", on="symbol", values="close", aggregate_function="last")
        .sort("timestamp")
    )
    returns = np.diff(np.log(close_wide.drop("timestamp").to_numpy()), axis=0)

    clusters = _correlation_clusters(returns, cluster_count=3, min_cluster_assets=3)

    assert clusters
    assert all(len(cluster) >= 3 for cluster in clusters)


def test_hysteresis_final_weights_are_factor_neutral_after_turnover_step() -> None:
    scores = np.array([-3.0, -2.8, -2.6, 3.0, 2.8, 2.6])
    current = np.zeros(6)
    beta = np.array(
        [
            [1.0, 0.2],
            [0.3, 0.8],
            [0.2, -0.4],
            [0.5, -0.1],
            [-0.2, 0.4],
            [0.7, 0.5],
        ]
    )
    config = ReengineeredBacktestConfig(
        n_factors=2,
        pca_window=80,
        ar_window=30,
        entry_score=2.0,
        exit_score=0.5,
        stop_score=4.0,
        max_positions=6,
        max_turnover_per_rebalance=0.40,
        use_half_life_filter=False,
        target_annual_volatility=None,
        factor_neutralize=True,
    )
    return_window = np.ones((80, len(scores))) * 0.001

    weights = build_hysteresis_target_weights(
        scores,
        current,
        config,
        loadings=beta,
        return_window=return_window,
    )

    assert np.isclose(weights.sum(), 0.0, atol=1e-10)
    assert np.allclose(beta.T @ weights, np.zeros(beta.shape[1]), atol=1e-10)


def test_reengineered_backtest_runs_with_turnover_cap() -> None:
    frame = _synthetic_ohlc()
    config = ReengineeredBacktestConfig(
        n_factors=2,
        pca_window=96,
        ar_window=36,
        rebalance_hours=12,
        entry_score=0.25,
        exit_score=0.1,
        stop_score=5.0,
        max_positions=6,
        fee_bps=6.0,
        max_turnover_per_rebalance=0.15,
        use_half_life_filter=False,
        target_annual_volatility=None,
        factor_neutralize=False,
        min_assets=8,
    )

    result = backtest_pca_stat_arb_reengineered(frame, config)

    assert result.equity_curve.height > 0
    assert np.isfinite(result.metrics["total_return"])
    assert result.equity_curve.get_column("turnover").max() <= config.max_turnover_per_rebalance + 1e-12
    assert result.equity_curve.get_column("active_positions").max() <= config.max_positions


def test_wavelet_factor_backtest_runs_and_excludes_factor_assets() -> None:
    frame = _synthetic_ohlc(hours=320, assets=10)
    config = WaveletFactorBacktestConfig(
        pca_window=120,
        ar_window=50,
        rebalance_hours=12,
        entry_score=0.25,
        exit_score=0.1,
        stop_score=5.0,
        max_positions=6,
        max_turnover_per_rebalance=0.20,
        wavelet_fast_hours=2,
        wavelet_slow_hours=8,
        use_half_life_filter=False,
        target_annual_volatility=None,
        factor_neutralize=False,
        min_assets=8,
    )

    result = backtest_wavelet_factor_stat_arb(frame, config)

    assert result.equity_curve.height > 0
    assert np.isfinite(result.metrics["total_return"])
    assert result.equity_curve.get_column("active_positions").max() <= config.max_positions
    if result.weights.height > 0:
        traded_symbols = set(result.weights.get_column("symbol").to_list())
        assert "BTCUSDT" not in traded_symbols
        assert "ETHUSDT" not in traded_symbols


def test_cluster_pca_backtest_runs_with_position_cap() -> None:
    frame = _synthetic_ohlc(hours=420, assets=16)
    config = ClusterPcaBacktestConfig(
        n_factors=1,
        pca_window=120,
        ar_window=50,
        rebalance_hours=12,
        entry_score=0.25,
        exit_score=0.1,
        stop_score=5.0,
        max_positions=8,
        max_turnover_per_rebalance=0.20,
        use_half_life_filter=False,
        target_annual_volatility=None,
        factor_neutralize=True,
        min_assets=8,
        cluster_count=3,
        min_cluster_assets=4,
    )

    result = backtest_cluster_pca_stat_arb(frame, config)

    assert result.equity_curve.height > 0
    assert np.isfinite(result.metrics["total_return"])
    assert result.equity_curve.get_column("active_positions").max() <= config.max_positions
    if result.weights.height > 0:
        grouped = result.weights.group_by("timestamp").agg(pl.col("weight").sum().alias("net"))
        assert grouped.get_column("net").abs().max() < 1e-10
