# Signal Diagnostics Formulas

## Information Coefficient

```text
IC_t = corr(signal_{i,t}, forward_return_{i,t+h})
```

Use cross-sectional IC for cross-sectional signals and time-series IC for single-asset signals.

## Rank IC

```text
rank_IC_t = corr(rank(signal_{i,t}), rank(forward_return_{i,t+h}))
```

Rank IC is often more robust to outliers.

## Bucket Return

```text
bucket_return_{q,t} = mean(forward_return_{i,t+h} | signal_{i,t} in bucket q)
```

Check monotonicity. A signal whose middle buckets beat the extremes is suspicious.

## Decay Curve

```text
effect(h) = mean(sign(signal_t) * return_{t:t+h})
```

The holding period should match the signal decay, not be chosen after seeing PnL.

## Cost-Adjusted Expected Return

```text
net_edge = expected_forward_return - expected_fee - expected_spread - expected_slippage - expected_funding
```

