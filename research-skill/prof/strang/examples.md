# Strang-Lens Quant Examples

## Example 1 - Factor Neutralization

Problem:

```text
Given raw signal s over N assets, remove exposure to K risk factors.
```

Objects:

```text
s: N x 1
B: N x K factor loading matrix
W: N x N diagonal asset weights or liquidity weights
```

Weighted projection:

```text
s_neutral = s - B (B' W B)^(-1) B' W s
```

Review questions:

- Are factors known at the decision time?
- Is `B' W B` well-conditioned?
- Does neutralization destroy most of the signal?
- Does turnover explode after neutralization?

## Example 2 - PCA Stat Arb

Objects:

```text
R: T x N standardized returns
V_k: N x k top PCA eigenvectors
f_t = R_t V_k
residual_t = R_t - f_t V_k'
```

Failure modes:

- PCA fit includes future data;
- unstable eigenvectors;
- too many components remove alpha;
- too few components leave beta exposure;
- residual is not mean-reverting after costs.

## Example 3 - Covariance Optimizer Blow-Up

If small eigenvalues dominate `Sigma^{-1}`, the optimizer may create large long/short weights in nearly offsetting assets.

Fixes:

- shrink covariance;
- add gross/concentration constraints;
- cap leverage;
- use robust risk model;
- test parameter stability out-of-sample.

