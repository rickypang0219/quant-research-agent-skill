# Andrew Ng Mental Models for Quant ML

## 1. ML Starts With the Label

If the target is vague, the model is irrelevant. In trading, the label must include horizon, timestamp, execution assumption, and cost relevance.

## 2. Data Quality Beats Model Cleverness

Bad timestamps, survivor-only universes, future-normalized features, and inconsistent corporate-action or funding treatment dominate architecture choices.

## 3. The Baseline Is the First Boss

The model must beat:

- no trade;
- beta/factor exposure;
- simple momentum/reversal;
- simple volatility/liquidity/funding rules;
- linear models.

If it cannot, complexity is hiding weakness.

## 4. Error Analysis Is More Useful Than Leaderboards

Find where the model fails:

- high volatility;
- low depth;
- funding spikes;
- exchange outages;
- major news;
- delistings;
- regime transitions.

Then decide whether the failure should be modeled, risk-limited, or used as a rejection reason.

## 5. Dev Set Is Not a Toy

The validation set drives iteration. If the user keeps tuning against it, it becomes training data. Keep a final untouched test period.

## 6. Feature Importance Is Not Causality

A feature can rank high because it proxies volatility, liquidity, beta, or timestamp artifacts. Always neutralize and stress by regime.

## 7. Prediction Is Not PnL

AUC, R2, and log loss do not pay fees. Convert predictions to positions and then evaluate turnover, costs, slippage, capacity, and risk.

