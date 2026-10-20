# Bertsekas Lens Examples

## Example 1 - Execution MDP

State:

- inventory remaining;
- time remaining;
- spread;
- volatility;
- depth;
- recent order flow.

Action:

- passive order size;
- aggressive order size;
- cancel/hold.

Reward:

```text
- implementation_shortfall - risk_penalty - inventory_penalty - fee
```

Baseline:

- TWAP;
- fixed participation;
- Almgren-Chriss schedule.

## Example 2 - RL Market Making Sanity Check

Reject the RL setup if:

- state excludes inventory;
- reward ignores adverse selection;
- simulator gives impossible fills;
- latency is zero;
- policy is not compared with symmetric quoting plus inventory skew.

## Example 3 - Stopping Rule

For a mean-reversion trade, define stop/exit as an optimal stopping problem only after specifying:

- state variable;
- transition model;
- cost of waiting;
- stop cost;
- terminal reward;
- estimation error.

