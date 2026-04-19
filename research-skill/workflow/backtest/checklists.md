# Backtesting Checklists

## 1. Hypothesis Checklist

- [ ] Instrument is specified.
- [ ] Venue is specified.
- [ ] Bar size or event type is specified.
- [ ] Date range is specified.
- [ ] Signal formula is explicit.
- [ ] Entry rule is explicit.
- [ ] Exit rule is explicit.
- [ ] Position sizing is explicit.
- [ ] Execution timing is explicit.
- [ ] Transaction cost model is explicit.
- [ ] Risk rule is explicit.
- [ ] Train/test split is explicit.
- [ ] Rejection criteria are explicit.

---

## 2. Look-Ahead Bias Checklist

- [ ] Signal at time `t` uses only data available at or before `t`.
- [ ] Rolling features are shifted if execution happens next bar.
- [ ] Forward returns are not used in feature construction.
- [ ] Labels are not leaked into training features.
- [ ] Fundamentals/macros/funding use release or available timestamp.
- [ ] Universe membership is point-in-time.
- [ ] Delisted instruments are included when relevant.
- [ ] Corporate actions are point-in-time if trading equities.
- [ ] Data revisions are handled or explicitly ignored.

---

## 3. Vectorized Backtest Checklist

- [ ] Positions are shifted correctly.
- [ ] Costs are included.
- [ ] Spread/slippage is at least approximated.
- [ ] Turnover is measured.
- [ ] Parameter search is logged.
- [ ] Heatmap is plotted.
- [ ] Forward test is untouched until final evaluation.
- [ ] Monthly PnL is shown.
- [ ] Drawdown is shown.
- [ ] Trade count is sufficient.
- [ ] Performance is not from one lucky trade.
- [ ] Result survives higher cost assumptions.

---

## 4. Event-Driven Backtest Checklist

- [ ] Market data replay is chronological.
- [ ] Event queue is deterministic.
- [ ] Strategy receives only available data.
- [ ] Risk manager checks every order.
- [ ] Exchange filters are enforced.
- [ ] Tick size and lot size are enforced.
- [ ] Min notional is enforced.
- [ ] Fees are venue-specific.
- [ ] Market orders cross spread.
- [ ] Limit orders do not fill magically.
- [ ] Partial fills are supported.
- [ ] Cancels can fail.
- [ ] Latency is modeled.
- [ ] Order status transitions are logged.
- [ ] Fills, orders, positions, and equity reconcile.
- [ ] Same code path can be adapted to paper/live trading.

---

## 5. Promotion Checklist

### Vectorized → Event-Driven

- [ ] Positive out-of-sample performance.
- [ ] Parameter plateau exists.
- [ ] Cost stress survives.
- [ ] Turnover is plausible.
- [ ] Signal has economic/microstructure rationale.
- [ ] Result is not dominated by one regime.

### Event-Driven → Paper

- [ ] Conservative fill model.
- [ ] Latency stress acceptable.
- [ ] Risk manager works.
- [ ] Logs are complete.
- [ ] Accounting reconciles.
- [ ] Engine can replay deterministically.

### Paper → Small Live

- [ ] Paper/live data path stable.
- [ ] API errors handled.
- [ ] Order rejects handled.
- [ ] Kill switch implemented.
- [ ] Monitoring implemented.
- [ ] Capital size is intentionally small.
