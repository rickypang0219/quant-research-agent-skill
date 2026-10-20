# Rama Cont Lens Examples

## Example 1 - Stylized Facts Before Model Choice

Bad formulation:

```text
Assume BTC returns follow geometric Brownian motion and price options.
```

Cont-style formulation:

```text
First measure BTC return tails, volatility clustering, jump frequency, intraday seasonality, and liquidity state. Use GBM only as a baseline. If tails/jumps dominate, compare jump-diffusion or Levy-style models and test calibration stability.
```

Minimal test:

- QQ plot vs Gaussian;
- tail quantiles;
- return autocorrelation;
- absolute return autocorrelation;
- realized volatility persistence;
- event study for large returns.

## Example 2 - OFI as a Short-Horizon Price Feature

Hypothesis:

```text
At short horizons, mid-price changes are better explained by order flow imbalance scaled by available depth than by signed trade volume alone.
```

Observable:

```text
OFI_t = change in demand at best bid - change in supply at best ask
```

Test:

```text
Delta mid over [t, t+h] = beta * OFI_bucket / depth_bucket + error
```

Compare:

- OFI regression;
- signed volume regression;
- imbalance-only baseline;
- no-feature baseline.

Failure modes:

- bad book reconstruction;
- event ordering errors;
- crossed/locked books;
- latency;
- unstable coefficients by regime;
- fees/spread consume the edge.

## Example 3 - Limit Order Book as Queue Model

Question:

```text
If I join the best bid, what is the probability my order fills before the mid-price moves down?
```

State:

- bid queue size;
- ask queue size;
- market order arrival intensity;
- limit order arrival intensity;
- cancel intensity;
- position in queue if available;
- spread and volatility state.

Output:

- fill probability;
- adverse-selection probability;
- expected realized spread;
- cancel threshold.

Do not claim queue-position accuracy from L2 snapshots unless queue position is modeled as latent and stress-tested.

## Example 4 - Jump Risk in Backtest Review

If a mean-reversion strategy has smooth profits but rare large losses, ask:

- Are large moves modeled as jumps or Gaussian tails?
- Does stop-loss execution assume impossible liquidity?
- What happens when spread widens 5x?
- Is liquidation distance enough under a gap?
- Does the strategy short volatility or liquidity?

Verdict:

```text
The strategy may be selling jump/liquidity risk. Sharpe is not meaningful until jump scenarios and execution stress are included.
```

