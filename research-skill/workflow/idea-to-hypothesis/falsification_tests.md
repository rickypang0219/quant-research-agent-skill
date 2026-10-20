# Falsification Tests

For every idea, try to kill it before building it.

The assistant should be adversarial but useful. The goal is not to prove that the idea works. The goal is to discover whether the idea survives contact with data.

## Basic Tests

### 1. Shuffle Test

Randomly shuffle future returns.

Expected result:

```text
The signal should disappear.
```

If performance remains strong after shuffling, the backtest likely has leakage or a bug.

### 2. Lag Test

Shift the signal forward incorrectly.

Expected result:

```text
Performance should disappear.
```

If it does not disappear, check timestamp alignment and lookahead bias.

### 3. Cost Stress Test

Double or triple transaction costs.

Expected result:

```text
The strategy should degrade but not become obviously impossible if the edge is real and large enough.
```

For high-turnover strategies, this is often the fastest way to kill weak ideas.

### 4. Subperiod Test

Test across bull, bear, sideways, high-volatility, low-volatility, crisis, and exchange-specific abnormal periods.

Expected result:

```text
The signal should either survive broadly or have a clearly explainable regime dependency.
```

### 5. Universe Test

Check whether the edge exists outside the original asset universe.

Examples:

- top 10 coins
- top 50 coins
- excluding BTC and ETH
- excluding illiquid coins
- spot only
- perpetual futures only

Expected result:

```text
The signal should not depend on one cherry-picked subset unless the mechanism explains why.
```

### 6. Horizon Test

Check whether the effect is stable across different prediction horizons.

Example horizons:

```text
1 bar
4 bars
12 bars
24 bars
3 days
1 week
```

Expected result:

```text
The signal should have a plausible decay curve.
```

### 7. Risk-Factor Test

Regress returns against obvious risk factors:

- BTC return
- ETH return
- market return
- momentum factor
- volatility factor
- liquidity factor
- funding factor
- size / market cap factor
- carry factor

Expected result:

```text
The alpha should not disappear completely after controlling for obvious risk factors, unless the strategy is intentionally harvesting that risk premium.
```

### 8. Turnover Test

Check whether profits are only from unrealistic rebalancing.

Metrics:

- average daily turnover
- turnover per rebalance
- average holding period
- fee drag
- slippage drag
- order count
- notional traded

Expected result:

```text
The strategy should remain plausible after realistic turnover constraints.
```

### 9. Liquidity Test

Remove assets with poor volume or wide spread.

Possible filters:

- minimum daily volume
- minimum order book depth
- maximum bid-ask spread
- maximum market impact estimate
- minimum listing age

Expected result:

```text
Performance should not depend entirely on assets that cannot be traded realistically.
```

### 10. Capacity Test

Estimate whether trade size destroys the edge.

Questions:

- What is the expected alpha per trade?
- What is the expected spread cost?
- What is the estimated market impact?
- How much depth exists at target size?
- How much can be traded before alpha turns negative?

Expected result:

```text
The strategy should have a realistic capacity estimate before live trading.
```

## Additional Tests

### 11. Baseline Test

Compare against simple baselines:

- buy and hold BTC
- equal-weight portfolio
- volatility-scaled portfolio
- simple momentum
- simple mean reversion
- random long/short with same turnover
- factor-neutral random basket

### 12. Parameter Sensitivity Test

Perturb important parameters:

- lookback window
- z-score threshold
- rebalance frequency
- holding period
- volatility window
- number of assets
- PCA components
- stop-loss / take-profit thresholds

Expected result:

```text
The result should not depend on one fragile parameter choice.
```

### 13. Walk-Forward Test

Use rolling train/test periods.

Expected result:

```text
Parameters selected in the training window should retain some performance in the test window.
```

### 14. Embargo / Purging Test

For overlapping labels, purge nearby training samples and apply an embargo.

Expected result:

```text
Performance should survive after reducing label leakage.
```

### 15. Execution Realism Test

Replace ideal fills with conservative assumptions:

- next-bar open fill
- bid/ask spread
- taker fees
- maker fees with fill probability
- partial fills
- slippage
- rejected orders
- delayed orders

Expected result:

```text
The strategy should not rely on impossible fills.
```

## Common Reasons Ideas Fail

- The signal is just beta.
- The signal is just volatility exposure.
- The signal is just momentum in disguise.
- The signal only works before fees.
- The signal only works during one market regime.
- The signal uses future information.
- The signal is too slow for live trading.
- The signal is too noisy for position sizing.
- The signal cannot be traded at available liquidity.
- The signal is overfit.
- The signal disappears after simple risk neutralization.
- The signal is caused by bad timestamps.
- The signal requires unavailable historical data.
