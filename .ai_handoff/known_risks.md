# Known Risks

## Potentially Dangerous Files / Paths

- `data/raw/`: local Binance OHLC parquet data. Large, gitignored, may be stale, may contain survivorship bias. Do not commit.
- `data/reports/`: local backtest outputs. Gitignored. Do not treat as authoritative without reproducing commands.
- `.env`: do not read, print, copy, or commit if present.
- `~/.codex/auth.json`: do not read, print, copy, or commit.
- Any API/exchange credential file: do not read, print, copy, or commit.
- `uv.lock`: untracked but important for reproducibility. Avoid hand-editing.
- `research/crypto_stat_arb/pca_residual_backtest.py`: high-risk strategy accounting logic. Small timing/cost changes can invalidate all results.
- `research/crypto_stat_arb/binance_ohlc.py`: data contract and repair logic. Small changes can alter the research dataset.

## Areas Where Another Model May Hallucinate

- Claiming the strategy has alpha because one 24h wavelet-factor run is positive. That run had average gross exposure around `0.004`, so it barely traded.
- Treating Binance current `exchangeInfo` as a historical point-in-time universe. It is not; delisted contracts are missing.
- Assuming there are exactly 130 eligible coins. Current Binance `TRADING` USDT perpetuals onboarded by `2023-01-01` returned 110 symbols.
- Treating `max_positions` as a guaranteed final hard cap. It is currently not reliable after final projection/hysteresis.
- Treating simple annualized Sharpe as robust. It is not autocorrelation-adjusted.
- Treating commission-only cost as realistic. Spread, slippage, funding, market impact, and execution failures are not modeled.
- Confusing half-life bars with hours. Internal half-life is in bars; hours are derived by multiplying by `bar_hours`.
- Assuming PCA factor exposures are stable or economically meaningful. This has not been proven.

## Data / API / Secrets Risks

- Binance collection requires network access and may hit HTTP 418/429 or transient connection resets.
- Downloader retries transient failures but is not a production ingestion system.
- Current data collection has survivorship bias.
- Local data availability is machine-specific; another agent should check files before running data-dependent commands.
- Do not place API keys in source, docs, prompts, or handoff files.

## Tests That Must Be Run

For any Python code change:

```bash
uv run --extra dev pytest
uv run ruff check
```

For data/collection/OHLC changes:

```bash
uv run python -m research.crypto_stat_arb.binance_ohlc audit --data-dir data/raw/binance_um_1h_onboard_20230101_all
```

For backtest logic changes, add or update unit tests first when possible, then run at least one representative real-data smoke run if data is available.

## Assumptions That Must Be Checked

- Data exists locally before running backtests.
- UTC timestamp semantics are preserved.
- `(timestamp, symbol)` remains unique.
- Signals use only data available before the traded return interval.
- Fees are charged on weight changes/turnover.
- Factor/dollar neutrality remains enforced where configured.
- Final active position count is actually bounded if the user asks for a hard cap.
- Universe selection is explicitly described as current-TRADING unless a historical instrument master is added.
