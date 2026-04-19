# Robust Statistics Examples

## Example 1 - Robust Z-Score

Classical:

```text
z = (x - mean(x)) / std(x)
```

Robust:

```text
z_robust = (x - median(x)) / (1.4826 * MAD(x))
```

Use when heavy tails or liquidation spikes distort mean/std.

## Example 2 - Regression Influence

If one crisis week creates the whole alpha estimate:

```text
Refit regression excluding top 1% absolute returns and compare coefficient sign, t-stat, and out-of-sample PnL.
```

Do not hide the crisis week. Report both versions.

## Example 3 - Robust Covariance

Portfolio optimization with sample covariance can be unstable. Compare:

- sample covariance;
- shrinkage covariance;
- robust covariance;
- factor covariance.

Then test turnover and realized drawdown.

