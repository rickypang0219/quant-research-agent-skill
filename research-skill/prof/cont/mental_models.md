# Rama Cont Mental Models for Quant Research

## 1. Empirical Facts Before Elegant Processes

A stochastic process is a model of observed regularities. First inspect heavy tails, volatility clustering, jumps, dependence, and liquidity state; then choose the process.

## 2. Brownian Motion Is a Baseline, Not a Default Truth

Continuous diffusions are analytically convenient, but markets often show discontinuities, fat tails, and state-dependent liquidity. Brownian models need empirical justification.

## 3. Jumps Represent Missing Continuous-Time Smoothness

Large moves, news shocks, liquidation cascades, and gap risk are not small Gaussian increments. A jump model changes hedging, risk, and execution assumptions.

## 4. The Order Book Is a Queueing System

At micro horizons, price movement is produced by queue depletion and replenishment. The state is not only price; it is bid/ask depth, event intensities, cancellations, and order flow imbalance.

## 5. Order Flow Imbalance Is More Physical Than Signed Volume Alone

Signed volume ignores liquidity supply. OFI compares demand and supply changes at the best quotes and naturally links price changes to available depth.

## 6. Impact Is Conditional on Liquidity

The same trade size can have different impact depending on depth, spread, volatility, and time of day. Impact models without liquidity state are incomplete.

## 7. Path Functionals Must Be Non-Anticipative

Drawdown, realized volatility, barriers, trailing stops, and path-dependent signals must use only information available up to decision time.

## 8. Calibration Is Part of the Model

If parameters drift across assets or regimes, that is information. Report calibration stability, not just fitted values.

## 9. Model Risk Is Not a Disclaimer

Model risk changes sizing, stress tests, and kill switches. If the model misses jumps or liquidity shocks, risk limits must compensate.

## 10. Microstructure Theory Must Touch Execution

A good LOB model should answer at least one execution question:

- Will I fill?
- Will I be adversely selected?
- Will the queue deplete?
- Will impact exceed edge?
- How does latency change the answer?

