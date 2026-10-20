# Verification Commands

## Baseline Checks

Run after Python edits:

```bash
uv run --extra dev pytest
uv run ruff check
```

Last observed result:

```text
uv run --extra dev pytest
11 passed

uv run ruff check
All checks passed!
```

## Data Audit

Run if local data exists and you touch data collection, schema, resampling, or OHLC repair:

```bash
uv run python -m research.crypto_stat_arb.binance_ohlc audit --data-dir data/raw/binance_um_1h_onboard_20230101_all
```

Last observed result:

```json
{
  "row_count": 3181310,
  "symbol_count": 110,
  "duplicate_rows": 0,
  "bad_ohlc_rows": 0,
  "negative_volume_rows": 0,
  "missing_intervals": 0,
  "symbols_with_gaps": [],
  "ok": true
}
```

## Reproduce Expanded-Data Collection

Requires network access. Do not run blindly if rate limits or runtime matter.

```bash
uv run python -m research.crypto_stat_arb.binance_ohlc collect \
  --start 2023-01-01 \
  --end 2026-04-20 \
  --onboard-cutoff 2023-01-01 \
  --output-dir data/raw/binance_um_1h_onboard_20230101_all \
  --request-sleep-seconds 2.0
```

## Representative Backtest Smoke Run

Requires local data.

```bash
uv run python -m research.crypto_stat_arb.pca_residual_backtest \
  --strategy wavelet-factor \
  --data-dir data/raw/binance_um_1h_onboard_20230101_all \
  --output-dir data/reports/wavelet_factor_110_24h \
  --bar-hours 24 \
  --max-positions 20
```

Known recent output for this exact run:

```json
{
  "total_return": 0.05338284269639737,
  "annualized_return": 0.0186920223795064,
  "annualized_volatility": 0.03125380197435566,
  "sharpe": 0.6079987615973689,
  "information_ratio": 0.6079987615973689,
  "max_drawdown": -0.031161384042457163,
  "average_turnover": 0.005976602419728266,
  "annualized_turnover": 2.181459883200817,
  "total_transaction_cost_usdt": 378.770190158191,
  "average_gross_exposure": 0.0041460979061279345,
  "average_active_positions": 0.08097560975609756
}
```
