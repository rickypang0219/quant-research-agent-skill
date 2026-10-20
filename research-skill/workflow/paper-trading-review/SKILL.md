---
name: paper-trading-review
description: Use to review paper trading and shadow trading: live-vs-backtest drift, submitted vs accepted orders, simulated vs actual fills, latency, slippage, feature drift, signal drift, reconciliation, risk breaches, and promotion to small live capital.
---

# Paper Trading Review Workflow

## Purpose

Paper trading tests the system, not just the signal. It should reveal live data, execution, latency, reconciliation, and operational gaps.

## Required Checks

- live feature values vs backtest feature values;
- intended orders vs submitted orders;
- submitted orders vs accepted/rejected orders;
- simulated fills vs paper/exchange fills;
- latency distribution;
- slippage distribution;
- order cancel/replace behavior;
- risk rejections;
- reconciliation differences;
- incident log.

## Output Standard

1. Paper-trading period
2. Strategy/config
3. Live-vs-sim drift
4. Execution diagnostics
5. Data diagnostics
6. Risk diagnostics
7. Incidents
8. Promotion verdict

