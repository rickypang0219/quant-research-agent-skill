---
name: production-readiness
description: Use when deciding whether quant research is ready for paper trading, live trading, deployment, monitoring, risk controls, production integration, or capital scaling.
---

# Production Readiness Skill

## Scope

Use this skill to decide whether a strategy or system can move from research to paper, from paper to live, or from small live to larger capital.

Default answer should be conservative. Production readiness is not a reward for a good backtest. It is a claim that the system can behave safely when markets, data, exchanges, and code fail.

## Readiness Levels

```text
L0 - Idea:
    No reproducible evidence.

L1 - Signal evidence:
    Observable, label, baseline, and basic predictive evidence exist.

L2 - Vectorized backtest:
    Lag-safe, cost-aware, reproducible, out-of-sample tested.

L3 - Event-driven replay:
    Order lifecycle, fills, latency, costs, and risk modeled.

L4 - Paper trading:
    Live data, paper orders, monitoring, reconciliation, and incident logs.

L5 - Small live:
    Tiny capital, hard limits, tested kill switch, daily review.

L6 - Scaled live:
    Only after stable small-live performance, capacity analysis, and operational maturity.
```

## Required Evidence

Before paper:

- reproducible backtest;
- data manifest;
- cost model;
- validation report;
- risk limits;
- event-driven execution assumption or clear reason it is unnecessary.

Before small live:

- paper trading report;
- live-vs-sim drift analysis;
- order/fill/reconciliation logs;
- monitoring and alerting;
- kill switch tested;
- rollback plan;
- max loss and position caps.

Before scaling:

- capacity analysis;
- slippage and impact estimates;
- drawdown and tail stress;
- stability across regimes;
- incident history;
- independent code/backtest review.

## Go / No-Go Criteria

Use:

- **GO:** evidence is reproducible, risks are bounded, and monitoring/rollback exist.
- **CONDITIONAL GO:** proceed only with explicit caps and fixes.
- **NO-GO:** missing accounting, leakage risk, untested execution, absent risk controls, or unexplained paper/live drift.
- **RESEARCH ONLY:** idea may be worth studying but is not deployable.

## Output Standard

When invoked, produce:

1. Readiness level
2. Evidence available
3. Blocking gaps
4. Risk controls required
5. Operational controls required
6. Tests required
7. Go/no-go verdict

