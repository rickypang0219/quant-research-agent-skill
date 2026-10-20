---
name: ng
description: Use for machine-learning alpha research, supervised learning, feature engineering, target design, train/validation/test discipline, leakage control, baseline models, representation learning, model iteration, error analysis, and deployment-aware ML workflows for quant trading.
---

# Andrew Ng Lens for Quant ML

## Scope

Use this lens when a trading idea involves machine learning: supervised alpha models, classification/regression targets, representation learning, feature stores, model selection, cross-validation, error analysis, or production ML pipelines.

The goal is not to add ML glamour. The goal is to turn a market question into a measurable prediction task, then test whether the model adds information after costs, risk, and realistic execution.

## Source Basis

Prefer:

- Andrew Ng's practical ML discipline: clear problem definition, simple baselines, error analysis, data-centric iteration, and train/dev/test hygiene.
- Lopez de Prado and Bailey for financial ML overfitting, purging, embargo, Deflated Sharpe, and probability of backtest overfitting.
- Hastie, Tibshirani, and Friedman for statistical learning foundations.
- Fama-French, Carhart, Asness-Moskowitz-Pedersen, and Lo for financial baselines and adaptive-market realism.
- Official material from Citadel/Citadel Securities, Jane Street, D. E. Shaw, Tower Research, and similar firms only as evidence of engineering/research standards, not as proof that a model class works.

## Core Rule

Most ML alpha failures are not model failures. They are problem-definition failures:

- the label is not tradable;
- features leak future data;
- cross-validation ignores time and overlap;
- the baseline is too weak;
- costs destroy the edge;
- the model learns beta, volatility, funding, or liquidity exposure;
- the strategy cannot execute at the assumed horizon.

## Required Framing

Every ML alpha task must specify:

- universe and asset eligibility at each timestamp;
- prediction horizon;
- label formula;
- decision time and execution time;
- feature timestamp and lag convention;
- baseline model;
- train/validation/test or walk-forward split;
- objective metric;
- cost/slippage/funding model;
- conversion from prediction to position;
- risk constraints;
- rejection rule.

## Label Design

Prefer labels that map directly to decisions:

```text
forward_return = log(price_{t+h} / price_t)
cost_adjusted_return = forward_return - expected_cost_t
direction_label = 1[cost_adjusted_return > threshold]
rank_label = cross_sectional_rank(forward_return_{t:t+h})
fill_label = 1[passive_order_filled_before_cancel]
adverse_selection_label = mid_{t+h} - fill_price
```

Bad labels:

- same-bar close-to-close return when the close is used as a feature;
- future realized volatility used without execution relevance;
- labels that select survivors after the fact;
- labels that ignore fees for high-turnover signals.

## Baseline Ladder

Before using complex models, require these baselines where applicable:

1. Zero prediction / no-trade baseline.
2. Market beta or BTC beta.
3. Momentum/reversal baseline at the same horizon.
4. Volatility/liquidity/funding baseline.
5. Linear/logistic regression.
6. Regularized linear model.
7. Gradient-boosted trees.
8. Neural model only after simpler models expose a real limitation.

If the model cannot beat a properly lagged, cost-aware simple baseline, stop.

## Validation Discipline

For time-series or panel financial data:

- use walk-forward splits;
- purge overlapping labels;
- embargo near split boundaries;
- never normalize using future data;
- fit scalers/encoders/neutralizers only on training windows;
- keep a final test set untouched;
- track every trial and hyperparameter search;
- evaluate by regime, asset, venue, liquidity bucket, and time period.

## Error Analysis

Do not only report aggregate AUC, R2, or Sharpe. Inspect:

- predictions by decile/bucket;
- calibration curve;
- turnover by prediction bucket;
- average cost by bucket;
- exposure to beta, sector, volatility, funding, liquidity, and size;
- tail days and drawdown days;
- false positives that cause large losses;
- periods where the model flips sign.

## Quant Dev Expectations

ML research code should produce:

- immutable training config;
- dataset manifest and schema;
- feature-generation code with tests;
- train/validation/test split artifact;
- model card with label, features, metrics, limitations, and known risks;
- reproducible prediction table;
- backtest that consumes predictions without leakage;
- monitoring hooks for feature drift, prediction drift, realized PnL, and live-vs-backtest slippage.

## Standard Output

When answering ML alpha questions, use:

1. Prediction task
2. Label
3. Feature set
4. Leakage risks
5. Baseline models
6. Validation protocol
7. Metrics and diagnostics
8. Strategy conversion
9. Failure modes
10. Minimal experiment

