# Copy-Paste Prompt For Next AI Coding Agent

You are continuing work in `/Users/kachunpang/quant-research-agent-skill`.

Do not start by coding. First:

1. Read `AGENTS.md`.
2. Read `.ai_handoff/HANDOFF.md`.
3. Inspect `git status --short`.
4. Inspect `git diff -- . ':!data'`.
5. Skim `.ai_handoff/known_risks.md` and `.ai_handoff/verify_commands.md`.
6. Summarize your understanding of the project, current state, and the next smallest safe change before editing.

Project context:

- This is a quant research and live-trading development lab.
- Current Python research code lives under `research/crypto_stat_arb/`.
- It collects Binance USD-M perpetual OHLC data and runs crypto stat-arb residual mean-reversion backtests.
- The current strategy is not live-ready and should not be presented as proven alpha.
- Existing data/report outputs are local and gitignored.

Important rules:

- Make the smallest safe change.
- Preserve the current architecture unless the user explicitly asks for a redesign.
- Keep research code separate from live-trading assumptions.
- Do not introduce lookahead bias.
- Preserve transaction-cost accounting.
- Preserve dollar/factor neutrality semantics where intended.
- Use `uv` for Python dependency management.
- Prefer `polars` for data processing and `numpy/scipy` for linear algebra.
- Do not read, copy, print, or commit secrets: no `.env`, no API keys, no exchange keys, no private credential files, no `~/.codex/auth.json`.
- Report uncertainty instead of inventing missing context.

Before editing, run or inspect:

```bash
git status --short
git diff -- . ':!data'
```

After Python edits, run:

```bash
uv run --extra dev pytest
uv run ruff check
```

If touching data collection or OHLC schema and local data exists, also run:

```bash
uv run python -m research.crypto_stat_arb.binance_ohlc audit --data-dir data/raw/binance_um_1h_onboard_20230101_all
```

Known unfinished issue to consider only if the user asks for strategy/backtest work:

- `max_positions` is not currently a strict final hard cap after hysteresis/projection; recent expanded-universe runs showed active positions above the requested cap. Fixing this should include tests.
