---
name: robust-statistics
description: Use for robust statistics in quant research: outliers, heavy tails, robust regression, M-estimators, median/MAD, winsorization, robust covariance, influence functions, breakdown point, bootstrap, and contamination-resistant signal diagnostics.
---

# Robust Statistics Lens

## Scope

Use this lens when financial data is noisy, heavy-tailed, contaminated, or adversarial:

- outliers;
- bad ticks;
- liquidation spikes;
- robust regression;
- robust covariance;
- median/MAD scaling;
- winsorization/trimming;
- M-estimators;
- bootstrap under fat tails;
- influence diagnostics.

## Core Doctrine

Mean and variance are fragile. In finance, the outlier is often the point.

## Quant Rules

- Do not delete outliers without deciding whether they are data errors or genuine market risk.
- Report sensitivity to winsorization and robust scaling.
- Use median/MAD or robust z-scores when tails dominate.
- Check influence of top events on regression coefficients and Sharpe.
- Robust estimators reduce fragility, but can also hide crash risk if misused.

## Standard Output

1. Contamination/outlier risk
2. Robust estimator
3. Comparison to classical estimator
4. Influence diagnostics
5. Trading/risk consequence
6. Failure modes

