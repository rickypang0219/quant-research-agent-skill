---
name: gatheral
description: Use for volatility surface, implied volatility, stochastic volatility, rough volatility, volatility microstructure, no-dynamic-arbitrage market impact, option pricing intuition, and execution-impact consistency.
---

# Jim Gatheral Lens for Volatility and Market Impact

## Scope

Use this lens for:

- implied volatility surfaces;
- volatility skew and term structure;
- stochastic volatility;
- rough volatility;
- option hedging diagnostics;
- variance risk premium;
- market impact shape and decay;
- no-dynamic-arbitrage constraints for impact models.

## Core Doctrine

Volatility and impact models must be internally consistent. A model that fits one slice but violates arbitrage or execution logic is not safe.

## Quant Rules

- Separate physical volatility forecasts from risk-neutral implied volatility.
- Check static arbitrage in option surfaces.
- Treat rough volatility as an empirical regularity to test, not a slogan.
- Impact decay and impact shape must be mutually consistent.
- Execution cost models should not permit profitable round-trip manipulation.

## Standard Output

1. Volatility or impact object
2. Measure: physical or risk-neutral
3. Model assumption
4. Arbitrage/consistency checks
5. Calibration data
6. Trading/risk implication
7. Failure modes

