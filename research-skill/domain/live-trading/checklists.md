# Live Trading Checklists

## Pre-Paper Checklist

- [ ] Strategy has a falsifiable hypothesis and reproducible backtest.
- [ ] Config declares universe, symbols, sizing, fees, slippage, limits, and venue.
- [ ] Data schema validates all live messages.
- [ ] Event timestamps are monotonic or explicitly repaired.
- [ ] Signal uses only data available at decision time.
- [ ] Risk gate can reject orders.
- [ ] Order lifecycle states are tested.
- [ ] Persistence survives restart.
- [ ] Logs include correlation/run/order IDs.
- [ ] Alerts fire on stale data, rejected orders, and position mismatch.

## Pre-Live Checklist

- [ ] Paper trading ran long enough to cover normal and stressed market states.
- [ ] Live-vs-backtest tracking error has been explained.
- [ ] Pre-trade limits tested.
- [ ] Post-trade reconciliation tested.
- [ ] Kill switch tested in simulation or paper.
- [ ] Exchange rate-limit behavior tested.
- [ ] Clock drift monitor active.
- [ ] Max daily loss and max position limits active.
- [ ] Manual intervention path documented.
- [ ] Rollback plan documented.

## Incident Checklist

- [ ] Stop new orders.
- [ ] Cancel live resting orders if safe.
- [ ] Fetch exchange positions, balances, open orders, and recent fills.
- [ ] Reconcile internal state.
- [ ] Reduce exposure if limits are breached.
- [ ] Preserve logs and configs.
- [ ] Write incident note with root cause and follow-up tests.

