# Steven Shreve Mental Models for Quant Research

## 1. Filtration Is the Anti-Lookahead Device

In code, "no leakage" means the trading decision is measurable with respect to the information available at that time.

## 2. Martingale Measure Is Not Market Belief

Risk-neutral probabilities price claims; physical probabilities describe real-world dynamics. Confusing them creates bad alpha claims and bad risk estimates.

## 3. Self-Financing Is an Accounting Constraint

A trading strategy must specify how position changes are funded. PnL cannot appear from rebalancing algebra.

## 4. Binomial Trees Are Not Toy Models

They expose the core logic of replication, state prices, dynamic hedging, American exercise, and backward induction before continuous-time notation obscures it.

## 5. Ito's Formula Is Quadratic-Variation Accounting

The second-order term is not optional. Gamma, realized variance, hedging error, and volatility exposure all flow from quadratic variation.

## 6. SDEs Need Existence, Uniqueness, and Interpretation

Before simulating:

- Are coefficients adapted?
- Are they Lipschitz or otherwise well-posed?
- Is the solution strong or weak?
- Is the numerical scheme stable?
- Does the process stay in the valid state space?

## 7. Control Problems Need State, Control, and Objective

Sizing, execution, and liquidation are not fully specified until state variables, admissible controls, objective, constraints, and terminal conditions are written.

## 8. Transaction Costs Create Regions, Not Points

With costs, continuous rebalancing becomes impossible. Optimal policies often have no-trade regions, impulse controls, or singular controls rather than exact target weights.

## 9. Heavy Traffic Turns Queues Into Diffusions

Discrete event systems can have diffusion approximations under scaling limits. This is useful for market microstructure only if the scaling assumptions match the venue/data.

## 10. Mathematical Elegance Must Survive Discretization

Continuous-time results must be translated into discrete decisions, finite liquidity, tick sizes, fees, latency, and numerical error before they become trading systems.

