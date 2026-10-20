# Bertsekas Mental Models

## 1. State Must Be Markov Enough

If the state omits inventory, latency, spread, volatility, or risk limits, the policy will learn from a fake world.

## 2. Reward Design Is Strategy Design

A bad reward teaches bad trading. Include costs, drawdown, inventory, and risk penalties.

## 3. Baselines Are Mandatory

Compare DP/RL policies to TWAP, VWAP, no-trade, linear liquidation, and simple threshold policies.

## 4. Approximation Error Is Model Risk

Approximate DP can overfit simulation assumptions. Stress transition dynamics and execution costs.

## 5. Policy Constraints Matter

An optimal policy that violates lot size, rate limits, or risk limits is not admissible.

