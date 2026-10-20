"""Event-driven, cost-aware PCA residual stat-arb backtest with funding PnL.

This module is a redesign of the calendar-rebalance PCA residual strategy.
Key differences from ``pca_residual_backtest``:

1. Event-driven trading: signals are evaluated every bar, but a position is
   opened only when the expected remaining reversion exceeds a multiple of the
   round-trip fee. There is no calendar rebalance, so trading frequency is an
   output of the cost model rather than an input parameter.
2. Per-asset no-trade band: optional weight adjustments smaller than the band
   are skipped instead of proportionally scaling every trade.
3. Weight drift: between trades, held weights drift with realized returns so
   the backtest does not assume free continuous rebalancing.
4. Maker/taker fee split: entries are assumed limit-friendly (maker), exits
   and stops cross the spread (taker).
5. Funding PnL: each funding event is assigned to the holding interval that
   contains it and settles against the position held over that interval.
6. Adaptive factor count: the number of PCA factors is chosen each refit by
   the Marchenko-Pastur eigenvalue edge instead of a fixed count.
7. BTC as the tradable market hedge: instead of projecting weights into a
   PCA-loading nullspace, residual market beta is hedged with an explicit
   BTC leg. BTC itself is excluded from the residual basket.
8. Causal universe: eligibility per refit uses only trailing data (finite
   window returns plus a trailing quote-volume liquidity rank), instead of
   filtering columns on full-sample information.
9. Hard position cap: at most ``max_positions`` residual names (plus the BTC
   hedge leg) can be held at any time.

Timing convention (matches the rest of the repo): the signal at close ``t``
uses returns observed through ``t - signal_lag_bars``; trades execute at close
``t`` and earn the close-to-close return ``t -> t+1``. Fees are charged at the
execution bar.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl
from scipy import linalg

from research.crypto_stat_arb.binance_funding import load_funding_dir
from research.crypto_stat_arb.binance_ohlc import load_ohlc_dir
from research.crypto_stat_arb.pca_residual_backtest import resample_ohlc_frame


@dataclass(frozen=True)
class EventDrivenConfig:
    pca_window: int = 24 * 180
    ar_window: int = 24 * 60
    pca_refit_bars: int = 24
    signal_lag_bars: int = 0
    max_factors: int = 10
    entry_score: float = 2.0
    exit_score: float = 0.5
    stop_score: float = 4.0
    cost_multiple: float = 2.0
    no_trade_band: float = 0.005
    max_positions: int = 20
    target_gross: float = 1.0
    max_weight_per_asset: float = 0.10
    maker_fee_bps: float = 2.0
    taker_fee_bps: float = 5.0
    initial_equity_usdt: float = 100_000.0
    bar_hours: float = 1.0
    min_half_life_bars: float = 4.0
    max_half_life_bars: float | None = None
    universe_size: int = 60
    liquidity_window_bars: int = 24 * 30
    btc_symbol: str = "BTCUSDT"
    hedge_with_btc: bool = True
    target_annual_volatility: float | None = 0.20
    include_funding: bool = True
    min_assets: int = 8

    @property
    def maker_fee_rate(self) -> float:
        return self.maker_fee_bps / 10_000.0

    @property
    def taker_fee_rate(self) -> float:
        return self.taker_fee_bps / 10_000.0

    @property
    def round_trip_fee_rate(self) -> float:
        return self.maker_fee_rate + self.taker_fee_rate

    @property
    def periods_per_year(self) -> float:
        return 365.0 * 24.0 / self.bar_hours

    @property
    def effective_max_half_life_bars(self) -> float:
        pca_half_window = self.pca_window * 0.5
        if self.max_half_life_bars is None:
            return pca_half_window
        return min(self.max_half_life_bars, pca_half_window)


def _validate_config(config: EventDrivenConfig) -> None:
    if config.pca_window <= config.ar_window + 1:
        raise ValueError("pca_window must be larger than ar_window + 1")
    if config.ar_window < 5:
        raise ValueError("ar_window must be >= 5")
    if config.pca_refit_bars < 1:
        raise ValueError("pca_refit_bars must be >= 1")
    if config.signal_lag_bars < 0:
        raise ValueError("signal_lag_bars cannot be negative")
    if config.max_factors < 1:
        raise ValueError("max_factors must be >= 1")
    if config.exit_score < 0 or config.exit_score >= config.entry_score:
        raise ValueError("exit_score must satisfy 0 <= exit_score < entry_score")
    if config.stop_score <= config.entry_score:
        raise ValueError("stop_score must exceed entry_score")
    if config.cost_multiple < 0:
        raise ValueError("cost_multiple cannot be negative")
    if config.no_trade_band < 0:
        raise ValueError("no_trade_band cannot be negative")
    if config.max_positions < 2:
        raise ValueError("max_positions must be >= 2")
    if config.target_gross <= 0:
        raise ValueError("target_gross must be positive")
    if config.max_weight_per_asset <= 0:
        raise ValueError("max_weight_per_asset must be positive")
    if config.maker_fee_bps < 0 or config.taker_fee_bps < 0:
        raise ValueError("fees cannot be negative")
    if config.bar_hours <= 0:
        raise ValueError("bar_hours must be positive")
    if config.universe_size < config.min_assets:
        raise ValueError("universe_size must be >= min_assets")
    if config.liquidity_window_bars < 1:
        raise ValueError("liquidity_window_bars must be >= 1")
    if config.target_annual_volatility is not None and config.target_annual_volatility <= 0:
        raise ValueError("target_annual_volatility must be positive when set")


@dataclass(frozen=True)
class PanelData:
    """Aligned wide panel without full-sample column filtering.

    Rows with missing symbols keep NaN so universe decisions can stay causal.
    ``times[k]`` is the open time of the bar whose close-to-close return is
    ``simple_returns[k]``; that return accrues over the wall-clock interval
    ``(times[k], times[k] + bar]``.
    """

    times: list[datetime]
    times_ms: np.ndarray
    symbols: list[str]
    simple_returns: np.ndarray
    log_returns: np.ndarray
    quote_volume: np.ndarray
    funding: np.ndarray


def prepare_panel(
    frame: pl.DataFrame,
    *,
    funding_frame: pl.DataFrame | None,
    bar_hours: float,
) -> PanelData:
    required = {"timestamp", "symbol", "close"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    has_quote_volume = "quote_volume" in frame.columns
    value_columns = ["close", "quote_volume"] if has_quote_volume else ["close"]
    wide = (
        frame.select(["timestamp", "symbol", *value_columns])
        .sort(["timestamp", "symbol"])
        .pivot(index="timestamp", on="symbol", values=value_columns, aggregate_function="last")
        .sort("timestamp")
    )
    if has_quote_volume:
        symbols = sorted(
            column.removeprefix("close_")
            for column in wide.columns
            if column.startswith("close_")
        )
        close_columns = [f"close_{symbol}" for symbol in symbols]
        volume_columns = [f"quote_volume_{symbol}" for symbol in symbols]
    else:
        symbols = sorted(column for column in wide.columns if column != "timestamp")
        close_columns = symbols
        volume_columns = []
    if len(symbols) < 2:
        raise ValueError("Need at least two symbols after alignment")

    close = wide.select(close_columns).to_numpy().astype(float)
    close = np.where(close > 0, close, np.nan)
    if volume_columns:
        quote_volume = wide.select(volume_columns).to_numpy().astype(float)
        quote_volume = np.nan_to_num(quote_volume, nan=0.0)
    else:
        quote_volume = np.zeros_like(close)

    with np.errstate(invalid="ignore", divide="ignore"):
        simple_returns = close[1:] / close[:-1] - 1.0
        log_returns = np.diff(np.log(close), axis=0)

    timestamps = wide.get_column("timestamp").to_list()
    times = timestamps[1:]
    times_ms = np.array([int(item.timestamp() * 1000) for item in times], dtype=np.int64)

    funding = np.zeros_like(simple_returns)
    if funding_frame is not None and funding_frame.height > 0:
        bar_ms = int(bar_hours * 60 * 60 * 1000)
        symbol_index = {symbol: idx for idx, symbol in enumerate(symbols)}
        row_index = {int(ms): idx for idx, ms in enumerate(times_ms)}
        events = funding_frame.select(
            pl.col("timestamp").dt.timestamp("ms").alias("funding_ms"),
            "symbol",
            "funding_rate",
        )
        hour_ms = 60 * 60 * 1000
        for funding_ms, symbol, rate in events.iter_rows():
            column = symbol_index.get(symbol)
            if column is None:
                continue
            # Vendor funding timestamps carry millisecond jitter around the
            # nominal settlement hour, so snap to the nearest hour first.
            snapped_ms = int(round(int(funding_ms) / hour_ms)) * hour_ms
            # A funding event at time tau settles on the position held over the
            # return interval (open, open + bar] that contains tau, with the
            # boundary event tau == open + bar assigned to the older holder.
            bucket_open = ((snapped_ms - 1) // bar_ms) * bar_ms
            row = row_index.get(bucket_open)
            if row is None:
                continue
            funding[row, column] += float(rate)

    return PanelData(
        times=times,
        times_ms=times_ms,
        symbols=symbols,
        simple_returns=simple_returns,
        log_returns=log_returns,
        quote_volume=quote_volume[1:],
        funding=funding,
    )


def marchenko_pastur_factor_count(
    eigenvalues: np.ndarray,
    *,
    n_observations: int,
    n_assets: int,
    max_factors: int,
) -> int:
    """Count eigenvalues above the Marchenko-Pastur noise edge.

    For a standardized return matrix the MP upper edge is ``(1 + sqrt(N/T))^2``.
    At least one factor is always kept so the dominant market mode is removed.
    """
    if n_observations < 2:
        return 1
    edge = (1.0 + np.sqrt(n_assets / n_observations)) ** 2
    count = int(np.sum(eigenvalues > edge))
    return int(np.clip(count, 1, max_factors))


def _ar1_stats(cumulative_residuals: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """AR(1) s-scores, OU half-lives, and equilibrium stds from cumulative residuals."""
    x_lag = cumulative_residuals[:-1]
    x_next = cumulative_residuals[1:]
    lag_mean = x_lag.mean(axis=0)
    next_mean = x_next.mean(axis=0)
    lag_centered = x_lag - lag_mean
    next_centered = x_next - next_mean
    lag_var = np.sum(lag_centered * lag_centered, axis=0)
    covariance = np.sum(lag_centered * next_centered, axis=0)

    b = np.full(cumulative_residuals.shape[1], np.nan)
    valid_var = lag_var > 1e-12
    b[valid_var] = covariance[valid_var] / lag_var[valid_var]
    a = next_mean - b * lag_mean
    innovation = x_next - a - b * x_lag
    innovation_var = np.mean(innovation * innovation, axis=0)

    valid_ou = (b > 0.0) & (b < 1.0) & (innovation_var > 1e-12)
    equilibrium_mean = np.full_like(b, np.nan)
    equilibrium_std = np.full_like(b, np.nan)
    half_life = np.full_like(b, np.nan)
    equilibrium_mean[valid_ou] = a[valid_ou] / (1.0 - b[valid_ou])
    equilibrium_std[valid_ou] = np.sqrt(innovation_var[valid_ou] / (1.0 - b[valid_ou] ** 2))
    half_life[valid_ou] = np.log(2.0) / (-np.log(b[valid_ou]))

    current = cumulative_residuals[-1]
    s_score = (current - equilibrium_mean) / equilibrium_std
    return s_score, half_life, equilibrium_std


@dataclass
class ModelState:
    """Cached factor model refit on a trailing window, updated bar by bar."""

    fitted_index: int
    columns: np.ndarray
    mean: np.ndarray
    std: np.ndarray
    loadings: np.ndarray
    n_factors: int
    residual_buffer: np.ndarray
    beta_btc: np.ndarray
    explained_variance: float
    btc_index: int | None
    updated_index: int = field(init=False)

    def __post_init__(self) -> None:
        self.updated_index = self.fitted_index


def fit_model_state(
    panel: PanelData,
    end_index: int,
    config: EventDrivenConfig,
) -> ModelState | None:
    """Fit the PCA residual model on the window ending at ``end_index`` inclusive."""
    window = panel.log_returns[end_index - config.pca_window + 1 : end_index + 1]
    finite = np.isfinite(window).all(axis=0)

    btc_index: int | None = None
    if config.hedge_with_btc and config.btc_symbol in panel.symbols:
        candidate = panel.symbols.index(config.btc_symbol)
        if finite[candidate]:
            btc_index = candidate

    tradeable = finite.copy()
    if btc_index is not None:
        tradeable[btc_index] = False

    liquidity_start = max(0, end_index - config.liquidity_window_bars + 1)
    trailing_volume = panel.quote_volume[liquidity_start : end_index + 1].mean(axis=0)
    candidates = np.flatnonzero(tradeable)
    if len(candidates) < config.min_assets:
        return None
    if len(candidates) > config.universe_size:
        ranked = candidates[np.argsort(trailing_volume[candidates])[::-1]]
        candidates = np.sort(ranked[: config.universe_size])

    columns = candidates
    sub_window = window[:, columns]
    mean = sub_window.mean(axis=0)
    std = sub_window.std(axis=0, ddof=1)
    std = np.where(std > 1e-12, std, np.nan)
    standardized = np.nan_to_num((sub_window - mean) / std, copy=False)

    covariance = standardized.T @ standardized / max(1, standardized.shape[0] - 1)
    eigenvalues, eigenvectors = linalg.eigh(covariance, check_finite=False)
    order = np.argsort(eigenvalues)[::-1]
    n_factors = marchenko_pastur_factor_count(
        eigenvalues[order],
        n_observations=standardized.shape[0],
        n_assets=standardized.shape[1],
        max_factors=config.max_factors,
    )
    loadings = eigenvectors[:, order[:n_factors]]
    residuals = standardized - (standardized @ loadings) @ loadings.T
    total_variance = float(np.maximum(eigenvalues.sum(), 1e-12))
    explained_variance = float(eigenvalues[order[:n_factors]].sum() / total_variance)

    if btc_index is not None:
        btc_returns = window[:, btc_index]
        btc_centered = btc_returns - btc_returns.mean()
        btc_var = float(btc_centered @ btc_centered)
        if btc_var > 1e-16:
            beta_btc = (sub_window - mean).T @ btc_centered / btc_var
        else:
            beta_btc = np.zeros(len(columns))
            btc_index = None
    else:
        beta_btc = np.zeros(len(columns))

    return ModelState(
        fitted_index=end_index,
        columns=columns,
        mean=mean,
        std=std,
        loadings=loadings,
        n_factors=n_factors,
        residual_buffer=residuals[-(config.ar_window + 1) :].copy(),
        beta_btc=beta_btc,
        explained_variance=explained_variance,
        btc_index=btc_index,
    )


def update_model_state(state: ModelState, panel: PanelData, through_index: int) -> None:
    """Append residual rows for bars after the last update, keeping a rolling buffer."""
    for index in range(state.updated_index + 1, through_index + 1):
        row = panel.log_returns[index, state.columns]
        z = np.nan_to_num((row - state.mean) / state.std, copy=False)
        residual = z - (z @ state.loadings) @ state.loadings.T
        state.residual_buffer = np.vstack([state.residual_buffer[1:], residual])
    state.updated_index = max(state.updated_index, through_index)


def compute_signals(state: ModelState) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return s-scores, half-lives, and per-asset expected-edge scale (return units)."""
    cumulative = np.cumsum(state.residual_buffer, axis=0)
    s_score, half_life, equilibrium_std = _ar1_stats(cumulative)
    # equilibrium_std is in standardized cumulative-return units; multiplying by
    # the per-bar return std converts one s-score unit of reversion into a raw
    # log-return move for that asset.
    edge_scale = equilibrium_std * state.std
    return s_score, half_life, edge_scale


def build_event_driven_targets(
    state: ModelState,
    current_weights: np.ndarray,
    panel: PanelData,
    signal_index: int,
    config: EventDrivenConfig,
    counters: dict[str, int],
) -> np.ndarray:
    """Construct full-universe target weights from hold/enter/exit rules."""
    n_full = len(panel.symbols)
    s_scores, half_life, edge_scale = compute_signals(state)

    eligible = np.isfinite(s_scores)
    eligible &= np.isfinite(half_life)
    eligible &= half_life >= config.min_half_life_bars
    eligible &= half_life < config.effective_max_half_life_bars

    in_model = np.zeros(n_full, dtype=bool)
    in_model[state.columns] = True

    held = np.flatnonzero(np.abs(current_weights) > 1e-12)
    if state.btc_index is not None:
        held = held[held != state.btc_index]

    position_in_state = {int(col): pos for pos, col in enumerate(state.columns)}
    keep_long: list[int] = []
    keep_short: list[int] = []
    for asset in held:
        pos = position_in_state.get(int(asset))
        if pos is None or not eligible[pos]:
            continue
        score = s_scores[pos]
        if current_weights[asset] > 0 and -config.stop_score < score < -config.exit_score:
            keep_long.append(asset)
        elif current_weights[asset] < 0 and config.exit_score < score < config.stop_score:
            keep_short.append(asset)

    per_side = max(1, config.max_positions // 2)
    keep_long = sorted(keep_long, key=lambda a: s_scores[position_in_state[a]])[:per_side]
    keep_short = sorted(
        keep_short, key=lambda a: s_scores[position_in_state[a]], reverse=True
    )[:per_side]

    flat = np.abs(current_weights) <= 1e-12
    edge_threshold = config.cost_multiple * config.round_trip_fee_rate
    expected_edge = np.maximum(0.0, np.abs(s_scores) - config.exit_score) * edge_scale

    entry_long: list[int] = []
    entry_short: list[int] = []
    candidate_positions = np.flatnonzero(eligible & (np.abs(s_scores) >= config.entry_score))
    ranked = candidate_positions[np.argsort(expected_edge[candidate_positions])[::-1]]
    for pos in ranked:
        asset = int(state.columns[pos])
        if not flat[asset]:
            continue
        counters["entry_candidates"] += 1
        if expected_edge[pos] < edge_threshold:
            counters["entries_blocked_by_cost"] += 1
            continue
        if s_scores[pos] <= -config.entry_score and len(keep_long) + len(entry_long) < per_side:
            entry_long.append(asset)
        elif s_scores[pos] >= config.entry_score and len(keep_short) + len(entry_short) < per_side:
            entry_short.append(asset)

    long_idx = np.array(keep_long + entry_long, dtype=int)
    short_idx = np.array(keep_short + entry_short, dtype=int)

    targets = np.zeros(n_full)
    if len(long_idx) == 0 and len(short_idx) == 0:
        return targets

    # Inverse-volatility sizing inside each side, sides balanced to equal gross.
    vol_full = np.full(n_full, np.nan)
    vol_full[state.columns] = state.std
    for side_idx, side_sign in ((long_idx, 1.0), (short_idx, -1.0)):
        if len(side_idx) == 0:
            continue
        inverse_vol = 1.0 / np.maximum(vol_full[side_idx], 1e-8)
        side_weights = inverse_vol / inverse_vol.sum() * (config.target_gross / 2.0)
        targets[side_idx] = side_sign * side_weights

    capped = np.clip(targets, -config.max_weight_per_asset, config.max_weight_per_asset)
    gross = float(np.abs(capped).sum())
    if gross > 1e-12:
        targets = capped * min(1.0, config.target_gross / gross)

    if state.btc_index is not None:
        beta_full = np.zeros(n_full)
        beta_full[state.columns] = state.beta_btc
        targets[state.btc_index] = -float(targets @ beta_full)
        targets[state.btc_index] = float(
            np.clip(targets[state.btc_index], -config.target_gross / 2.0, config.target_gross / 2.0)
        )

    if config.target_annual_volatility is not None:
        active = np.flatnonzero(np.abs(targets) > 1e-12)
        if len(active) > 0:
            window = panel.log_returns[
                signal_index - config.pca_window + 1 : signal_index + 1
            ][:, active]
            window = np.nan_to_num(window, copy=False)
            covariance = np.cov(window, rowvar=False)
            variance = float(targets[active] @ np.atleast_2d(covariance) @ targets[active])
            if variance > 1e-16:
                annualized = float(np.sqrt(variance * config.periods_per_year))
                if annualized > config.target_annual_volatility:
                    targets *= config.target_annual_volatility / annualized

    return targets


def apply_no_trade_band(
    current_weights: np.ndarray,
    target_weights: np.ndarray,
    *,
    band: float,
) -> np.ndarray:
    """Skip optional adjustments smaller than the band; exits always execute.

    A target of exactly zero on a held name is a forced exit and bypasses the
    band, so stops and ineligibility flushes are never deferred.
    """
    executed = current_weights.copy()
    delta = target_weights - current_weights
    forced_exit = (np.abs(current_weights) > 1e-12) & (np.abs(target_weights) <= 1e-12)
    trade = forced_exit | (np.abs(delta) > band)
    executed[trade] = target_weights[trade]
    return executed


def trading_fee_rate(
    current_weights: np.ndarray,
    executed_weights: np.ndarray,
    config: EventDrivenConfig,
) -> tuple[float, float]:
    """Return (fee as fraction of equity, turnover) for one trade decision.

    Risk-increasing quantity (same direction as the final position) pays maker;
    risk-reducing quantity (closing or flipping out of the old position) pays
    taker.
    """
    delta = executed_weights - current_weights
    turnover = float(np.abs(delta).sum())
    if turnover <= 1e-15:
        return 0.0, 0.0

    closing = np.zeros_like(delta)
    opening = np.zeros_like(delta)
    same_sign = current_weights * executed_weights > 0
    increases = same_sign & (np.abs(executed_weights) > np.abs(current_weights))
    decreases = same_sign & ~increases
    flips_or_flat = ~same_sign

    opening[increases] = np.abs(delta[increases])
    closing[decreases] = np.abs(delta[decreases])
    closing[flips_or_flat] = np.abs(current_weights[flips_or_flat])
    opening[flips_or_flat] = np.abs(executed_weights[flips_or_flat])

    fee = float(opening.sum()) * config.maker_fee_rate + float(closing.sum()) * config.taker_fee_rate
    return fee, turnover


@dataclass(frozen=True)
class EventDrivenResult:
    equity_curve: pl.DataFrame
    weights: pl.DataFrame
    metrics: dict[str, float]
    symbols: list[str]
    config: EventDrivenConfig


def backtest_event_driven(
    frame: pl.DataFrame,
    *,
    funding_frame: pl.DataFrame | None = None,
    config: EventDrivenConfig | None = None,
) -> EventDrivenResult:
    """Run the event-driven cost-aware residual reversion backtest."""
    config = config or EventDrivenConfig()
    _validate_config(config)
    panel = prepare_panel(frame, funding_frame=funding_frame, bar_hours=config.bar_hours)
    n_bars, n_assets = panel.simple_returns.shape
    if n_assets < config.min_assets:
        raise ValueError(f"Need at least {config.min_assets} symbols; got {n_assets}")
    if n_bars <= config.pca_window + config.signal_lag_bars + 1:
        raise ValueError("Not enough observations for pca_window plus signal lag")
    if config.include_funding and funding_frame is None:
        raise ValueError("include_funding=True requires funding_frame")

    weights = np.zeros(n_assets)
    equity = float(config.initial_equity_usdt)
    counters = {"entry_candidates": 0, "entries_blocked_by_cost": 0, "bars_traded": 0}
    equity_records: list[dict[str, Any]] = []
    weight_records: list[dict[str, Any]] = []

    first_signal = config.pca_window - 1 + config.signal_lag_bars
    state = fit_model_state(panel, first_signal - config.signal_lag_bars, config)
    if state is None:
        raise ValueError("Initial universe too small to fit the factor model")

    for t in range(first_signal, n_bars):
        # 1. PnL of bar t with the position carried into it.
        bar_returns = np.nan_to_num(panel.simple_returns[t], copy=False)
        gross_return = float(weights @ bar_returns)
        funding_return = (
            -float(weights @ panel.funding[t]) if config.include_funding else 0.0
        )

        # 2. Drift held weights with realized returns before the trade decision.
        portfolio_growth = 1.0 + gross_return + funding_return
        if portfolio_growth > 1e-12:
            weights = weights * (1.0 + bar_returns) / portfolio_growth

        # 3. Signal at close t uses data through t - signal_lag_bars.
        signal_index = t - config.signal_lag_bars
        if signal_index - state.fitted_index >= config.pca_refit_bars:
            refreshed = fit_model_state(panel, signal_index, config)
            if refreshed is not None:
                state = refreshed
        update_model_state(state, panel, signal_index)

        targets = build_event_driven_targets(
            state, weights, panel, signal_index, config, counters
        )
        executed = apply_no_trade_band(weights, targets, band=config.no_trade_band)
        fee_return, turnover = trading_fee_rate(weights, executed, config)
        if turnover > 1e-15:
            counters["bars_traded"] += 1
        weights = executed

        net_return = gross_return + funding_return - fee_return
        equity *= 1.0 + net_return

        active = np.flatnonzero(np.abs(weights) > 1e-12)
        equity_records.append(
            {
                "timestamp": panel.times[t],
                "gross_return": gross_return,
                "funding_return": funding_return,
                "fee_return": fee_return,
                "net_return": net_return,
                "equity_usdt": equity,
                "turnover": turnover,
                "transaction_cost_usdt": fee_return * equity / (1.0 + net_return)
                if (1.0 + net_return) > 1e-12
                else 0.0,
                "gross_exposure": float(np.abs(weights).sum()),
                "net_exposure": float(weights.sum()),
                "active_positions": int(len(active)),
                "n_factors": state.n_factors,
                "model_explained_variance": state.explained_variance,
            }
        )
        if turnover > 1e-15:
            for asset in active:
                weight_records.append(
                    {
                        "timestamp": panel.times[t],
                        "symbol": panel.symbols[asset],
                        "weight": float(weights[asset]),
                    }
                )

    equity_curve = pl.DataFrame(equity_records)
    weight_frame = pl.DataFrame(
        weight_records,
        schema={"timestamp": pl.Datetime, "symbol": pl.String, "weight": pl.Float64},
        orient="row",
    )
    metrics = compute_event_driven_metrics(equity_curve, config, counters)
    return EventDrivenResult(
        equity_curve=equity_curve,
        weights=weight_frame,
        metrics=metrics,
        symbols=panel.symbols,
        config=config,
    )


def compute_event_driven_metrics(
    equity_curve: pl.DataFrame,
    config: EventDrivenConfig,
    counters: dict[str, int],
) -> dict[str, float]:
    if equity_curve.is_empty():
        return {"rows": 0.0}

    returns = equity_curve.get_column("net_return").to_numpy()
    gross = equity_curve.get_column("gross_return").to_numpy()
    funding = equity_curve.get_column("funding_return").to_numpy()
    fees = equity_curve.get_column("fee_return").to_numpy()
    equity = equity_curve.get_column("equity_usdt").to_numpy()

    volatility = float(np.std(returns, ddof=1)) if len(returns) > 1 else 0.0
    sharpe = (
        float(np.mean(returns) / volatility * np.sqrt(config.periods_per_year))
        if volatility > 1e-12
        else float("nan")
    )
    gross_volatility = float(np.std(gross, ddof=1)) if len(gross) > 1 else 0.0
    gross_sharpe = (
        float(np.mean(gross) / gross_volatility * np.sqrt(config.periods_per_year))
        if gross_volatility > 1e-12
        else float("nan")
    )
    years = len(returns) / config.periods_per_year
    total_return = float(equity[-1] / config.initial_equity_usdt - 1.0)
    annualized_return = (
        float((equity[-1] / config.initial_equity_usdt) ** (1.0 / years) - 1.0)
        if years > 0 and equity[-1] > 0
        else float("nan")
    )
    running_peak = np.maximum.accumulate(equity)
    drawdown = equity / running_peak - 1.0
    avg_turnover = float(equity_curve.get_column("turnover").mean())

    return {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": volatility * float(np.sqrt(config.periods_per_year)),
        "sharpe": sharpe,
        "gross_sharpe": gross_sharpe,
        "max_drawdown": float(np.min(drawdown)),
        "average_turnover": avg_turnover,
        "annualized_turnover": avg_turnover * config.periods_per_year,
        "cumulative_gross_return": float(np.sum(gross)),
        "cumulative_funding_return": float(np.sum(funding)),
        "cumulative_fee_return": float(np.sum(fees)),
        "total_transaction_cost_usdt": float(
            equity_curve.get_column("transaction_cost_usdt").sum()
        ),
        "average_gross_exposure": float(equity_curve.get_column("gross_exposure").mean()),
        "average_active_positions": float(equity_curve.get_column("active_positions").mean()),
        "average_n_factors": float(equity_curve.get_column("n_factors").mean()),
        "entry_candidates": float(counters["entry_candidates"]),
        "entries_blocked_by_cost": float(counters["entries_blocked_by_cost"]),
        "bars_traded": float(counters["bars_traded"]),
        "bars_total": float(equity_curve.height),
    }


def _write_result(result: EventDrivenResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    result.equity_curve.write_parquet(output_dir / "equity_curve.parquet")
    result.weights.write_parquet(output_dir / "weights.parquet")
    (output_dir / "metrics.json").write_text(
        json.dumps(result.metrics, indent=2), encoding="utf-8"
    )
    (output_dir / "config.json").write_text(
        json.dumps(asdict(result.config), indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the event-driven cost-aware crypto stat-arb backtest."
    )
    parser.add_argument(
        "--data-dir", type=Path, default=Path("data/raw/binance_um_1h_onboard_20230101_all")
    )
    parser.add_argument("--funding-dir", type=Path, default=Path("data/raw/binance_um_funding"))
    parser.add_argument("--no-funding", action="store_true")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/reports/event_driven_backtest")
    )
    parser.add_argument("--bar-hours", type=int, choices=[1, 4, 12, 24], default=1)
    parser.add_argument("--pca-window-days", type=int, default=180)
    parser.add_argument("--ar-window-days", type=int, default=60)
    parser.add_argument("--pca-refit-hours", type=int, default=24)
    parser.add_argument("--signal-lag-bars", type=int, default=EventDrivenConfig.signal_lag_bars)
    parser.add_argument("--max-factors", type=int, default=EventDrivenConfig.max_factors)
    parser.add_argument("--entry-score", type=float, default=EventDrivenConfig.entry_score)
    parser.add_argument("--exit-score", type=float, default=EventDrivenConfig.exit_score)
    parser.add_argument("--stop-score", type=float, default=EventDrivenConfig.stop_score)
    parser.add_argument("--cost-multiple", type=float, default=EventDrivenConfig.cost_multiple)
    parser.add_argument("--no-trade-band", type=float, default=EventDrivenConfig.no_trade_band)
    parser.add_argument("--max-positions", type=int, default=EventDrivenConfig.max_positions)
    parser.add_argument("--target-gross", type=float, default=EventDrivenConfig.target_gross)
    parser.add_argument(
        "--max-weight-per-asset", type=float, default=EventDrivenConfig.max_weight_per_asset
    )
    parser.add_argument("--maker-fee-bps", type=float, default=EventDrivenConfig.maker_fee_bps)
    parser.add_argument("--taker-fee-bps", type=float, default=EventDrivenConfig.taker_fee_bps)
    parser.add_argument("--universe-size", type=int, default=EventDrivenConfig.universe_size)
    parser.add_argument("--no-btc-hedge", action="store_true")
    parser.add_argument(
        "--target-annual-volatility",
        type=float,
        default=EventDrivenConfig.target_annual_volatility,
    )
    parser.add_argument(
        "--min-half-life-bars", type=float, default=EventDrivenConfig.min_half_life_bars
    )
    parser.add_argument("--max-half-life-bars", type=float)
    args = parser.parse_args()

    def bars(hours: float) -> int:
        return max(1, int(round(hours / args.bar_hours)))

    config = EventDrivenConfig(
        pca_window=bars(args.pca_window_days * 24),
        ar_window=bars(args.ar_window_days * 24),
        pca_refit_bars=bars(args.pca_refit_hours),
        signal_lag_bars=args.signal_lag_bars,
        max_factors=args.max_factors,
        entry_score=args.entry_score,
        exit_score=args.exit_score,
        stop_score=args.stop_score,
        cost_multiple=args.cost_multiple,
        no_trade_band=args.no_trade_band,
        max_positions=args.max_positions,
        target_gross=args.target_gross,
        max_weight_per_asset=args.max_weight_per_asset,
        maker_fee_bps=args.maker_fee_bps,
        taker_fee_bps=args.taker_fee_bps,
        bar_hours=float(args.bar_hours),
        min_half_life_bars=args.min_half_life_bars,
        max_half_life_bars=args.max_half_life_bars,
        universe_size=args.universe_size,
        liquidity_window_bars=bars(24 * 30),
        hedge_with_btc=not args.no_btc_hedge,
        target_annual_volatility=args.target_annual_volatility,
        include_funding=not args.no_funding,
    )

    frame = resample_ohlc_frame(load_ohlc_dir(args.data_dir), bar_hours=args.bar_hours)
    funding_frame = None if args.no_funding else load_funding_dir(args.funding_dir)
    result = backtest_event_driven(frame, funding_frame=funding_frame, config=config)
    _write_result(result, args.output_dir)
    print(json.dumps(result.metrics, indent=2))


if __name__ == "__main__":
    main()
