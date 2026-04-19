# Simons-Lens Quant Examples

## Example 1 - Correlation Network Regime

Idea:

```text
Crypto market structure changes when the correlation network becomes more concentrated.
```

Observable:

- rolling correlation matrix;
- top eigenvalue share;
- network centrality;
- clustering coefficient;
- dispersion of pairwise correlations.

Test:

```text
When top eigenvalue share jumps above its 90th percentile,
do residual stat-arb signals decay faster over the next 24 hours
than during normal correlation regimes?
```

Baseline:

- realized volatility regime;
- BTC beta;
- simple market-wide drawdown state.

## Example 2 - Topological Market State

Idea:

```text
Persistent homology detects regime transitions.
```

Required translation:

- define point cloud from asset returns or factor loadings;
- choose distance metric;
- compute persistence summary;
- map summary to future volatility, correlation, or strategy degradation;
- compare to PCA eigenvalue and volatility baselines.

Reject if topology does not beat cheaper baselines.

## Example 3 - Weak Signal Combination

If 30 weak alphas each barely pass a signal test, do not immediately combine them.

Require:

- pairwise signal correlation;
- shared risk exposure;
- turnover overlap;
- cost interaction;
- combined portfolio test;
- degradation estimate for live execution.

