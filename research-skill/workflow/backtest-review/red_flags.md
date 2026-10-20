# Backtest Review Red Flags

## Critical Red Flags

These usually invalidate the backtest immediately.

### 1. Same-Bar Look-Ahead

The strategy computes a signal using close price at time `t` and earns return from `t-1` to `t`.

Correct rule:

```text
signal_t can only affect position after signal_t is observable.
```

---

### 2. Position Not Lagged

Bad:

```text
pnl_t = signal_t * return_t
```

Usually correct:

```text
pnl_t = signal_{t-1} * return_t
```

unless the execution model explicitly justifies same-bar execution.

---

### 3. No Costs for High-Turnover Strategy

If turnover is high and costs are ignored, the backtest is fantasy.

---

### 4. Market Orders Filled at Mid

Market buys pay the ask. Market sells hit the bid.

Filling all market orders at mid without spread cost is usually invalid.

---

### 5. Limit Orders Always Filled

A limit order touching the price does not guarantee fill.

Need at least one of:

- conservative fill rule
- queue model
- volume model
- partial fill model
- empirical fill-rate estimate

---

### 6. Parameter Search on Forward Test

If forward data influenced parameter choice, it is no longer forward data.

---

### 7. Survivorship Bias

Using today's universe for historical testing can create fake alpha.

For crypto, this means ignoring delisted/dead coins or only testing assets that survived and became liquid.

---

### 8. Wrong Annualization

Crypto trades 24/7. US equities do not.

Using `sqrt(252)` for hourly crypto returns is wrong.

---

### 9. PnL Unit Error

Common mistakes:

- treating USD notional as quantity
- ignoring contract multiplier
- confusing base and quote currency
- using percent return with quantity position
- applying fee to PnL instead of traded notional

---

### 10. PnL Comes From One Trade

A strategy that makes all money from one or two events is not statistically reliable.

---

## Medium Red Flags

### 1. Parameter Heatmap Has One Spike

If only one exact parameter works, assume overfitting.

---

### 2. Sharpe Drops Sharply After Small Cost Increase

If 2x cost destroys performance, the strategy is fragile.

---

### 3. Strategy Works Only in One Regime

This is not always fatal, but the strategy needs regime detection or strict deployment rules.

---

### 4. High Turnover With Slow Signal

If signal horizon is long but turnover is high, the implementation may be unstable or over-reactive.

---

### 5. Unrealistic Capacity

If the strategy requires trading a large fraction of market volume, performance is overstated.

---

### 6. No Trade-Level Analysis

Aggregate Sharpe hides execution, concentration, and tail problems.

---

### 7. No Drawdown Autopsy

If you do not know why the strategy lost money in its worst period, you do not understand the strategy.

---

## Subtle Red Flags

### 1. Forward Fill Leakage

Forward-filling fundamental, funding, or index membership data can leak information if timestamps are not handled carefully.

---

### 2. Resampling Ambiguity

A bar labeled `10:00` may represent:

- 09:59-10:00
- 10:00-10:01
- 10:00-10:59
- 09:00-10:00

This matters for signal timing.

---

### 3. Cross-Sectional Normalization Leakage

At time `t`, z-scores should use only assets known and tradable at time `t`.

---

### 4. Rebalance Price Ambiguity

If the signal is calculated on close and rebalance is also at close, you need an explicit closing auction assumption.

For crypto, there is usually no single closing auction.

---

### 5. Hidden Leverage

Dollar-neutral does not mean low risk.

A portfolio can be net zero but gross 10x leveraged.

---

### 6. Ignoring Funding on Perpetuals

For crypto perpetual futures, funding can dominate PnL for some strategies.

---

### 7. Ignoring Borrow Constraints on Shorts

For equity or spot shorting, borrow availability and borrow cost matter.

---

### 8. Unrealistic Reinvestment

Compounding assumes capital can be scaled smoothly. This may be false under liquidity constraints.

---

## Blunt Reviewer Language

Use direct language when needed:

```text
This result is not trustworthy because the PnL uses current target position against current returns.
```

```text
The Sharpe ratio is meaningless until costs, spread, and position timing are fixed.
```

```text
This is a research sketch, not a backtest.
```

```text
The edge may exist, but this implementation has not proven it.
```

```text
The result is probably overfit because the parameter surface has one isolated peak and forward performance is poor.
```
