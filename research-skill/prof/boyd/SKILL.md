---
name: boyd
description: Use for convex optimization, portfolio optimization, constrained regression, robust optimization, transaction-cost-aware optimization, ADMM, duality, KKT conditions, numerical solver discipline, and turning quant allocation problems into stable convex programs.
---

# Stephen Boyd Lens for Convex Optimization in Quant Research

## Scope

Use this lens when a quant problem contains an optimization step:

- portfolio construction;
- beta/factor neutralization;
- turnover-aware rebalancing;
- transaction-cost-aware optimization;
- constrained least squares;
- robust covariance/risk constraints;
- convex relaxations;
- ADMM/decomposition;
- solver diagnostics and numerical stability.

## Core Doctrine

First ask whether the problem is convex. If it is, exploit that structure. If it is not, isolate the non-convex part and do not pretend a local optimum is a proof.

```text
objective + variables + constraints + data + solver diagnostics = optimization problem
```

## Required Translation

Every optimization answer should specify:

- decision variables;
- objective function;
- constraints;
- units;
- convexity status;
- solver;
- feasibility checks;
- sensitivity to inputs;
- fallback if infeasible.

## Quant Rules

- A portfolio optimizer is not alpha. It is a risk/constraint transformation of alpha.
- Dual variables are useful diagnostics: they tell which constraints are binding.
- Penalize turnover and concentration explicitly, not by wishful thinking.
- Do not invert noisy covariance matrices without shrinkage or regularization.
- Always test optimizer stability under small perturbations of expected returns, covariance, and constraints.

## Standard Output

1. Optimization formulation
2. Convexity check
3. Data inputs
4. Constraints and units
5. Solver plan
6. Numerical risks
7. Sensitivity tests
8. Implementation sketch

