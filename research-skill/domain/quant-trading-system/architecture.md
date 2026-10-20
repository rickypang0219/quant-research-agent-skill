# Quant Trading System Architecture

## Core Principle

A production trading system is a set of explicit state machines around uncertain market data and uncertain execution. Keep research, simulation, risk, and live execution separate but semantically aligned.

## Canonical Layers

```text
Raw Data
  -> Normalization
  -> Validation
  -> Feature Store
  -> Signal Engine
  -> Portfolio Construction
  -> Risk Gate
  -> Order Manager
  -> Execution Adapter
  -> Exchange
  -> Fills / Positions / Balances
  -> Reconciliation
  -> Metrics / Logs / Alerts
```

## State Boundaries

- Strategy state: features, signals, pending decisions.
- Portfolio state: positions, cash, margin, realized/unrealized PnL.
- Risk state: limits, utilization, breaches, kill-switch state.
- Order state: submitted, accepted, partially filled, filled, canceled, rejected, expired.
- Exchange state: open orders, fills, balances, positions.

No component should pretend another component's state is true without reconciliation.

## Research-to-Live Parity

Use shared semantics for:

- symbol identifiers;
- timestamp conventions;
- order side/type/time-in-force;
- fee and funding calculation;
- position quantity units;
- portfolio value;
- risk limits;
- fill events.

Differences between backtest and live must be explicit config, not hidden behavior.

## Minimum Production Modules

- Data adapter
- Schema validator
- Feature calculator
- Strategy
- Portfolio/accounting engine
- Risk manager
- Order manager
- Execution adapter
- Persistence layer
- Reconciliation loop
- Metrics/logging
- Alerting
- Kill switch

## Common Architecture Bugs

- Strategy directly calls exchange API.
- Risk checks occur after order submission.
- Internal position state is trusted without exchange reconciliation.
- Backtest and live use different fill/accounting semantics.
- Logs cannot connect signal -> order -> fill -> PnL.
- Restart loses open-order state.
- Config changes are not versioned.
- Clock drift is ignored.

