# Examples

These examples show how to apply the idea-to-hypothesis workflow to quant research ideas.

## Example 1 — Physics Analogy

### Raw Idea

> Ground-state quantum fluctuation is like mean return, and particle excitation is like non-zero stock return.

### Plain Market Translation

Returns may fluctuate around a latent equilibrium. Large deviations from equilibrium may represent market shocks, liquidity events, or regime excitations.

### Possible Observables

| Concept | Proxy |
|---|---|
| ground state | rolling mean return, fair value, VWAP, POC |
| fluctuation | residual return |
| excitation | return z-score above threshold |
| energy | realized volatility |
| regime | volatility/correlation state |

### Falsifiable Hypothesis

```text
When residual return exceeds 2 rolling standard deviations during low-volatility regimes,
future returns should mean-revert over the next H bars more often than the unconditional baseline.
```

### Null Hypothesis

```text
Large residual returns do not predict future returns after fees and slippage.
```

### Minimum Test

```text
Compute residual z-score.
Bucket events by z-score.
Measure forward return over 1, 4, 12, and 24 bars.
Compare against unconditional forward return.
Include fees.
```

### Decision

```text
TEST
```

Reason:

The physics analogy is not directly tradable, but it can be converted into measurable residual deviation, volatility regime, and forward-return tests.

## Example 2 — PCA Residual Mean Reversion

### Raw Idea

> Coins deviate from the crypto market factor and revert.

### Professor Routing

| Module | Role |
|---|---|
| Strang | PCA, projection, residuals, factor-neutral returns |
| Lo | Adaptive Markets, risk, crowding, regime decay |
| Simons | empirical validation, signal testing, robustness |

### Falsifiable Hypothesis

```text
When an asset's PCA residual s-score is above +2,
the asset should underperform the factor-hedged basket over the next 24 hours.

When an asset's PCA residual s-score is below -2,
the asset should outperform the factor-hedged basket over the next 24 hours.
```

### Null Hypothesis

```text
PCA residual s-score has no predictive power after fees, slippage, and beta neutralization.
```

### Minimum Experiment

```text
Universe: top 50 liquid coins
Bar: 1h
PCA window: 180 days
Residual model: AR(1)
Signal: s-score
Target: factor-neutral forward return
Validation: walk-forward
```

### Failure Modes

1. The signal is just BTC beta.
2. Residuals are not stationary.
3. The half-life is too long.
4. Turnover destroys the edge.
5. PCA loadings are unstable in crisis regimes.

### Decision

```text
TEST
```

## Example 3 — Order Book Imbalance

### Raw Idea

> If bid depth is much larger than ask depth, price should go up.

### Plain Market Translation

A positive order-book imbalance may indicate short-term buying pressure or liquidity support.

### Observable Variables

| Concept | Proxy |
|---|---|
| bid pressure | bid depth at top N levels |
| ask pressure | ask depth at top N levels |
| imbalance | (bid_depth - ask_depth) / (bid_depth + ask_depth) |
| future movement | next 1s, 5s, 30s, or 1m return |

### Falsifiable Hypothesis

```text
When top-10 order-book imbalance is above the 90th percentile,
next-30-second midprice return should be positive after fees and spread,
relative to unconditional next-30-second return.
```

### Null Hypothesis

```text
Order-book imbalance has no predictive power after spread, fees, and adverse selection.
```

### Minimum Test

```text
Data: L2 order book snapshots and trades
Feature: top-N imbalance
Target: future midprice return
Horizon: 1s, 5s, 30s, 1m
Metric: bucketed forward return and hit rate
Cost: spread + taker/maker fee + slippage
```

### Failure Modes

1. Queue position is not modeled.
2. Signal decays faster than execution latency.
3. Spoofing or fleeting liquidity contaminates the feature.
4. Edge exists only before fees.
5. Historical snapshots are not realistic enough.

### Decision

```text
REFINE
```

Reason:

The idea is testable, but before backtesting, the execution assumption must be clarified: taker execution, maker execution, or midprice prediction only.

## Example 4 — Funding Rate Mean Reversion

### Raw Idea

> When funding is extremely positive, the market is overcrowded long and should reverse.

### Plain Market Translation

High positive funding may indicate crowded long positioning in perpetual futures. If the crowd is overextended, future returns may be negative or volatility may rise.

### Observable Variables

| Concept | Proxy |
|---|---|
| long crowding | positive funding rate z-score |
| crowdedness | funding percentile over rolling window |
| unwind | negative future return or liquidation spike |
| carry | funding collected or paid |
| market regime | realized volatility and BTC trend |

### Falsifiable Hypothesis

```text
When funding-rate z-score is above +2
and BTC trend is flat or negative,
the next 24-hour return should be lower than baseline
after accounting for funding and transaction costs.
```

### Null Hypothesis

```text
Funding rate does not predict future returns after controlling for momentum, volatility, and market beta.
```

### Minimum Test

```text
Universe: liquid perpetual futures
Feature: funding z-score
Target: next 8h / 24h return
Controls: BTC return, volatility, momentum
Validation: subperiod and regime split
```

### Failure Modes

1. Positive funding is compensation for momentum, not reversal.
2. Shorting high-funding assets loses money during strong bull trends.
3. Funding data timing is misaligned.
4. Borrowing, margin, or liquidation risk is ignored.
5. The signal is exchange-specific.

### Decision

```text
TEST
```

## Example 5 — Regime Shift from PCA Eigenvalues

### Raw Idea

> When the first PCA eigenvalue spikes, the market becomes one-dimensional and diversification breaks.

### Professor Routing

| Module | Role |
|---|---|
| Strang | eigenvalues, covariance, PCA interpretation |
| Lo | systemic risk, crowding, market adaptation |
| Brunton | regime dynamics and state variables |
| Simons | empirical stress testing |

### Observable Variables

| Concept | Proxy |
|---|---|
| market one-dimensionality | first eigenvalue / total eigenvalue sum |
| correlation spike | average pairwise correlation |
| diversification collapse | realized portfolio volatility |
| regime shift | change point in eigenvalue ratio |

### Falsifiable Hypothesis

```text
When the first PCA eigenvalue share rises above its 95th percentile,
cross-sectional stat-arb residual signals should weaken,
and portfolio drawdown risk should increase over the next 24 to 72 hours.
```

### Null Hypothesis

```text
PCA eigenvalue concentration does not predict future strategy drawdown or residual signal decay.
```

### Minimum Test

```text
Compute rolling PCA eigenvalue share.
Bucket periods by eigenvalue concentration.
Measure next 24h/72h strategy returns, drawdowns, and residual mean-reversion strength.
Compare against baseline.
```

### Failure Modes

1. Eigenvalue spike is contemporaneous, not predictive.
2. The signal is just realized volatility.
3. The PCA window is too slow.
4. The result only appears in crisis periods.
5. It helps risk control but not alpha generation.

### Decision

```text
TEST
```
