# AI Handoff

Generated from repository root: `/Users/kachunpang/quant-research-agent-skill`

## Project Summary

This repository is a quant research and live-trading development lab. It contains:

- `research-skill/`: model-neutral instruction/skill library for quant research, strategy review, code review, data audit, risk, and live-trading discipline.
- `research/crypto_stat_arb/`: Python research modules for crypto statistical arbitrage experiments using Binance USD-M perpetual OHLC data, PCA/explicit-factor residuals, AR(1) s-scores, half-life filters, transaction costs, and vectorized backtests.
- `tests/`: pytest tests for core backtest mechanics, factor/dollar neutral projection, turnover caps, resampling, and OHLC repair.

The current research problem is crypto statistical arbitrage using residual mean reversion. The project is not live-trading ready.

## Current Task Summary

The latest user request was to prepare a clean, model-neutral handoff bundle so another AI coding agent can continue if Codex quota is exhausted. This directory is the handoff bundle.

Previous active research work:

- Built a Python/uv research module for Binance USD-M perpetual OHLC collection and PCA/wavelet-factor residual backtests.
- Collected current Binance `TRADING` USDT perpetuals with `onboardDate <= 2023-01-01`.
- Found 110 current eligible symbols, not 130, using Binance's current `exchangeInfo` endpoint.
- Collected 1h OHLC from `2023-01-01 00:00:00 UTC` through `2026-04-20 00:00:00 UTC`.
- Audited 3,181,310 rows: 110 symbols, 28,921 rows each, zero duplicates, zero missing hourly intervals, zero bad OHLC rows after one conservative vendor-candle repair.
- Reran expanded-universe backtests. Results are not strong enough for paper/live trading.

## Architecture Summary

Python package:

- `research/crypto_stat_arb/binance_ohlc.py`
  - Selects current Binance USD-M USDT perpetual symbols by `onboardDate`.
  - Fetches 1h klines with retry/backoff for HTTP 418/429 and transient socket failures.
  - Converts klines to a Polars OHLC schema.
  - Repairs vendor OHLC candle bound inconsistencies by widening high/low while preserving open/close.
  - Audits schema, duplicates, OHLC validity, volume, and hourly gaps.

- `research/crypto_stat_arb/pca_residual_backtest.py`
  - Prepares aligned close-to-close return matrices.
  - Supports 1h, 4h, 12h, and 24h resampling.
  - Implements baseline PCA residual AR(1) s-score backtest.
  - Implements reengineered PCA variant with hysteresis, half-life gating, turnover cap, factor neutralization, and volatility scaling.
  - Implements explicit BTC/ETH/equal-weight-market residual model with causal Haar-style band-pass filtering.
  - Writes `equity_curve.parquet`, `weights.parquet`, `metrics.json`, and `config.json`.

Dependency management:

- Use `uv`.
- `pyproject.toml` declares runtime dependencies: `numpy`, `polars`, `scipy`.
- Dev dependencies: `pytest`, `ruff`.

Data/report directories:

- `data/raw/` and `data/reports/` are intentionally gitignored.
- Existing local data may be present but should not be assumed on another machine.

## Important Design Decisions

- Timing convention: signal uses information through close `t`; position earns close-to-close return from `t` to `t+1`.
- Transaction cost: `fee_bps / 10000 * equity * turnover`, with current commission default `6 bps`.
- Crypto annualization uses 365 days: `periods_per_year = 365 * 24 / bar_hours`.
- Sharpe is simple IID-style annualization of per-bar net returns; it is not Newey-West/Lo adjusted.
- Half-life is measured in bars; output also includes half-life in hours.
- Half-life eligibility requires `min_half_life_bars <= half_life_bars < pca_window / 2` unless an explicit max is lower.
- PCA factor count must be smaller than asset count; `_pca_residuals` validates this.
- Factor neutrality uses projection in asset space so `1^T w = 0` and `Beta^T w = 0` when feasible.
- The Binance universe is current-TRADING only, not a true historical point-in-time instrument master.
- The module is a research/falsification tool, not a live execution system.

## Files Changed Recently

Tracked modified:

- `AGENTS.md`: added repository-specific quickstart, uv commands, and no-secrets/no-hallucination reminders.
- `.gitignore`: ignores Python caches, uv cache, virtualenv, and local data/report outputs.

Untracked project files:

- `pyproject.toml`
- `uv.lock`
- `research/crypto_stat_arb/__init__.py`
- `research/crypto_stat_arb/binance_ohlc.py`
- `research/crypto_stat_arb/pca_residual_backtest.py`
- `tests/test_binance_ohlc.py`
- `tests/test_pca_residual_backtest.py`
- `.ai_handoff/*`

Local ignored artifacts:

- `data/raw/binance_um_1h/` top-50-ish earlier dataset.
- `data/raw/binance_um_1h_onboard_20230101_all/` expanded 110-symbol dataset.
- `data/reports/*` backtest result directories.
- `.venv/`, caches, `__pycache__/`.

## Open TODOs

High priority:

- Fix or redesign final hard cardinality enforcement. In expanded 110-symbol runs, `active_positions` can exceed `--max-positions` after hysteresis/projection. Treat current `max_positions` as an entry-selection cap, not a guaranteed final portfolio cap.
- Add tests proving final active position count cannot exceed the configured hard limit after factor projection, turnover cap, and forced exits.
- Add cluster-specific factor models instead of relying on global PCA or global BTC/ETH/market residuals.
- Add liquidity filters and participation/capacity checks before accepting lower-volume tail symbols.
- Add slippage/spread/funding models. Current cost model includes commission only.
- Add Newey-West/Lo adjusted Sharpe or autocorrelation-aware performance diagnostics.
- Add point-in-time universe support. Current Binance endpoint excludes delisted contracts and is survivorship-biased.

Research TODOs:

- Compare cluster-specific factors on 4h/12h/24h bars.
- Require enough active candidates relative to constraints before projection, e.g. active names > `constraints + buffer`.
- Add regime/year split and out-of-sample/walk-forward validation.
- Add signal diagnostics: signal decay, bucket monotonicity, IC/rank IC, turnover by signal bucket.
- Add PnL decomposition: gross alpha, cost drag, factor exposure, funding, slippage.

Engineering TODOs:

- Add a resumable manifest for data collection instead of relying only on existing parquet files.
- Add unit tests for downloader retry behavior with mocked HTTP/socket failures.
- Add schema/data-contract docs for raw OHLC and result outputs.

## Known Bugs Or Failing Tests

Known bug/risk:

- `max_positions` is not a strict final hard cap after all portfolio transformations. Recent 110-symbol wavelet runs reported max active positions above 20.

Current test/check status:

- `uv run --extra dev pytest`: passing, 11 tests.
- `uv run ruff check`: passing.
- `uv run python -m research.crypto_stat_arb.binance_ohlc audit --data-dir data/raw/binance_um_1h_onboard_20230101_all`: passing locally if the expanded data exists.

No currently known failing tests.

## Recent Backtest Results

Expanded 110-symbol runs:

| Run | Total Return | Sharpe | Max DD | Annual Turnover | Cost USDT | Avg Gross | Avg Active |
|---|---:|---:|---:|---:|---:|---:|---:|
| `wavelet_factor_110_24h` | `+5.34%` | `0.608` | `-3.12%` | `2.18x` | `378.77` | `0.004` | `0.081` |
| `wavelet_factor_110_12h` | `-11.23%` | `-0.218` | `-26.24%` | `94.70x` | `16015.96` | `0.632` | `22.638` |
| `wavelet_factor_110_4h` | `-8.52%` | `-0.277` | `-15.63%` | `76.90x` | `12561.76` | `0.417` | `14.850` |
| `pca_reengineered_110_24h_1factor` | `-29.99%` | `-0.718` | `-33.45%` | `62.68x` | `8768.42` | `0.459` | `6.295` |

Interpretation:

- The only positive expanded-universe run barely deploys capital, so it is not meaningful as tradable evidence.
- Runs that actually deploy capital lose money and/or pay high transaction costs.
- Do not present current results as alpha.

## Commands To Run Before Editing

```bash
git status --short
git diff -- . ':!data'
sed -n '1,220p' AGENTS.md
sed -n '1,220p' .ai_handoff/HANDOFF.md
```

For quant/backtest work, read relevant skills, usually:

```bash
sed -n '1,220p' research-skill/domain/statistical-arbitrage/SKILL.md
sed -n '1,220p' research-skill/prof/strang/SKILL.md
sed -n '1,220p' research-skill/domain/risk/SKILL.md
sed -n '1,220p' research-skill/workflow/backtest-review/SKILL.md
sed -n '1,220p' research-skill/workflow/code-review/SKILL.md
```

## Commands To Run After Editing

Always for Python changes:

```bash
uv run --extra dev pytest
uv run ruff check
```

If touching data collection or OHLC handling:

```bash
uv run python -m research.crypto_stat_arb.binance_ohlc audit --data-dir data/raw/binance_um_1h_onboard_20230101_all
```

If touching backtest logic, rerun at least one synthetic/unit path plus one real-data smoke run if data exists. Example:

```bash
uv run python -m research.crypto_stat_arb.pca_residual_backtest \
  --strategy wavelet-factor \
  --data-dir data/raw/binance_um_1h_onboard_20230101_all \
  --output-dir data/reports/wavelet_factor_110_24h \
  --bar-hours 24 \
  --max-positions 20
```

## Rules For Future AI Agents

- Read `AGENTS.md` first.
- Read `.ai_handoff/HANDOFF.md` before editing.
- Inspect `git status --short` and `git diff`.
- Summarize your understanding before making changes.
- Make the smallest safe change.
- Preserve the current research/live-trading separation.
- Do not claim live readiness.
- Do not invent data, exchange behavior, or performance results.
- Do not read or copy secrets such as `.env`, API keys, exchange credentials, or `~/.codex/auth.json`.
- Prefer `polars` for data processing and `numpy/scipy` for linear algebra.
- Keep timing assumptions explicit and avoid lookahead bias.
- Include transaction costs in every strategy result.
- Run verification commands and report failures honestly.

## Do Not Break

- Signal timing: no same-bar lookahead.
- Cost accounting: fees charged on position changes/turnover.
- Dollar neutrality: `1^T w = 0` where intended.
- Factor neutrality: `Beta^T w = 0` where intended and feasible.
- Matrix shape safety: PCA/factor columns must be fewer than assets/observations as appropriate.
- Half-life units: bars internally, hours only as derived output.
- Data contract: UTC timestamps, one row per symbol/hour, no duplicate `(timestamp, symbol)`.
- Conservative OHLC repair: preserve open/close, widen high/low only.
- Gitignored local data: do not commit raw Binance parquet data or report parquet outputs.
