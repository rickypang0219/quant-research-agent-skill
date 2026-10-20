"""Tests for the event-driven cost-aware stat-arb backtest."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import numpy as np
import polars as pl
import pytest

from research.crypto_stat_arb.event_driven_backtest import (
    EventDrivenConfig,
    apply_no_trade_band,
    backtest_event_driven,
    marchenko_pastur_factor_count,
    prepare_panel,
    trading_fee_rate,
)


def _synthetic_ohlc(
    *,
    n_symbols: int = 12,
    n_bars: int = 400,
    seed: int = 7,
) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    start = datetime(2024, 1, 1, tzinfo=UTC)
    market = rng.normal(0.0, 0.01, size=n_bars)
    rows: list[dict[str, object]] = []
    for symbol_index in range(n_symbols):
        symbol = f"SYM{symbol_index:02d}USDT" if symbol_index else "BTCUSDT"
        beta = 1.0 + 0.1 * symbol_index
        spread = np.zeros(n_bars)
        for t in range(1, n_bars):
            spread[t] = 0.9 * spread[t - 1] + rng.normal(0.0, 0.004)
        returns = beta * market + np.diff(np.concatenate([[0.0], spread]))
        close = 100.0 * np.exp(np.cumsum(returns))
        for t in range(n_bars):
            rows.append(
                {
                    "timestamp": start + timedelta(hours=t),
                    "symbol": symbol,
                    "close": float(close[t]),
                    "quote_volume": float(1e6 * (n_symbols - symbol_index)),
                }
            )
    return pl.DataFrame(rows).with_columns(
        pl.col("timestamp").dt.replace_time_zone("UTC", ambiguous="raise")
    )


def _small_config(**overrides: object) -> EventDrivenConfig:
    defaults: dict[str, object] = {
        "pca_window": 120,
        "ar_window": 40,
        "pca_refit_bars": 12,
        "max_positions": 6,
        "min_assets": 6,
        "universe_size": 10,
        "liquidity_window_bars": 24,
        "target_annual_volatility": None,
        "include_funding": False,
        "cost_multiple": 0.0,
        "no_trade_band": 0.0,
    }
    defaults.update(overrides)
    return EventDrivenConfig(**defaults)  # type: ignore[arg-type]


def test_marchenko_pastur_keeps_dominant_factor_only() -> None:
    rng = np.random.default_rng(0)
    t, n = 600, 20
    market = rng.normal(size=(t, 1))
    noise = rng.normal(size=(t, n))
    data = market @ np.full((1, n), 0.9) + 0.4 * noise
    standardized = (data - data.mean(axis=0)) / data.std(axis=0, ddof=1)
    eigenvalues = np.sort(
        np.linalg.eigvalsh(standardized.T @ standardized / (t - 1))
    )[::-1]
    count = marchenko_pastur_factor_count(
        eigenvalues, n_observations=t, n_assets=n, max_factors=10
    )
    assert count == 1


def test_no_trade_band_skips_small_changes_but_forces_exits() -> None:
    current = np.array([0.05, -0.05, 0.05, 0.0])
    target = np.array([0.052, 0.0, 0.10, 0.001])
    executed = apply_no_trade_band(current, target, band=0.01)
    assert executed[0] == pytest.approx(0.05)  # small adjustment skipped
    assert executed[1] == pytest.approx(0.0)  # forced exit always executes
    assert executed[2] == pytest.approx(0.10)  # large adjustment executes
    assert executed[3] == pytest.approx(0.0)  # tiny entry skipped


def test_trading_fee_splits_maker_and_taker() -> None:
    config = EventDrivenConfig(maker_fee_bps=2.0, taker_fee_bps=5.0)
    current = np.array([0.0, 0.10, -0.10])
    executed = np.array([0.10, 0.0, -0.04])
    fee, turnover = trading_fee_rate(current, executed, config)
    # 0.10 opened (maker), 0.10 closed (taker), 0.06 reduced (taker).
    expected = 0.10 * 2e-4 + (0.10 + 0.06) * 5e-4
    assert fee == pytest.approx(expected)
    assert turnover == pytest.approx(0.10 + 0.10 + 0.06)


def test_trading_fee_sign_flip_pays_taker_then_maker() -> None:
    config = EventDrivenConfig(maker_fee_bps=2.0, taker_fee_bps=5.0)
    current = np.array([0.10])
    executed = np.array([-0.05])
    fee, turnover = trading_fee_rate(current, executed, config)
    expected = 0.10 * 5e-4 + 0.05 * 2e-4
    assert fee == pytest.approx(expected)
    assert turnover == pytest.approx(0.15)


def test_funding_assigned_to_holding_interval() -> None:
    start = datetime(2024, 1, 1, tzinfo=UTC)
    rows = []
    for t in range(12):
        for symbol in ("AAAUSDT", "BBBUSDT"):
            rows.append(
                {
                    "timestamp": start + timedelta(hours=t),
                    "symbol": symbol,
                    "close": 100.0 + t,
                    "quote_volume": 1.0,
                }
            )
    ohlc = pl.DataFrame(rows).with_columns(
        pl.col("timestamp").dt.replace_time_zone("UTC", ambiguous="raise")
    )
    funding = pl.DataFrame(
        {
            "timestamp": [datetime(2024, 1, 1, 8, tzinfo=UTC)],
            "symbol": ["AAAUSDT"],
            "funding_rate": [0.0001],
        }
    ).with_columns(pl.col("timestamp").dt.replace_time_zone("UTC", ambiguous="raise"))

    panel = prepare_panel(ohlc, funding_frame=funding, bar_hours=1.0)
    column = panel.symbols.index("AAAUSDT")
    # The 08:00 funding event settles on the position held over (07:00, 08:00].
    row = list(panel.times_ms).index(
        int(datetime(2024, 1, 1, 7, tzinfo=UTC).timestamp() * 1000)
    )
    assert panel.funding[row, column] == pytest.approx(0.0001)
    assert float(np.abs(panel.funding).sum()) == pytest.approx(0.0001)


def test_backtest_respects_hard_position_cap_and_gross_limit() -> None:
    frame = _synthetic_ohlc()
    config = _small_config(max_positions=4)
    result = backtest_event_driven(frame, config=config)
    max_active = int(result.equity_curve.get_column("active_positions").max())
    # Residual names are capped at max_positions; the BTC hedge adds one leg.
    assert max_active <= config.max_positions + 1
    max_gross = float(result.equity_curve.get_column("gross_exposure").max())
    assert max_gross <= config.target_gross * 1.5 + 1e-9
    equity = result.equity_curve.get_column("equity_usdt").to_numpy()
    assert np.isfinite(equity).all()


def test_cost_filter_blocks_entries() -> None:
    frame = _synthetic_ohlc(seed=3)
    permissive = backtest_event_driven(frame, config=_small_config())
    strict = backtest_event_driven(
        frame, config=_small_config(cost_multiple=1e6, no_trade_band=0.0)
    )
    assert permissive.metrics["bars_traded"] > 0
    assert strict.metrics["entries_blocked_by_cost"] >= strict.metrics["entry_candidates"] - 0.5
    assert strict.metrics["bars_traded"] <= permissive.metrics["bars_traded"]
    assert float(strict.equity_curve.get_column("gross_exposure").max()) == pytest.approx(0.0)


def test_no_funding_flag_requires_no_frame() -> None:
    frame = _synthetic_ohlc(seed=5)
    with pytest.raises(ValueError, match="include_funding"):
        backtest_event_driven(frame, config=_small_config(include_funding=True))


def test_weights_drift_between_trades() -> None:
    frame = _synthetic_ohlc(seed=11)
    # A huge band means positions are never adjusted after entry, so any change
    # in gross exposure between consecutive bars must come from price drift.
    config = _small_config(no_trade_band=10.0, hedge_with_btc=False)
    result = backtest_event_driven(frame, config=config)
    gross = result.equity_curve.get_column("gross_exposure").to_numpy()
    held = gross > 0
    if held.any():
        drifting = np.flatnonzero(held[:-1] & held[1:] )
        assert len(drifting) > 0
        changes = np.abs(gross[drifting + 1] - gross[drifting])
        assert float(changes.max()) > 0.0
