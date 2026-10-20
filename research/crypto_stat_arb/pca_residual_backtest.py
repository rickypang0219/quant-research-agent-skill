"""PCA residual AR(1) s-score backtest for crypto statistical arbitrage.

The timing convention is explicit:

1. At close ``t``, the model uses returns observed through ``t``.
2. It forms target weights for the next close-to-close period.
3. PnL for ``t -> t+1`` is earned by the position formed after close ``t``.
4. Commission is charged on target-weight changes, not on returns.

This is a vectorized research falsification module, not a live execution model.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl
from scipy.cluster import hierarchy
from scipy import linalg
from scipy.spatial.distance import squareform

from research.crypto_stat_arb.binance_ohlc import load_ohlc_dir


@dataclass(frozen=True)
class BacktestConfig:
    n_factors: int = 3
    pca_window: int = 24 * 180
    ar_window: int = 24 * 60
    rebalance_hours: int = 4
    entry_score: float = 1.25
    max_positions: int = 20
    target_gross: float = 1.0
    fee_bps: float = 6.0
    initial_equity_usdt: float = 100_000.0
    bar_hours: float = 1.0
    min_half_life_bars: float = 4.0
    max_half_life_bars: float | None = None
    min_assets: int = 8
    use_half_life_filter: bool = True

    @property
    def fee_rate(self) -> float:
        return self.fee_bps / 10_000.0

    @property
    def periods_per_year(self) -> float:
        return 365.0 * 24.0 / self.bar_hours

    @property
    def effective_max_half_life_bars(self) -> float:
        pca_half_window = self.pca_window * 0.5
        if self.max_half_life_bars is None:
            return pca_half_window
        return min(self.max_half_life_bars, pca_half_window)


@dataclass(frozen=True)
class ReengineeredBacktestConfig(BacktestConfig):
    """Lower-turnover PCA residual strategy configuration.

    This variant is intentionally more conservative than the first baseline:
    it uses entry/exit hysteresis, keeps existing positions until they revert or
    stop, caps rebalance turnover, neutralizes active weights to PCA factors when
    feasible, and scales gross exposure to a realized-volatility target.
    """

    rebalance_hours: int = 24
    entry_score: float = 2.0
    exit_score: float = 0.5
    stop_score: float = 4.0
    max_positions: int = 10
    max_turnover_per_rebalance: float = 0.25
    target_annual_volatility: float | None = 0.20
    factor_neutralize: bool = True


@dataclass(frozen=True)
class WaveletFactorBacktestConfig(ReengineeredBacktestConfig):
    """Explicit-factor residual strategy with a causal Haar-style band-pass filter."""

    entry_score: float = 1.5
    exit_score: float = 0.35
    max_positions: int = 10
    wavelet_fast_hours: float = 24.0
    wavelet_slow_hours: float = 168.0
    exclude_factor_symbols: bool = True


@dataclass(frozen=True)
class ClusterPcaBacktestConfig(ReengineeredBacktestConfig):
    """Cluster-local PCA residual strategy configuration."""

    n_factors: int = 1
    entry_score: float = 1.5
    exit_score: float = 0.35
    max_positions: int = 20
    cluster_count: int = 8
    min_cluster_assets: int = 6


@dataclass(frozen=True)
class MatrixData:
    times: list[datetime]
    symbols: list[str]
    simple_returns: np.ndarray
    log_returns: np.ndarray


@dataclass(frozen=True)
class BacktestResult:
    equity_curve: pl.DataFrame
    weights: pl.DataFrame
    metrics: dict[str, float]
    symbols: list[str]
    config: BacktestConfig


def _validate_config(config: BacktestConfig) -> None:
    if config.n_factors < 1:
        raise ValueError("n_factors must be >= 1")
    if config.pca_window <= config.n_factors + 2:
        raise ValueError("pca_window must be larger than n_factors")
    if config.ar_window < 5:
        raise ValueError("ar_window must be >= 5")
    if config.pca_window <= config.ar_window + 1:
        raise ValueError("pca_window must be larger than ar_window + 1")
    if config.rebalance_hours < 1:
        raise ValueError("rebalance_hours must be >= 1")
    if config.max_positions < 2:
        raise ValueError("max_positions must be >= 2")
    if config.target_gross <= 0:
        raise ValueError("target_gross must be positive")
    if config.fee_bps < 0:
        raise ValueError("fee_bps cannot be negative")
    if config.bar_hours <= 0:
        raise ValueError("bar_hours must be positive")
    if config.min_half_life_bars < 0:
        raise ValueError("min_half_life_bars cannot be negative")
    if (
        config.max_half_life_bars is not None
        and config.max_half_life_bars <= config.min_half_life_bars
    ):
        raise ValueError("max_half_life_bars must exceed min_half_life_bars when set")
    if isinstance(config, ReengineeredBacktestConfig):
        if config.exit_score < 0:
            raise ValueError("exit_score cannot be negative")
        if config.exit_score >= config.entry_score:
            raise ValueError("exit_score must be smaller than entry_score")
        if config.stop_score <= config.entry_score:
            raise ValueError("stop_score must be larger than entry_score")
        if config.max_turnover_per_rebalance <= 0:
            raise ValueError("max_turnover_per_rebalance must be positive")
        if config.target_annual_volatility is not None and config.target_annual_volatility <= 0:
            raise ValueError("target_annual_volatility must be positive when set")
    if isinstance(config, WaveletFactorBacktestConfig):
        if config.wavelet_fast_hours <= 0:
            raise ValueError("wavelet_fast_hours must be positive")
        if config.wavelet_slow_hours <= config.wavelet_fast_hours:
            raise ValueError("wavelet_slow_hours must exceed wavelet_fast_hours")
    if isinstance(config, ClusterPcaBacktestConfig):
        if config.cluster_count < 1:
            raise ValueError("cluster_count must be >= 1")
        if config.min_cluster_assets <= config.n_factors + 1:
            raise ValueError("min_cluster_assets must exceed n_factors + 1")


def prepare_return_matrix(frame: pl.DataFrame) -> MatrixData:
    """Pivot OHLC data into aligned close-to-close return matrices."""
    required = {"timestamp", "symbol", "close"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    close_wide = (
        frame.select(["timestamp", "symbol", "close"])
        .drop_nulls()
        .sort(["timestamp", "symbol"])
        .pivot(index="timestamp", on="symbol", values="close", aggregate_function="last")
        .sort("timestamp")
        .drop_nulls()
    )
    symbols = [column for column in close_wide.columns if column != "timestamp"]
    if len(symbols) < 2:
        raise ValueError("Need at least two symbols after alignment")

    close = close_wide.select(symbols).to_numpy().astype(float)
    valid_columns = np.isfinite(close).all(axis=0) & (close > 0).all(axis=0)
    if not valid_columns.all():
        close = close[:, valid_columns]
        symbols = [symbol for symbol, valid in zip(symbols, valid_columns, strict=True) if valid]
    if len(symbols) < 2:
        raise ValueError("Need at least two valid symbols after filtering")

    simple_returns = close[1:] / close[:-1] - 1.0
    log_returns = np.diff(np.log(close), axis=0)
    times = close_wide.get_column("timestamp").to_list()[1:]
    return MatrixData(
        times=times,
        symbols=symbols,
        simple_returns=simple_returns,
        log_returns=log_returns,
    )


def resample_ohlc_frame(frame: pl.DataFrame, *, bar_hours: int) -> pl.DataFrame:
    """Resample 1h OHLC data to coarser wall-clock bars."""
    if bar_hours < 1:
        raise ValueError("bar_hours must be >= 1")
    if bar_hours == 1:
        return frame.sort(["symbol", "timestamp"])

    required = {"timestamp", "symbol", "open", "high", "low", "close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns for resampling: {sorted(missing)}")

    bucket_ms = bar_hours * 60 * 60 * 1000
    aggregations = [
        pl.col("open").first().alias("open"),
        pl.col("high").max().alias("high"),
        pl.col("low").min().alias("low"),
        pl.col("close").last().alias("close"),
        pl.col("volume").sum().alias("volume"),
    ]
    if "quote_volume" in frame.columns:
        aggregations.append(pl.col("quote_volume").sum().alias("quote_volume"))

    return (
        frame.sort(["symbol", "timestamp"])
        .with_columns(
            ((pl.col("timestamp").dt.timestamp("ms") // bucket_ms) * bucket_ms).alias(
                "_bucket_ms"
            )
        )
        .group_by(["_bucket_ms", "symbol"])
        .agg(aggregations)
        .with_columns(
            pl.from_epoch(pl.col("_bucket_ms"), time_unit="ms")
            .dt.replace_time_zone("UTC")
            .alias("timestamp")
        )
        .drop("_bucket_ms")
        .select(["timestamp", "symbol", "open", "high", "low", "close", "volume"])
        .sort(["symbol", "timestamp"])
    )


def _pca_residuals(return_window: np.ndarray, n_factors: int) -> tuple[np.ndarray, float, np.ndarray]:
    """Standardize returns, remove top PCA components, and return residual returns."""
    if return_window.ndim != 2:
        raise ValueError("return_window must be 2D")
    if return_window.shape[1] <= n_factors:
        raise ValueError("n_factors must be smaller than the asset count")

    mean = return_window.mean(axis=0)
    std = return_window.std(axis=0, ddof=1)
    std = np.where(std > 1e-12, std, np.nan)
    standardized = (return_window - mean) / std
    standardized = np.nan_to_num(standardized, copy=False)

    covariance = standardized.T @ standardized / max(1, standardized.shape[0] - 1)
    eigenvalues, eigenvectors = linalg.eigh(covariance, check_finite=False)
    order = np.argsort(eigenvalues)[::-1]
    top = order[:n_factors]
    loadings = eigenvectors[:, top]
    fitted = (standardized @ loadings) @ loadings.T
    residuals = standardized - fitted
    total_variance = float(np.maximum(eigenvalues.sum(), 1e-12))
    explained_variance = float(eigenvalues[top].sum() / total_variance)
    return residuals, explained_variance, loadings


def _ar1_s_scores(cumulative_residuals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Estimate AR(1) s-scores and OU half-lives from cumulative residuals."""
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
    return s_score, half_life


def build_target_weights(
    s_scores: np.ndarray,
    config: BacktestConfig,
    *,
    half_life_bars: np.ndarray | None = None,
) -> np.ndarray:
    """Build equal-dollar long/short weights from the strongest residual s-scores."""
    weights = np.zeros_like(s_scores, dtype=float)
    eligible = np.isfinite(s_scores)
    if config.use_half_life_filter:
        if half_life_bars is None:
            eligible &= False
        else:
            eligible &= np.isfinite(half_life_bars)
            eligible &= half_life_bars >= config.min_half_life_bars
            eligible &= half_life_bars < config.effective_max_half_life_bars

    long_candidates = np.flatnonzero(eligible & (s_scores <= -config.entry_score))
    short_candidates = np.flatnonzero(eligible & (s_scores >= config.entry_score))
    if len(long_candidates) == 0 or len(short_candidates) == 0:
        return weights

    per_side = max(1, config.max_positions // 2)
    long_order = long_candidates[np.argsort(s_scores[long_candidates])]
    short_order = short_candidates[np.argsort(s_scores[short_candidates])[::-1]]
    long_idx = long_order[:per_side]
    short_idx = short_order[:per_side]

    weights[long_idx] = config.target_gross / (2.0 * len(long_idx))
    weights[short_idx] = -config.target_gross / (2.0 * len(short_idx))
    return weights


def _renormalize_gross(weights: np.ndarray, target_gross: float) -> np.ndarray:
    gross = float(np.abs(weights).sum())
    if gross <= 1e-12:
        return np.zeros_like(weights)
    return weights * (target_gross / gross)


def _project_active_factor_neutral(
    weights: np.ndarray,
    beta: np.ndarray,
    *,
    target_gross: float,
    strict: bool = False,
) -> np.ndarray:
    """Project active weights into the dollar/factor-neutral subspace.

    Let ``Beta`` be the active asset exposure matrix with shape ``N x K``.
    The target portfolio must satisfy:

    ``1^T w = 0`` and ``Beta^T w = 0``.

    The input weights encode the desired long/short basket membership. We project
    those weights onto the nullspace of ``[1, Beta]^T`` and then rescale long and
    short sides to ``+target_gross/2`` and ``-target_gross/2`` when feasible.
    """
    active = np.flatnonzero(np.abs(weights) > 1e-12)
    if len(active) <= beta.shape[1] + 1:
        return np.zeros_like(weights) if strict else weights

    active_weights = weights[active]
    constraints = np.column_stack([np.ones(len(active)), beta[active]])
    if np.linalg.matrix_rank(constraints) >= len(active):
        return np.zeros_like(weights) if strict else weights

    correction = constraints @ (np.linalg.pinv(constraints, rcond=1e-10) @ active_weights)
    projected_active = active_weights - correction

    long_active = active_weights > 0
    short_active = active_weights < 0
    if float(projected_active[long_active].sum()) <= 1e-12:
        return np.zeros_like(weights) if strict else weights
    if float(-projected_active[short_active].sum()) <= 1e-12:
        return np.zeros_like(weights) if strict else weights
    gross = float(np.abs(projected_active).sum())
    if gross <= 1e-12:
        return np.zeros_like(weights) if strict else weights
    scaled_active = projected_active * (target_gross / gross)

    projected = np.zeros_like(weights)
    projected[active] = scaled_active
    if strict:
        active_constraints = constraints.T @ scaled_active
        if np.max(np.abs(active_constraints)) > 1e-8:
            return np.zeros_like(weights)
    return projected


def _scale_to_volatility_target(
    weights: np.ndarray,
    return_window: np.ndarray,
    config: ReengineeredBacktestConfig,
) -> np.ndarray:
    if config.target_annual_volatility is None:
        return weights
    if np.abs(weights).sum() <= 1e-12:
        return weights

    covariance = np.cov(return_window, rowvar=False)
    variance = float(weights @ covariance @ weights)
    if variance <= 1e-16:
        return weights
    annualized_volatility = float(np.sqrt(variance * config.periods_per_year))
    if annualized_volatility <= config.target_annual_volatility:
        return weights
    return weights * (config.target_annual_volatility / annualized_volatility)


def _trailing_mean(values: np.ndarray, window: int) -> np.ndarray:
    if window < 1:
        raise ValueError("window must be >= 1")
    if values.ndim != 2:
        raise ValueError("values must be 2D")
    if window == 1:
        return values.copy()
    output = np.full_like(values, np.nan, dtype=float)
    if values.shape[0] < window:
        return output
    cumulative = np.vstack([np.zeros((1, values.shape[1])), np.cumsum(values, axis=0)])
    output[window - 1 :] = (cumulative[window:] - cumulative[:-window]) / window
    return output


def _haar_style_bandpass(values: np.ndarray, *, fast_window: int, slow_window: int) -> np.ndarray:
    """Causal Haar-style band-pass from the difference of two trailing smoothers."""
    if slow_window <= fast_window:
        raise ValueError("slow_window must exceed fast_window")
    return _trailing_mean(values, fast_window) - _trailing_mean(values, slow_window)


def _factor_index(symbols: list[str], symbol: str) -> int | None:
    try:
        return symbols.index(symbol)
    except ValueError:
        return None


def _explicit_factor_residuals(
    return_window: np.ndarray,
    symbols: list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str], float]:
    """Fit BTC/ETH/market factors and return residuals plus factor exposures."""
    btc_index = _factor_index(symbols, "BTCUSDT")
    eth_index = _factor_index(symbols, "ETHUSDT")
    factor_columns: list[np.ndarray] = []
    factor_names: list[str] = []
    factor_asset_mask = np.zeros(len(symbols), dtype=bool)

    if btc_index is not None:
        factor_columns.append(return_window[:, btc_index])
        factor_names.append("BTCUSDT")
        factor_asset_mask[btc_index] = True
    if eth_index is not None:
        factor_columns.append(return_window[:, eth_index])
        factor_names.append("ETHUSDT")
        factor_asset_mask[eth_index] = True

    market_mask = ~factor_asset_mask
    if market_mask.sum() < 2:
        market_mask = np.ones(len(symbols), dtype=bool)
    factor_columns.append(return_window[:, market_mask].mean(axis=1))
    factor_names.append("EW_MARKET")

    factors = np.column_stack(factor_columns)
    if return_window.shape[0] <= factors.shape[1] + 1:
        raise ValueError("Need more observations than explicit factor columns")

    design = np.column_stack([np.ones(return_window.shape[0]), factors])
    coefficients, *_ = np.linalg.lstsq(design, return_window, rcond=1e-10)
    fitted = design @ coefficients
    residuals = return_window - fitted
    exposures = coefficients[1:].T
    total_variance = float(np.var(return_window))
    residual_variance = float(np.var(residuals))
    explained_variance = 1.0 - residual_variance / total_variance if total_variance > 1e-16 else 0.0
    return residuals, exposures, factor_asset_mask, factor_names, explained_variance


def _correlation_clusters(
    return_window: np.ndarray,
    *,
    cluster_count: int,
    min_cluster_assets: int,
) -> list[np.ndarray]:
    """Cluster assets by trailing return correlation."""
    asset_count = return_window.shape[1]
    if asset_count < min_cluster_assets:
        return []
    if cluster_count <= 1 or asset_count <= min_cluster_assets:
        return [np.arange(asset_count)]

    correlation = np.corrcoef(return_window, rowvar=False)
    correlation = np.nan_to_num(correlation, nan=0.0, posinf=0.0, neginf=0.0)
    correlation = np.clip(correlation, -1.0, 1.0)
    np.fill_diagonal(correlation, 1.0)
    distance = np.sqrt(np.maximum(0.0, 0.5 * (1.0 - correlation)))
    condensed = squareform(distance, checks=False)
    linkage = hierarchy.linkage(condensed, method="average")
    labels = hierarchy.fcluster(linkage, t=min(cluster_count, asset_count), criterion="maxclust")
    clusters: list[np.ndarray] = []
    for label in sorted(set(labels)):
        members = np.flatnonzero(labels == label)
        if len(members) >= min_cluster_assets:
            clusters.append(members)
    return clusters


def _cluster_pca_residual_signals(
    return_window: np.ndarray,
    config: ClusterPcaBacktestConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, list[np.ndarray]]:
    """Compute AR(1) s-scores from PCA residuals inside correlation clusters."""
    asset_count = return_window.shape[1]
    s_scores = np.full(asset_count, np.nan)
    half_life = np.full(asset_count, np.nan)
    beta_columns: list[np.ndarray] = []
    explained_variance_weighted = 0.0
    explained_weight = 0
    clusters = _correlation_clusters(
        return_window,
        cluster_count=config.cluster_count,
        min_cluster_assets=config.min_cluster_assets,
    )

    for cluster_members in clusters:
        if len(cluster_members) <= config.n_factors + 1:
            continue
        cluster_window = return_window[:, cluster_members]
        residuals, explained_variance, loadings = _pca_residuals(
            cluster_window,
            config.n_factors,
        )
        cumulative = np.cumsum(residuals, axis=0)
        ar_sample = cumulative[-(config.ar_window + 1) :]
        cluster_scores, cluster_half_life = _ar1_s_scores(ar_sample)
        s_scores[cluster_members] = cluster_scores
        half_life[cluster_members] = cluster_half_life

        for factor_index in range(loadings.shape[1]):
            beta_column = np.zeros(asset_count)
            beta_column[cluster_members] = loadings[:, factor_index]
            beta_columns.append(beta_column)
        explained_variance_weighted += explained_variance * len(cluster_members)
        explained_weight += len(cluster_members)

    if beta_columns:
        beta = np.column_stack(beta_columns)
    else:
        beta = np.zeros((asset_count, 1))
    explained_variance = explained_variance_weighted / explained_weight if explained_weight else np.nan
    return s_scores, half_life, beta, explained_variance, clusters


def build_hysteresis_target_weights(
    s_scores: np.ndarray,
    current_weights: np.ndarray,
    config: ReengineeredBacktestConfig,
    *,
    loadings: np.ndarray,
    return_window: np.ndarray,
    half_life_bars: np.ndarray | None = None,
) -> np.ndarray:
    """Build persistent long/short weights with entry/exit hysteresis."""
    eligible = np.isfinite(s_scores)
    if config.use_half_life_filter:
        if half_life_bars is None:
            eligible &= False
        else:
            eligible &= np.isfinite(half_life_bars)
            eligible &= half_life_bars >= config.min_half_life_bars
            eligible &= half_life_bars < config.effective_max_half_life_bars

    previous_long = np.flatnonzero(current_weights > 1e-12)
    previous_short = np.flatnonzero(current_weights < -1e-12)

    keep_long = [
        idx
        for idx in previous_long
        if eligible[idx] and s_scores[idx] < -config.exit_score and s_scores[idx] > -config.stop_score
    ]
    keep_short = [
        idx
        for idx in previous_short
        if eligible[idx] and s_scores[idx] > config.exit_score and s_scores[idx] < config.stop_score
    ]

    per_side = max(1, config.max_positions // 2)
    keep_long = sorted(keep_long, key=lambda idx: s_scores[idx])[:per_side]
    keep_short = sorted(keep_short, key=lambda idx: s_scores[idx], reverse=True)[:per_side]

    pending_long_exits = max(0, len(previous_long) - len(keep_long))
    pending_short_exits = max(0, len(previous_short) - len(keep_short))
    pending_exits = pending_long_exits + pending_short_exits
    if pending_exits:
        long_slots = 0
        short_slots = 0
    else:
        long_slots = max(0, per_side - len(keep_long))
        short_slots = max(0, per_side - len(keep_short))
    flat = np.abs(current_weights) <= 1e-12
    long_candidates = np.flatnonzero(eligible & flat & (s_scores <= -config.entry_score))
    short_candidates = np.flatnonzero(eligible & flat & (s_scores >= config.entry_score))

    add_long = []
    add_short = []
    if long_slots > 0:
        add_long = list(long_candidates[np.argsort(s_scores[long_candidates])[:long_slots]])
    if short_slots > 0:
        add_short = list(short_candidates[np.argsort(s_scores[short_candidates])[::-1][:short_slots]])

    long_idx = np.array(keep_long + add_long, dtype=int)
    short_idx = np.array(keep_short + add_short, dtype=int)
    raw = np.zeros_like(s_scores, dtype=float)
    if len(long_idx) > 0 and len(short_idx) > 0:
        raw[long_idx] = config.target_gross / (2.0 * len(long_idx))
        raw[short_idx] = -config.target_gross / (2.0 * len(short_idx))

    if config.factor_neutralize:
        raw = _project_active_factor_neutral(raw, loadings, target_gross=config.target_gross)
    raw = _scale_to_volatility_target(raw, return_window, config)

    forced_flat = (np.abs(current_weights) > 1e-12) & ~eligible
    forced_target = current_weights.copy()
    forced_target[forced_flat] = 0.0
    optional_delta = raw - forced_target
    optional_delta[forced_flat] = 0.0
    optional_turnover = float(np.abs(optional_delta).sum())
    if optional_turnover > config.max_turnover_per_rebalance:
        optional_delta *= config.max_turnover_per_rebalance / optional_turnover
    final = forced_target + optional_delta
    if config.factor_neutralize:
        final = _project_active_factor_neutral(
            final,
            loadings,
            target_gross=float(np.abs(final).sum()),
            strict=True,
        )
        final = _scale_to_volatility_target(final, return_window, config)
    return final


def _compute_signal_weights(
    log_returns: np.ndarray,
    signal_index: int,
    config: BacktestConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    window = log_returns[signal_index - config.pca_window + 1 : signal_index + 1]
    residuals, explained_variance, _ = _pca_residuals(window, config.n_factors)
    cumulative = np.cumsum(residuals, axis=0)
    ar_sample = cumulative[-(config.ar_window + 1) :]
    s_scores, half_life = _ar1_s_scores(ar_sample)
    weights = build_target_weights(s_scores, config, half_life_bars=half_life)
    return weights, s_scores, half_life, explained_variance


def _compute_hysteresis_signal_weights(
    log_returns: np.ndarray,
    signal_index: int,
    current_weights: np.ndarray,
    config: ReengineeredBacktestConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    window = log_returns[signal_index - config.pca_window + 1 : signal_index + 1]
    residuals, explained_variance, loadings = _pca_residuals(window, config.n_factors)
    cumulative = np.cumsum(residuals, axis=0)
    ar_sample = cumulative[-(config.ar_window + 1) :]
    s_scores, half_life = _ar1_s_scores(ar_sample)
    weights = build_hysteresis_target_weights(
        s_scores,
        current_weights,
        config,
        loadings=loadings,
        return_window=window,
        half_life_bars=half_life,
    )
    return weights, s_scores, half_life, explained_variance


def _compute_wavelet_factor_signal_weights(
    log_returns: np.ndarray,
    symbols: list[str],
    signal_index: int,
    current_weights: np.ndarray,
    config: WaveletFactorBacktestConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    window = log_returns[signal_index - config.pca_window + 1 : signal_index + 1]
    residuals, exposures, factor_asset_mask, _, explained_variance = _explicit_factor_residuals(
        window,
        symbols,
    )
    residual_price = np.cumsum(residuals, axis=0)
    fast_window = _bars_from_hours(config.wavelet_fast_hours, int(config.bar_hours))
    slow_window = _bars_from_hours(config.wavelet_slow_hours, int(config.bar_hours))
    filtered = _haar_style_bandpass(
        residual_price,
        fast_window=fast_window,
        slow_window=slow_window,
    )
    ar_sample = filtered[-(config.ar_window + 1) :]
    finite_rows = np.isfinite(ar_sample).all(axis=1)
    if finite_rows.sum() < 5:
        s_scores = np.full(log_returns.shape[1], np.nan)
        half_life = np.full(log_returns.shape[1], np.nan)
    else:
        s_scores, half_life = _ar1_s_scores(ar_sample[finite_rows])

    if config.exclude_factor_symbols:
        s_scores = s_scores.copy()
        s_scores[factor_asset_mask] = np.nan

    weights = build_hysteresis_target_weights(
        s_scores,
        current_weights,
        config,
        loadings=exposures,
        return_window=window,
        half_life_bars=half_life,
    )
    return weights, s_scores, half_life, explained_variance


def _compute_cluster_pca_signal_weights(
    log_returns: np.ndarray,
    signal_index: int,
    current_weights: np.ndarray,
    config: ClusterPcaBacktestConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    window = log_returns[signal_index - config.pca_window + 1 : signal_index + 1]
    s_scores, half_life, beta, explained_variance, _ = _cluster_pca_residual_signals(
        window,
        config,
    )
    weights = build_hysteresis_target_weights(
        s_scores,
        current_weights,
        config,
        loadings=beta,
        return_window=window,
        half_life_bars=half_life,
    )
    return weights, s_scores, half_life, explained_variance


def backtest_pca_stat_arb(frame: pl.DataFrame, config: BacktestConfig | None = None) -> BacktestResult:
    """Run the close-to-close PCA residual s-score backtest."""
    config = config or BacktestConfig()
    _validate_config(config)
    matrix = prepare_return_matrix(frame)
    if len(matrix.symbols) < max(config.min_assets, config.n_factors + 1):
        raise ValueError(
            f"Need at least {max(config.min_assets, config.n_factors + 1)} aligned assets; "
            f"got {len(matrix.symbols)}"
        )
    if matrix.log_returns.shape[0] <= config.pca_window + 1:
        raise ValueError("Not enough observations for pca_window and one forward return")

    current_weights = np.zeros(len(matrix.symbols), dtype=float)
    equity = float(config.initial_equity_usdt)
    equity_records: list[dict[str, Any]] = []
    weight_records: list[dict[str, Any]] = []

    first_signal_index = config.pca_window - 1
    first_trade_index = first_signal_index + 1
    for trade_index in range(first_trade_index, matrix.simple_returns.shape[0]):
        signal_index = trade_index - 1
        turnover = 0.0
        cost_usdt = 0.0
        explained_variance = np.nan
        active_positions = int(np.count_nonzero(current_weights))

        if (signal_index - first_signal_index) % config.rebalance_hours == 0:
            target_weights, s_scores, half_life, explained_variance = _compute_signal_weights(
                matrix.log_returns,
                signal_index,
                config,
            )
            turnover = float(np.abs(target_weights - current_weights).sum())
            cost_usdt = equity * config.fee_rate * turnover
            current_weights = target_weights
            active_positions = int(np.count_nonzero(current_weights))

            timestamp = matrix.times[trade_index]
            for symbol_index in np.flatnonzero(current_weights):
                weight_records.append(
                    {
                        "timestamp": timestamp,
                        "symbol": matrix.symbols[symbol_index],
                        "weight": float(current_weights[symbol_index]),
                        "s_score": float(s_scores[symbol_index]),
                        "half_life_bars": float(half_life[symbol_index]),
                        "half_life_hours": float(half_life[symbol_index] * config.bar_hours),
                    }
                )

        gross_return = float(current_weights @ matrix.simple_returns[trade_index])
        cost_return = cost_usdt / equity if equity > 0 else 0.0
        net_return = gross_return - cost_return
        equity *= 1.0 + net_return

        equity_records.append(
            {
                "timestamp": matrix.times[trade_index],
                "gross_return": gross_return,
                "cost_return": cost_return,
                "net_return": net_return,
                "equity_usdt": equity,
                "turnover": turnover,
                "transaction_cost_usdt": cost_usdt,
                "gross_exposure": float(np.abs(current_weights).sum()),
                "net_exposure": float(current_weights.sum()),
                "active_positions": active_positions,
                "pca_explained_variance": explained_variance,
            }
        )

    equity_curve = pl.DataFrame(equity_records)
    weights = pl.DataFrame(
        weight_records,
        schema={
            "timestamp": pl.Datetime,
            "symbol": pl.String,
            "weight": pl.Float64,
            "s_score": pl.Float64,
            "half_life_bars": pl.Float64,
            "half_life_hours": pl.Float64,
        },
        orient="row",
    )
    metrics = compute_metrics(equity_curve, config)
    return BacktestResult(
        equity_curve=equity_curve,
        weights=weights,
        metrics=metrics,
        symbols=matrix.symbols,
        config=config,
    )


def backtest_pca_stat_arb_reengineered(
    frame: pl.DataFrame,
    config: ReengineeredBacktestConfig | None = None,
) -> BacktestResult:
    """Run the lower-turnover PCA residual strategy variant."""
    config = config or ReengineeredBacktestConfig()
    _validate_config(config)
    matrix = prepare_return_matrix(frame)
    if len(matrix.symbols) < max(config.min_assets, config.n_factors + 1):
        raise ValueError(
            f"Need at least {max(config.min_assets, config.n_factors + 1)} aligned assets; "
            f"got {len(matrix.symbols)}"
        )
    if matrix.log_returns.shape[0] <= config.pca_window + 1:
        raise ValueError("Not enough observations for pca_window and one forward return")

    current_weights = np.zeros(len(matrix.symbols), dtype=float)
    equity = float(config.initial_equity_usdt)
    equity_records: list[dict[str, Any]] = []
    weight_records: list[dict[str, Any]] = []

    first_signal_index = config.pca_window - 1
    first_trade_index = first_signal_index + 1
    for trade_index in range(first_trade_index, matrix.simple_returns.shape[0]):
        signal_index = trade_index - 1
        turnover = 0.0
        cost_usdt = 0.0
        explained_variance = np.nan
        active_positions = int(np.count_nonzero(np.abs(current_weights) > 1e-12))

        if (signal_index - first_signal_index) % config.rebalance_hours == 0:
            target_weights, s_scores, half_life, explained_variance = (
                _compute_hysteresis_signal_weights(
                    matrix.log_returns,
                    signal_index,
                    current_weights,
                    config,
                )
            )
            turnover = float(np.abs(target_weights - current_weights).sum())
            cost_usdt = equity * config.fee_rate * turnover
            current_weights = target_weights
            active_positions = int(np.count_nonzero(np.abs(current_weights) > 1e-12))

            timestamp = matrix.times[trade_index]
            for symbol_index in np.flatnonzero(np.abs(current_weights) > 1e-12):
                weight_records.append(
                    {
                        "timestamp": timestamp,
                        "symbol": matrix.symbols[symbol_index],
                        "weight": float(current_weights[symbol_index]),
                        "s_score": float(s_scores[symbol_index]),
                        "half_life_bars": float(half_life[symbol_index]),
                        "half_life_hours": float(half_life[symbol_index] * config.bar_hours),
                    }
                )

        gross_return = float(current_weights @ matrix.simple_returns[trade_index])
        cost_return = cost_usdt / equity if equity > 0 else 0.0
        net_return = gross_return - cost_return
        equity *= 1.0 + net_return

        equity_records.append(
            {
                "timestamp": matrix.times[trade_index],
                "gross_return": gross_return,
                "cost_return": cost_return,
                "net_return": net_return,
                "equity_usdt": equity,
                "turnover": turnover,
                "transaction_cost_usdt": cost_usdt,
                "gross_exposure": float(np.abs(current_weights).sum()),
                "net_exposure": float(current_weights.sum()),
                "active_positions": active_positions,
                "pca_explained_variance": explained_variance,
            }
        )

    equity_curve = pl.DataFrame(equity_records)
    weights = pl.DataFrame(
        weight_records,
        schema={
            "timestamp": pl.Datetime,
            "symbol": pl.String,
            "weight": pl.Float64,
            "s_score": pl.Float64,
            "half_life_bars": pl.Float64,
            "half_life_hours": pl.Float64,
        },
        orient="row",
    )
    metrics = compute_metrics(equity_curve, config)
    return BacktestResult(
        equity_curve=equity_curve,
        weights=weights,
        metrics=metrics,
        symbols=matrix.symbols,
        config=config,
    )


def backtest_wavelet_factor_stat_arb(
    frame: pl.DataFrame,
    config: WaveletFactorBacktestConfig | None = None,
) -> BacktestResult:
    """Run explicit-factor residual strategy with causal wavelet-style filtering."""
    config = config or WaveletFactorBacktestConfig()
    _validate_config(config)
    matrix = prepare_return_matrix(frame)
    if len(matrix.symbols) < max(config.min_assets, config.n_factors + 1):
        raise ValueError(
            f"Need at least {max(config.min_assets, config.n_factors + 1)} aligned assets; "
            f"got {len(matrix.symbols)}"
        )
    if matrix.log_returns.shape[0] <= config.pca_window + 1:
        raise ValueError("Not enough observations for pca_window and one forward return")

    current_weights = np.zeros(len(matrix.symbols), dtype=float)
    equity = float(config.initial_equity_usdt)
    equity_records: list[dict[str, Any]] = []
    weight_records: list[dict[str, Any]] = []

    first_signal_index = config.pca_window - 1
    first_trade_index = first_signal_index + 1
    for trade_index in range(first_trade_index, matrix.simple_returns.shape[0]):
        signal_index = trade_index - 1
        turnover = 0.0
        cost_usdt = 0.0
        explained_variance = np.nan
        active_positions = int(np.count_nonzero(np.abs(current_weights) > 1e-12))

        if (signal_index - first_signal_index) % config.rebalance_hours == 0:
            target_weights, s_scores, half_life, explained_variance = (
                _compute_wavelet_factor_signal_weights(
                    matrix.log_returns,
                    matrix.symbols,
                    signal_index,
                    current_weights,
                    config,
                )
            )
            turnover = float(np.abs(target_weights - current_weights).sum())
            cost_usdt = equity * config.fee_rate * turnover
            current_weights = target_weights
            active_positions = int(np.count_nonzero(np.abs(current_weights) > 1e-12))

            timestamp = matrix.times[trade_index]
            for symbol_index in np.flatnonzero(np.abs(current_weights) > 1e-12):
                weight_records.append(
                    {
                        "timestamp": timestamp,
                        "symbol": matrix.symbols[symbol_index],
                        "weight": float(current_weights[symbol_index]),
                        "s_score": float(s_scores[symbol_index]),
                        "half_life_bars": float(half_life[symbol_index]),
                        "half_life_hours": float(half_life[symbol_index] * config.bar_hours),
                    }
                )

        gross_return = float(current_weights @ matrix.simple_returns[trade_index])
        cost_return = cost_usdt / equity if equity > 0 else 0.0
        net_return = gross_return - cost_return
        equity *= 1.0 + net_return

        equity_records.append(
            {
                "timestamp": matrix.times[trade_index],
                "gross_return": gross_return,
                "cost_return": cost_return,
                "net_return": net_return,
                "equity_usdt": equity,
                "turnover": turnover,
                "transaction_cost_usdt": cost_usdt,
                "gross_exposure": float(np.abs(current_weights).sum()),
                "net_exposure": float(current_weights.sum()),
                "active_positions": active_positions,
                "model_explained_variance": explained_variance,
            }
        )

    equity_curve = pl.DataFrame(equity_records)
    weights = pl.DataFrame(
        weight_records,
        schema={
            "timestamp": pl.Datetime,
            "symbol": pl.String,
            "weight": pl.Float64,
            "s_score": pl.Float64,
            "half_life_bars": pl.Float64,
            "half_life_hours": pl.Float64,
        },
        orient="row",
    )
    metrics = compute_metrics(equity_curve, config)
    return BacktestResult(
        equity_curve=equity_curve,
        weights=weights,
        metrics=metrics,
        symbols=matrix.symbols,
        config=config,
    )


def backtest_cluster_pca_stat_arb(
    frame: pl.DataFrame,
    config: ClusterPcaBacktestConfig | None = None,
) -> BacktestResult:
    """Run cluster-local PCA residual strategy."""
    config = config or ClusterPcaBacktestConfig()
    _validate_config(config)
    matrix = prepare_return_matrix(frame)
    if len(matrix.symbols) < max(config.min_assets, config.min_cluster_assets):
        raise ValueError(
            f"Need at least {max(config.min_assets, config.min_cluster_assets)} aligned assets; "
            f"got {len(matrix.symbols)}"
        )
    if matrix.log_returns.shape[0] <= config.pca_window + 1:
        raise ValueError("Not enough observations for pca_window and one forward return")

    current_weights = np.zeros(len(matrix.symbols), dtype=float)
    equity = float(config.initial_equity_usdt)
    equity_records: list[dict[str, Any]] = []
    weight_records: list[dict[str, Any]] = []

    first_signal_index = config.pca_window - 1
    first_trade_index = first_signal_index + 1
    for trade_index in range(first_trade_index, matrix.simple_returns.shape[0]):
        signal_index = trade_index - 1
        turnover = 0.0
        cost_usdt = 0.0
        explained_variance = np.nan
        active_positions = int(np.count_nonzero(np.abs(current_weights) > 1e-12))

        if (signal_index - first_signal_index) % config.rebalance_hours == 0:
            target_weights, s_scores, half_life, explained_variance = (
                _compute_cluster_pca_signal_weights(
                    matrix.log_returns,
                    signal_index,
                    current_weights,
                    config,
                )
            )
            turnover = float(np.abs(target_weights - current_weights).sum())
            cost_usdt = equity * config.fee_rate * turnover
            current_weights = target_weights
            active_positions = int(np.count_nonzero(np.abs(current_weights) > 1e-12))

            timestamp = matrix.times[trade_index]
            for symbol_index in np.flatnonzero(np.abs(current_weights) > 1e-12):
                weight_records.append(
                    {
                        "timestamp": timestamp,
                        "symbol": matrix.symbols[symbol_index],
                        "weight": float(current_weights[symbol_index]),
                        "s_score": float(s_scores[symbol_index]),
                        "half_life_bars": float(half_life[symbol_index]),
                        "half_life_hours": float(half_life[symbol_index] * config.bar_hours),
                    }
                )

        gross_return = float(current_weights @ matrix.simple_returns[trade_index])
        cost_return = cost_usdt / equity if equity > 0 else 0.0
        net_return = gross_return - cost_return
        equity *= 1.0 + net_return

        equity_records.append(
            {
                "timestamp": matrix.times[trade_index],
                "gross_return": gross_return,
                "cost_return": cost_return,
                "net_return": net_return,
                "equity_usdt": equity,
                "turnover": turnover,
                "transaction_cost_usdt": cost_usdt,
                "gross_exposure": float(np.abs(current_weights).sum()),
                "net_exposure": float(current_weights.sum()),
                "active_positions": active_positions,
                "model_explained_variance": explained_variance,
            }
        )

    equity_curve = pl.DataFrame(equity_records)
    weights = pl.DataFrame(
        weight_records,
        schema={
            "timestamp": pl.Datetime,
            "symbol": pl.String,
            "weight": pl.Float64,
            "s_score": pl.Float64,
            "half_life_bars": pl.Float64,
            "half_life_hours": pl.Float64,
        },
        orient="row",
    )
    metrics = compute_metrics(equity_curve, config)
    return BacktestResult(
        equity_curve=equity_curve,
        weights=weights,
        metrics=metrics,
        symbols=matrix.symbols,
        config=config,
    )


def compute_metrics(equity_curve: pl.DataFrame, config: BacktestConfig) -> dict[str, float]:
    if equity_curve.is_empty():
        return {
            "total_return": float("nan"),
            "annualized_return": float("nan"),
            "annualized_volatility": float("nan"),
            "sharpe": float("nan"),
            "information_ratio": float("nan"),
            "max_drawdown": float("nan"),
            "average_turnover": float("nan"),
            "annualized_turnover": float("nan"),
            "total_transaction_cost_usdt": 0.0,
        }

    returns = equity_curve.get_column("net_return").to_numpy()
    equity = equity_curve.get_column("equity_usdt").to_numpy()
    mean_return = float(np.mean(returns))
    volatility = float(np.std(returns, ddof=1)) if len(returns) > 1 else 0.0
    annualized_volatility = volatility * np.sqrt(config.periods_per_year)
    sharpe = (
        mean_return / volatility * np.sqrt(config.periods_per_year)
        if volatility > 1e-12
        else float("nan")
    )
    total_return = float(equity[-1] / config.initial_equity_usdt - 1.0)
    years = len(returns) / config.periods_per_year
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
        "annualized_volatility": annualized_volatility,
        "sharpe": sharpe,
        "information_ratio": sharpe,
        "max_drawdown": float(np.min(drawdown)),
        "average_turnover": avg_turnover,
        "annualized_turnover": avg_turnover * config.periods_per_year,
        "total_transaction_cost_usdt": float(
            equity_curve.get_column("transaction_cost_usdt").sum()
        ),
        "average_gross_exposure": float(equity_curve.get_column("gross_exposure").mean()),
        "average_active_positions": float(equity_curve.get_column("active_positions").mean()),
    }


def _write_result(result: BacktestResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    result.equity_curve.write_parquet(output_dir / "equity_curve.parquet")
    result.weights.write_parquet(output_dir / "weights.parquet")
    (output_dir / "metrics.json").write_text(json.dumps(result.metrics, indent=2), encoding="utf-8")
    (output_dir / "config.json").write_text(
        json.dumps(asdict(result.config), indent=2),
        encoding="utf-8",
    )


def _bars_from_hours(hours: float, bar_hours: int) -> int:
    return max(1, int(round(hours / bar_hours)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PCA residual crypto stat-arb backtest.")
    parser.add_argument(
        "--strategy",
        choices=["baseline", "reengineered", "wavelet-factor", "cluster-pca"],
        default="baseline",
        help="Backtest rule set to run.",
    )
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/binance_um_1h"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/reports/pca_residual_backtest"))
    parser.add_argument("--bar-hours", type=int, choices=[1, 4, 12, 24], default=1)
    parser.add_argument("--n-factors", type=int)
    parser.add_argument("--pca-window", type=int, help="PCA rolling window in bars.")
    parser.add_argument("--ar-window", type=int, help="AR rolling window in bars.")
    parser.add_argument("--rebalance-hours", type=int)
    parser.add_argument("--entry-score", type=float)
    parser.add_argument("--max-positions", type=int)
    parser.add_argument("--target-gross", type=float)
    parser.add_argument("--fee-bps", type=float, default=BacktestConfig.fee_bps)
    parser.add_argument("--initial-equity-usdt", type=float, default=BacktestConfig.initial_equity_usdt)
    parser.add_argument("--min-half-life-bars", type=float, default=BacktestConfig.min_half_life_bars)
    parser.add_argument("--max-half-life-bars", type=float)
    parser.add_argument("--disable-half-life-filter", action="store_true")
    parser.add_argument("--exit-score", type=float, default=ReengineeredBacktestConfig.exit_score)
    parser.add_argument("--stop-score", type=float, default=ReengineeredBacktestConfig.stop_score)
    parser.add_argument(
        "--max-turnover-per-rebalance",
        type=float,
        default=ReengineeredBacktestConfig.max_turnover_per_rebalance,
    )
    parser.add_argument(
        "--target-annual-volatility",
        type=float,
        default=ReengineeredBacktestConfig.target_annual_volatility,
    )
    parser.add_argument("--disable-factor-neutralization", action="store_true")
    parser.add_argument(
        "--wavelet-fast-hours",
        type=float,
        default=WaveletFactorBacktestConfig.wavelet_fast_hours,
    )
    parser.add_argument(
        "--wavelet-slow-hours",
        type=float,
        default=WaveletFactorBacktestConfig.wavelet_slow_hours,
    )
    parser.add_argument("--cluster-count", type=int, default=ClusterPcaBacktestConfig.cluster_count)
    parser.add_argument(
        "--min-cluster-assets",
        type=int,
        default=ClusterPcaBacktestConfig.min_cluster_assets,
    )
    args = parser.parse_args()

    frame = resample_ohlc_frame(load_ohlc_dir(args.data_dir), bar_hours=args.bar_hours)

    if args.strategy == "baseline":
        n_factors = args.n_factors if args.n_factors is not None else BacktestConfig.n_factors
        pca_window = args.pca_window
        if pca_window is None:
            pca_window = max(n_factors + 3, _bars_from_hours(24 * 180, args.bar_hours))
        ar_window = args.ar_window
        if ar_window is None:
            ar_window = max(5, _bars_from_hours(24 * 60, args.bar_hours))
        rebalance_bars = _bars_from_hours(
            args.rebalance_hours
            if args.rebalance_hours is not None
            else BacktestConfig.rebalance_hours,
            args.bar_hours,
        )
        config = BacktestConfig(
            n_factors=n_factors,
            pca_window=pca_window,
            ar_window=ar_window,
            rebalance_hours=rebalance_bars,
            entry_score=(
                args.entry_score if args.entry_score is not None else BacktestConfig.entry_score
            ),
            max_positions=(
                args.max_positions if args.max_positions is not None else BacktestConfig.max_positions
            ),
            target_gross=(
                args.target_gross if args.target_gross is not None else BacktestConfig.target_gross
            ),
            fee_bps=args.fee_bps,
            initial_equity_usdt=args.initial_equity_usdt,
            bar_hours=float(args.bar_hours),
            min_half_life_bars=args.min_half_life_bars,
            max_half_life_bars=args.max_half_life_bars,
            use_half_life_filter=not args.disable_half_life_filter,
        )
        result = backtest_pca_stat_arb(frame, config)
    elif args.strategy == "reengineered":
        n_factors = (
            args.n_factors if args.n_factors is not None else ReengineeredBacktestConfig.n_factors
        )
        pca_window = args.pca_window
        if pca_window is None:
            pca_window = max(n_factors + 3, _bars_from_hours(24 * 180, args.bar_hours))
        ar_window = args.ar_window
        if ar_window is None:
            ar_window = max(5, _bars_from_hours(24 * 60, args.bar_hours))
        rebalance_bars = _bars_from_hours(
            args.rebalance_hours
            if args.rebalance_hours is not None
            else ReengineeredBacktestConfig.rebalance_hours,
            args.bar_hours,
        )
        config = ReengineeredBacktestConfig(
            n_factors=n_factors,
            pca_window=pca_window,
            ar_window=ar_window,
            rebalance_hours=rebalance_bars,
            entry_score=(
                args.entry_score
                if args.entry_score is not None
                else ReengineeredBacktestConfig.entry_score
            ),
            max_positions=(
                args.max_positions
                if args.max_positions is not None
                else ReengineeredBacktestConfig.max_positions
            ),
            target_gross=(
                args.target_gross
                if args.target_gross is not None
                else ReengineeredBacktestConfig.target_gross
            ),
            fee_bps=args.fee_bps,
            initial_equity_usdt=args.initial_equity_usdt,
            bar_hours=float(args.bar_hours),
            min_half_life_bars=args.min_half_life_bars,
            max_half_life_bars=args.max_half_life_bars,
            use_half_life_filter=not args.disable_half_life_filter,
            exit_score=args.exit_score,
            stop_score=args.stop_score,
            max_turnover_per_rebalance=args.max_turnover_per_rebalance,
            target_annual_volatility=args.target_annual_volatility,
            factor_neutralize=not args.disable_factor_neutralization,
        )
        result = backtest_pca_stat_arb_reengineered(frame, config)
    elif args.strategy == "wavelet-factor":
        n_factors = (
            args.n_factors if args.n_factors is not None else WaveletFactorBacktestConfig.n_factors
        )
        pca_window = args.pca_window
        if pca_window is None:
            pca_window = max(n_factors + 3, _bars_from_hours(24 * 180, args.bar_hours))
        ar_window = args.ar_window
        if ar_window is None:
            ar_window = max(5, _bars_from_hours(24 * 60, args.bar_hours))
        rebalance_bars = _bars_from_hours(
            args.rebalance_hours
            if args.rebalance_hours is not None
            else WaveletFactorBacktestConfig.rebalance_hours,
            args.bar_hours,
        )
        config = WaveletFactorBacktestConfig(
            n_factors=n_factors,
            pca_window=pca_window,
            ar_window=ar_window,
            rebalance_hours=rebalance_bars,
            entry_score=(
                args.entry_score
                if args.entry_score is not None
                else WaveletFactorBacktestConfig.entry_score
            ),
            max_positions=(
                args.max_positions
                if args.max_positions is not None
                else WaveletFactorBacktestConfig.max_positions
            ),
            target_gross=(
                args.target_gross
                if args.target_gross is not None
                else WaveletFactorBacktestConfig.target_gross
            ),
            fee_bps=args.fee_bps,
            initial_equity_usdt=args.initial_equity_usdt,
            bar_hours=float(args.bar_hours),
            min_half_life_bars=args.min_half_life_bars,
            max_half_life_bars=args.max_half_life_bars,
            use_half_life_filter=not args.disable_half_life_filter,
            exit_score=args.exit_score,
            stop_score=args.stop_score,
            max_turnover_per_rebalance=args.max_turnover_per_rebalance,
            target_annual_volatility=args.target_annual_volatility,
            factor_neutralize=not args.disable_factor_neutralization,
            wavelet_fast_hours=args.wavelet_fast_hours,
            wavelet_slow_hours=args.wavelet_slow_hours,
        )
        result = backtest_wavelet_factor_stat_arb(frame, config)
    else:
        n_factors = args.n_factors if args.n_factors is not None else ClusterPcaBacktestConfig.n_factors
        pca_window = args.pca_window
        if pca_window is None:
            pca_window = max(n_factors + 3, _bars_from_hours(24 * 180, args.bar_hours))
        ar_window = args.ar_window
        if ar_window is None:
            ar_window = max(5, _bars_from_hours(24 * 60, args.bar_hours))
        rebalance_bars = _bars_from_hours(
            args.rebalance_hours
            if args.rebalance_hours is not None
            else ClusterPcaBacktestConfig.rebalance_hours,
            args.bar_hours,
        )
        config = ClusterPcaBacktestConfig(
            n_factors=n_factors,
            pca_window=pca_window,
            ar_window=ar_window,
            rebalance_hours=rebalance_bars,
            entry_score=(
                args.entry_score if args.entry_score is not None else ClusterPcaBacktestConfig.entry_score
            ),
            max_positions=(
                args.max_positions
                if args.max_positions is not None
                else ClusterPcaBacktestConfig.max_positions
            ),
            target_gross=(
                args.target_gross
                if args.target_gross is not None
                else ClusterPcaBacktestConfig.target_gross
            ),
            fee_bps=args.fee_bps,
            initial_equity_usdt=args.initial_equity_usdt,
            bar_hours=float(args.bar_hours),
            min_half_life_bars=args.min_half_life_bars,
            max_half_life_bars=args.max_half_life_bars,
            use_half_life_filter=not args.disable_half_life_filter,
            exit_score=args.exit_score,
            stop_score=args.stop_score,
            max_turnover_per_rebalance=args.max_turnover_per_rebalance,
            target_annual_volatility=args.target_annual_volatility,
            factor_neutralize=not args.disable_factor_neutralization,
            cluster_count=args.cluster_count,
            min_cluster_assets=args.min_cluster_assets,
        )
        result = backtest_cluster_pca_stat_arb(frame, config)
    _write_result(result, args.output_dir)
    print(json.dumps(result.metrics, indent=2))


if __name__ == "__main__":
    main()
