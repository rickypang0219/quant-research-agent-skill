# Gilbert Strang Mental Models for Quant Research

## 1. Projection Is the Core Move

Regression, neutralization, PCA residuals, and factor models are all projection problems. Always ask:

- What space are we projecting onto?
- What is the residual?
- Is the residual the intended tradable object?
- Which inner product or weighting scheme defines the projection?

## 2. Dimensions Prevent Many Bugs

Before coding matrix operations, write dimensions:

```text
R: T x N returns
X: T x K factor returns
B: N x K asset loadings
W: N x 1 portfolio weights
```

Most quant bugs are silent dimension or index-alignment bugs.

## 3. Covariance Is an Operator, Not Just a Table

Covariance maps portfolios to risk. Its eigenvectors define risk directions; unstable small eigenvalues can create fake precision and unstable optimizers.

## 4. Residual Means "Orthogonal Under Assumptions"

A residual is only orthogonal to the fitted factor space under the sample, weighting, and model specification. It is not automatically alpha.

## 5. Shrinkage Is Humility

Sample covariance and beta estimates are noisy. Shrinkage is not cosmetic; it is a defense against overconfident optimization.

## 6. Numerical Stability Is Research Integrity

Ill-conditioned matrices, nearly collinear factors, unstable PCA ranks, and inverted noisy covariance matrices can manufacture strategies that disappear out-of-sample.

