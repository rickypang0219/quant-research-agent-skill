# Gatheral Lens Examples

## Example 1 - Volatility Surface Sanity Check

Before using an implied-vol feature:

- check stale options;
- remove crossed markets;
- check moneyness and maturity definitions;
- test static arbitrage;
- compare to realized volatility and variance risk premium.

## Example 2 - Rough Volatility Claim

Bad:

```text
Crypto volatility is rough, so use a rough vol model.
```

Better:

```text
Estimate log-volatility scaling across intraday horizons. Compare Hurst exponent and forecast loss against EWMA/GARCH/realized-vol baselines.
```

## Example 3 - Market Impact Review

If a backtest uses temporary impact with fast exponential decay, check whether round-trip trading can generate expected profit.

Verdict:

```text
Reject the impact model until it satisfies no-dynamic-arbitrage consistency.
```

