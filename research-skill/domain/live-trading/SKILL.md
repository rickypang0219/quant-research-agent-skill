---
name: live-trading
description: Use for live trading system design, paper trading, exchange APIs, execution, data ingestion, risk checks, monitoring, kill switches, logging, reconciliation, deployment readiness, and production incident handling.
---

# Live Trading Skill

## Scope

Use this skill when the work touches paper trading, real capital, exchange connectivity, streaming data, order routing, reconciliation, monitoring, deployment, or operational risk.

Live trading is not a backtest with a WebSocket. It is a distributed system that can lose money while partially broken.

## Source Basis

Use public engineering examples and official docs as priors:

- NautilusTrader: live trading, execution reconciliation, event-driven architecture, research-to-live parity.
- QuantConnect LEAN: modular algorithm engine, research/backtest/live workflows, portfolio/accounting abstractions.
- Official exchange API docs for actual order types, filters, rate limits, timestamps, and error codes.
- Public material from Jane Street, Citadel Securities, Tower Research, D. E. Shaw, and Renaissance only as evidence for engineering discipline: in-house systems, simulation, risk infrastructure, data/compute, and tight research-production loops.

## Live-Trading Rule

No strategy is live-ready unless all of these are true:

1. Data pipeline is reliable and timestamped.
2. Backtest is reproducible and lag-safe.
3. Costs, slippage, funding/borrow, and liquidity are included.
4. Event-driven or replay simulation matches the live execution assumption.
5. Paper trading has measured live-vs-sim drift.
6. Pre-trade and post-trade risk checks exist.
7. Positions, orders, fills, and balances reconcile against exchange state.
8. Monitoring and alerting are active.
9. Kill switch is tested.
10. Rollback and incident handling are documented.

## Architecture Layers

Separate:

- market data ingestion;
- normalization and schema validation;
- feature computation;
- signal generation;
- risk gate;
- order generation;
- execution adapter;
- order-state machine;
- portfolio/accounting state;
- reconciliation;
- persistence;
- metrics/logging/tracing;
- alerts;
- kill switch;
- deployment and rollback.

Do not mix signal logic with exchange error handling.

## Failure Modes

Handle:

- WebSocket disconnects;
- stale book or stale bars;
- out-of-order events;
- duplicate events;
- missing candles;
- exchange maintenance;
- rejected orders;
- partial fills;
- cancel rejection;
- rate limits;
- clock drift;
- balance mismatch;
- position mismatch;
- sudden fee/funding change;
- tick/lot/min-notional rule mismatch;
- symbol status changes;
- liquidation or margin calls;
- network partition;
- process crash and restart.

## Paper Trading Gate

Paper trading must report:

- intended orders vs submitted orders;
- submitted orders vs accepted/rejected orders;
- simulated fills vs exchange/paper fills;
- latency distribution;
- slippage distribution;
- live feature values vs backtest feature values;
- live signal distribution vs historical distribution;
- risk-limit breaches;
- reconciliation differences;
- incident log.

## Output Standard

When invoked, produce:

1. Live-readiness verdict
2. Architecture gaps
3. Data and timing risks
4. Execution risks
5. Risk controls
6. Monitoring and reconciliation
7. Tests required
8. Deployment plan
9. Rollback/kill-switch plan

