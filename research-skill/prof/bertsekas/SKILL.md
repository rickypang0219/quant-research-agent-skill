---
name: bertsekas
description: Use for dynamic programming, stochastic optimal control, Markov decision processes, approximate dynamic programming, reinforcement learning sanity checks, inventory control, execution control, liquidation, and sequential decision-making under uncertainty.
---

# Dimitri Bertsekas Lens for Dynamic Programming and Control

## Scope

Use this lens when the problem is sequential:

- optimal execution;
- inventory control;
- market making control;
- liquidation;
- capital allocation over time;
- stopping decisions;
- MDPs;
- approximate dynamic programming;
- reinforcement learning validation;
- constrained sequential decisions.

## Core Doctrine

A control problem needs state, action, transition, cost/reward, constraints, and horizon. Without these, it is not a control problem.

```text
state -> action -> transition -> cost -> value function -> policy
```

## Quant Rules

- Define the state before choosing RL or DP.
- The action must be executable under exchange/risk constraints.
- Reward must include costs, slippage, inventory risk, and penalties.
- Compare learned policies with simple baselines.
- Stress policies under transition/model misspecification.

## Standard Output

1. State
2. Action/control
3. Transition model
4. Cost/reward
5. Constraints
6. Horizon
7. Baseline policy
8. Algorithm
9. Failure modes

