# Quant ML Examples

## Example 1 - Crypto Cross-Sectional Return Model

Bad formulation:

```text
Train XGBoost to predict top-50 crypto returns.
```

Better formulation:

```text
Universe:
    Top-50 crypto perpetuals by trailing 30-day dollar volume, recomputed using only historical data.

Label:
    4-hour forward return minus taker fee estimate and expected spread cost.

Features:
    lagged returns, realized volatility, funding rate, open interest change, volume shock, BTC beta, cross-sectional momentum/reversal, liquidity rank.

Split:
    Walk-forward monthly retrain, one-week embargo, final six months untouched.

Baseline:
    BTC beta + momentum/reversal + funding carry.

Decision:
    Long top decile, short bottom decile, beta-neutral, gross <= 1.0, per-asset cap 5%.
```

## Example 2 - LOB Fill Probability Model

Prediction task:

```text
Given order-book state at decision time t, predict whether a passive bid at best bid fills within 2 seconds before cancellation.
```

Features:

- queue size ahead proxy;
- order flow imbalance;
- trade-sign intensity;
- cancel intensity;
- spread;
- volatility;
- distance to mid;
- venue/session.

Failure modes:

- L2 data cannot identify true queue position;
- hidden/iceberg liquidity;
- cancel latency;
- exchange throttles;
- adverse-selection conditional on fill.

## Example 3 - Rejecting a Beautiful but Useless Model

If a model gets high AUC predicting next-bar direction but loses after costs, the verdict is:

```text
The classifier has statistical signal but not tradable signal. Continue only if bucketed expected return after cost is monotonic and robust out-of-sample.
```

