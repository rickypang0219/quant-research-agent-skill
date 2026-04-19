---
name: shreve
description: Use for stochastic-process and mathematical-finance questions involving martingales, Brownian motion, stochastic calculus, Ito integrals, SDEs, risk-neutral pricing, equivalent martingale measures, no-arbitrage, binomial-to-continuous-time reasoning, stochastic control, utility maximization, transaction costs, optimal execution, and diffusion approximations.
---

# Steven Shreve Lens for Stochastic Calculus and Mathematical Finance

> Status: curated synthesis from public academic and official sources, not a literal exhaustive archive of every message, interview, conference talk, paper, lecture, or opinion.

## Scope

Use this lens when a quant problem requires rigorous stochastic-process foundations:

- martingales and filtrations;
- stopping times;
- Brownian motion;
- Ito integration and Ito's formula;
- stochastic differential equations;
- Girsanov change of measure;
- risk-neutral pricing;
- complete and incomplete markets;
- binomial model as a discrete foundation;
- stochastic control;
- utility maximization;
- transaction costs;
- optimal execution;
- diffusion approximations for queues/order books.

## Core Doctrine

Write the probability space before writing the trading formula.

```text
state space -> filtration -> admissible information -> process dynamics -> pricing/control objective -> theorem/algorithm -> implementation check
```

The Shreve-style discipline is to make the information structure explicit. A strategy cannot trade on information outside its filtration.

## Operating Principles

### 1. Filtration is the mathematical form of no lookahead

For any signal or strategy, define:

```text
F_t = information available at decision time t
```

A valid position must be predictable or at least adapted to the correct filtration. If a feature uses future data, it is not merely a bug; it violates the stochastic model.

### 2. Martingales encode fair games under the right measure

Risk-neutral pricing is not a forecast of real returns. It is a no-arbitrage valuation method under an equivalent martingale measure.

Always distinguish:

- physical measure `P`;
- pricing/risk-neutral measure `Q`;
- historical estimation;
- option-implied calibration;
- trading alpha under `P`;
- replication/pricing under `Q`.

### 3. Discrete models teach the continuous model

Use the binomial model to clarify:

- self-financing portfolios;
- state prices;
- replication;
- American exercise;
- dynamic programming;
- convergence intuition toward Brownian models.

Do not jump to continuous time if the discrete-time information and cash-flow accounting are unclear.

### 4. Ito calculus is a bookkeeping rule for stochastic paths

For `dS_t = mu_t S_t dt + sigma_t S_t dW_t`, remember that quadratic variation creates the second-derivative term in Ito's formula.

In trading terms:

- delta hedging error;
- gamma exposure;
- realized variance;
- discretization error;
- transaction costs.

### 5. Stochastic control is about admissible decisions

For sizing, liquidation, execution, and utility maximization, define:

- state variables;
- controls;
- admissibility constraints;
- objective;
- terminal condition;
- dynamic programming equation or verification argument.

If these are missing, the control problem is not specified.

### 6. Transaction costs change the theorem

Frictionless no-arbitrage results do not carry over unchanged when there are spreads, fees, market impact, or position constraints. With transaction costs, ask about:

- solvency region;
- no-trade region;
- shadow price;
- utility loss;
- execution schedule;
- liquidity risk.

## Quant Research Translation

When applying this lens, produce:

1. Probability space and filtration
2. State process
3. Control/trading decision
4. Objective or pricing claim
5. Measure: physical `P` or risk-neutral `Q`
6. Admissibility constraints
7. Discrete-time implementation
8. Numerical method
9. Failure modes

## Standard Use Cases

- Check whether a backtest has lookahead bias using filtration language.
- Explain risk-neutral vs physical probability.
- Derive a binomial or Black-Scholes pricing argument.
- Build an SDE model and state the assumptions.
- Translate a sizing/execution problem into stochastic control.
- Review whether transaction costs invalidate a frictionless argument.
- Build diffusion approximations for high-frequency queue/order-book systems.

## Use With Other Skills

- Use `prof/cont` for jump processes, stylized facts, pathwise/functional Ito calculus, model risk, and order-flow/LOB stochastic modeling.
- Use `prof/strang` for covariance, factor projections, and numerical linear algebra.
- Use `domain/risk` for leverage, tail, liquidation, and stress controls.
- Use `workflow/backtest-review` to convert filtration logic into code-review checks.

