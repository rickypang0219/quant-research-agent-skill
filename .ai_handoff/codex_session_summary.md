# Codex Session Summary

No raw Codex session transcript was copied into this repository.

Latest session files were located under `~/.codex/sessions/`, but they were not opened or copied because session transcripts can contain private prompts or other sensitive context.

Safe summary of the relevant work:

- The user requested a PCA/stat-arb research module for crypto statistical arbitrage using Binance USD-M perpetual OHLC data.
- The repo originally focused on `research-skill/`; a Python research module was added under `research/crypto_stat_arb/`.
- Data collection was expanded from a 50-symbol current top-volume universe to 110 current `TRADING` USDT perpetuals onboarded by `2023-01-01`.
- One vendor candle inconsistency was found and conservatively repaired.
- PCA and wavelet/explicit-factor residual backtests were run across 4h/12h/24h variants.
- Results do not justify paper/live trading. The best-looking 24h wavelet result barely deployed capital; active trading variants lost money or had high turnover/cost.
- A known unresolved issue is that final active position count can exceed the intended `max_positions` after hysteresis/projection.
