---
name: engle
description: Use for volatility econometrics, ARCH/GARCH, realized volatility, volatility forecasting, dynamic conditional correlation, V-Lab/SRISK style systemic risk, VaR/ES, volatility targeting, volatility clustering, and risk-model validation.
---

# Robert Engle Lens for Volatility Econometrics

## Scope

Use this lens when the task involves volatility or time-varying risk:

- ARCH/GARCH models;
- realized volatility;
- volatility clustering;
- volatility forecasting;
- dynamic conditional correlation;
- VaR and expected shortfall;
- volatility targeting;
- risk model validation;
- systemic risk measures such as SRISK;
- volatility regime diagnostics.

## Core Doctrine

Volatility is not constant. Treat it as a state variable that affects sizing, risk, execution cost, liquidation risk, and strategy decay.

```text
returns -> conditional volatility -> risk forecast -> sizing / limits / stress test
```

## Required Translation

Every volatility answer should specify:

- return series and sampling frequency;
- volatility estimator;
- forecast horizon;
- model class;
- training window;
- loss function;
- benchmark;
- risk decision affected.

## Quant Rules

- Do not annualize noisy high-frequency volatility without checking microstructure noise.
- A volatility target cannot use future volatility.
- Risk forecasts need backtests: exceedance tests, calibration, and regime slices.
- Volatility forecasts should be compared with simple baselines such as EWMA and realized volatility.
- Volatility is often the hidden driver of backtest performance.

## Standard Output

1. Volatility object
2. Model or estimator
3. Forecast horizon
4. Baseline
5. Validation test
6. Use in sizing/risk/execution
7. Failure modes

