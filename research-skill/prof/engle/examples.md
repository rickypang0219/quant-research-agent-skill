# Engle Lens Examples

## Example 1 - Volatility Targeting

Bad:

```text
Use 2x leverage because Sharpe is high.
```

Better:

```text
Estimate ex-ante volatility with EWMA/GARCH using only past returns. Scale position so forecast daily volatility contribution is capped, then stress realized volatility 2x.
```

## Example 2 - Volatility Forecast Validation

Compare:

- rolling realized volatility;
- EWMA;
- GARCH(1,1);
- regime-conditioned estimator.

Metrics:

- QLIKE loss;
- exceedance count;
- VaR breach clustering;
- drawdown under forecast error.

## Example 3 - Alpha Confounded by Volatility

If a strategy earns money only in low-volatility regimes, its "alpha" may be a volatility state exposure.

Test:

```text
Sort returns by realized volatility bucket and report PnL, turnover, hit rate, and drawdown by bucket.
```

