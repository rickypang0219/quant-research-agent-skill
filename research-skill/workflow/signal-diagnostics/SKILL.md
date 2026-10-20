---
name: signal-diagnostics
description: Use after feature construction and before full backtesting to test whether a signal contains information using IC, rank IC, bucket tests, monotonicity, horizon decay, turnover, factor exposure, cost-adjusted expected return, and regime stability.
---

# Signal Diagnostics Workflow

## Purpose

Test the signal before dressing it up as a strategy. This workflow asks whether the feature has information at all.

## Core Rule

A feature is not a strategy. Prove the signal has cost-aware predictive content before portfolio construction.

## Required Diagnostics

- forward-return horizon scan;
- Pearson IC and Spearman rank IC;
- bucket/decile forward returns;
- monotonicity by score bucket;
- hit rate by bucket;
- signal autocorrelation and turnover implication;
- factor/beta/volatility/funding exposure;
- performance by regime;
- cost-adjusted expected return;
- capacity/liquidity screen;
- stability across assets and time.

## Output Standard

1. Signal definition
2. Target definition
3. Timing/lag convention
4. Baselines
5. Diagnostics
6. Cost-aware interpretation
7. Failure modes
8. Verdict: reject, refine, backtest

