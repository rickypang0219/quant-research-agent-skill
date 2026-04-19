---
name: code-review
description: Use when reviewing quant research code, backtest code, live trading infrastructure, Python/Rust implementations, data pipelines, model training code, PnL accounting, leakage risks, tests, performance, and production safety.
---

# Quant Code Review Skill

## Scope

Use this skill for code review or code improvement. The review posture is adversarial and practical: find correctness bugs, hidden leakage, timing mistakes, risk gaps, and missing tests before style nits.

## Review Priority

Order findings by severity:

1. Money-losing correctness bugs.
2. Lookahead/data leakage.
3. PnL/accounting errors.
4. Execution/fill/risk assumptions that cannot hold live.
5. Data quality and timestamp bugs.
6. Numerical instability.
7. Performance bottlenecks that affect research or live behavior.
8. Missing tests.
9. Maintainability.
10. Style.

## Quant Review Questions

Ask:

- Does every timestamp mean event time, exchange time, local receive time, or decision time?
- Does signal at `t` only use data available before execution?
- Are positions lagged correctly relative to returns?
- Are costs charged on trades, not returns?
- Are funding/borrow/fees included where relevant?
- Are futures/perp contract multipliers correct?
- Is the universe point-in-time?
- Are missing data, delistings, and symbol changes handled?
- Are factors/normalizers/scalers fit only on training data?
- Are matrix dimensions and index alignments explicit?
- Are risk checks pre-trade and post-trade?
- Can the system restart and reconcile state?

## Python Standards

Prefer:

- small typed functions;
- `polars`/`pandas` with explicit sort and group keys;
- explicit timezone handling;
- schema validation with `pydantic` where inputs cross boundaries;
- vectorization where natural;
- `pytest` toy examples for PnL and leakage;
- `ruff` for linting;
- `ty` or `mypy` for serious packages.

Watch for:

- accidental same-bar execution;
- groupby operations that mix assets;
- rolling windows not sorted by timestamp;
- joins that create duplicates;
- forward fills across symbols;
- global z-scores where cross-sectional z-scores were intended;
- training scalers on full data;
- silent NaN handling.

## Rust Standards

Prefer:

- explicit state machines for orders/fills;
- `Result`-based error handling;
- `tracing` for structured logs;
- deterministic tests;
- bounded queues and backpressure;
- clear ownership around position/order state;
- benchmarks only after correctness tests.

Watch for:

- async tasks swallowing errors;
- unbounded channels in live paths;
- shared mutable state without clear synchronization;
- implicit float assumptions;
- panics in exchange-facing code;
- loss of precision in price/quantity conversions.

## Required Tests

For quant code, request or add tests for:

- previous position earns next return;
- fee charged on position change;
- no trade on missing/stale data;
- cross-asset lag does not leak;
- train/test split boundary;
- order rejected by risk limit;
- partial fill accounting;
- restart/reconciliation state;
- exchange filter rounding;
- deterministic rerun.

## Output Format

Use the normal review style:

1. Findings first, ordered by severity, with file/line references.
2. Open questions or assumptions.
3. Minimal patch or design direction.
4. Tests to add.

If no serious issue is found, say so clearly and name remaining test gaps.

