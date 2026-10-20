# Professor Router for Idea-to-Hypothesis

Use professor modules as reasoning engines.

## Strang

Use when the idea involves:

- linear algebra
- PCA
- SVD
- projections
- factor models
- residuals
- covariance
- correlation
- Hilbert space
- vector geometry
- least squares
- linear constraints
- neutralization
- numerical modeling

Strang should answer:

```text
What is the mathematical structure?
What is the vector space?
What is being projected onto what?
What is signal and what is residual?
Is the linear algebra correct?
Are the dimensions correct?
Is the estimator stable?
```

## Lo

Use when the idea involves:

- financial economics
- Adaptive Markets Hypothesis
- market efficiency
- behavioral adaptation
- risk management
- systemic risk
- hedge funds
- crowding
- regime adaptation
- AI in finance
- market sense
- empirical finance

Lo should answer:

```text
Why should this edge exist in markets?
Who adapts?
When does the edge decay?
What are the risk and behavioral explanations?
Is this a risk premium or mispricing?
Is the strategy exposed to crowding or systemic unwind?
```

## Brunton

Use when the idea involves:

- dynamical systems
- SINDy
- DMD
- Koopman theory
- state-space modeling
- sparse discovery
- regime dynamics
- control
- high-dimensional systems
- reduced-order modeling
- nonlinear dynamics
- data-driven discovery of governing equations

Brunton should answer:

```text
What are the state variables?
Can we discover governing dynamics?
Is there a low-dimensional representation?
Can we model regime transition?
Can we use sparse dynamics?
Can we control or stabilize the system?
```

## Simons

Use when the idea involves:

- statistical arbitrage
- empirical testing
- hidden structure
- signal validation
- scientific alpha discovery
- market state topology
- invariants
- pattern discovery
- research culture
- production research discipline

Simons should answer:

```text
Can this be tested?
Is the signal statistically real?
Is it robust?
Can it survive costs?
What would kill the idea?
Is this hidden structure or just noise?
How do we design the cleanest experiment?
```

## Quant Trading System

Use when the idea needs implementation.

It should answer:

```text
Can this be prototyped in Python?
Can it be paper traded?
What needs Rust productionization?
What can fail in live execution?
How do we monitor it?
How do we handle errors, missing data, and network failures?
```

## Combined Routing Examples

### PCA Residual Mean Reversion

Use:

```text
Strang + Lo + Simons
```

Reason:

- Strang: PCA, projections, residuals, factor neutralization
- Lo: market efficiency, adaptive decay, risk interpretation
- Simons: statistical testing, robustness, signal validation

### Regime Detection with DMD / SINDy

Use:

```text
Brunton + Lo + Simons
```

Reason:

- Brunton: state variables, low-dimensional dynamics, sparse governing equations
- Lo: adaptive market regimes and risk
- Simons: empirical validation and robustness

### Market Microstructure Signal

Use:

```text
Lo + Simons + Quant Trading System
```

Reason:

- Lo: liquidity, risk, market ecology
- Simons: signal testing and overfitting control
- Quant Trading System: latency, execution, order book handling, monitoring

### Abstract Mathematical Analogy

Use:

```text
Strang + Brunton + Simons
```

Reason:

- Strang: convert analogy into math
- Brunton: convert math into dynamics or state variables
- Simons: force the idea into measurable, falsifiable tests
