# Backtest Review Checklists

## 1. Minimum Information Required

Before reviewing, require:

- strategy description
- instrument universe
- timeframe
- data source
- data cleaning rules
- signal formula
- entry rules
- exit rules
- position sizing rule
- rebalance frequency
- PnL formula
- fee model
- slippage model
- fill model
- train/test split
- parameter-search method
- performance metrics
- trade log
- position history
- equity curve

If these are missing, verdict should usually be `INSUFFICIENT EVIDENCE`.

---

## 2. PnL Formula Checklist

- [ ] Are positions represented as quantity, notional, or weight?
- [ ] Does PnL use previous position, not future/current target position?
- [ ] Is trade quantity computed from change in position?
- [ ] Are transaction costs charged on absolute traded notional?
- [ ] Are fees, slippage, spread, funding, and borrow separated?
- [ ] Is NAV updated after PnL and costs?
- [ ] Are returns divided by previous NAV?
- [ ] Are cash and positions reconciled?
- [ ] Are realized and unrealized PnL handled correctly?
- [ ] Are inverse contracts, linear contracts, and spot positions handled differently if needed?
- [ ] Are contract multipliers included?
- [ ] Are base/quote currency conversions correct?

---

## 3. Timestamp Checklist

- [ ] What timestamp is attached to each price?
- [ ] What timestamp is attached to each signal?
- [ ] What timestamp is attached to each order?
- [ ] What timestamp is attached to each fill?
- [ ] Is the signal based only on information available at that time?
- [ ] Is the position lagged?
- [ ] Are rolling features computed without future data?
- [ ] Are resampled bars labeled by open time or close time?
- [ ] Are exchange server times used consistently?
- [ ] Are timezone conversions safe?
- [ ] Are missing bars handled correctly?

---

## 4. Data Checklist

- [ ] Is the data source reliable?
- [ ] Is raw data stored separately from cleaned data?
- [ ] Are cleaning steps reproducible?
- [ ] Are bad ticks removed with documented rules?
- [ ] Are missing values handled without leakage?
- [ ] Are delisted assets included where relevant?
- [ ] Is the universe point-in-time?
- [ ] Are corporate actions handled for equities?
- [ ] Are futures rolls handled for futures?
- [ ] Are funding rates aligned correctly for perpetuals?
- [ ] Are bid/ask and trade data used when execution requires them?

---

## 5. Cost Checklist

- [ ] Maker fee included?
- [ ] Taker fee included?
- [ ] Spread crossing included?
- [ ] Slippage included?
- [ ] Market impact included?
- [ ] Funding rate included for perpetuals?
- [ ] Borrow cost included for shorts?
- [ ] Financing/margin cost included?
- [ ] Withdrawal/deposit/settlement assumptions irrelevant or modeled?
- [ ] Fee tier realistic for traded volume?
- [ ] Costs stress-tested?

---

## 6. Fill Checklist

- [ ] Does market buy fill at ask or worse?
- [ ] Does market sell fill at bid or worse?
- [ ] Are limit order fills realistic?
- [ ] Is queue position considered?
- [ ] Are partial fills allowed?
- [ ] Are cancels delayed realistically?
- [ ] Is latency modeled?
- [ ] Is volume participation capped?
- [ ] Are OHLC bar fills conservative?
- [ ] Are stop orders modeled with gap risk?

---

## 7. Validation Checklist

- [ ] Is there a clean train/test/forward split?
- [ ] Was parameter search restricted to train/validation only?
- [ ] Was forward test touched only once?
- [ ] Is walk-forward testing performed?
- [ ] Are parameters stable across folds?
- [ ] Is performance stable across regimes?
- [ ] Is there a benchmark comparison?
- [ ] Is there factor exposure analysis?
- [ ] Is there data-snooping awareness?
- [ ] Are failed experiments recorded?

---

## 8. Parameter Search Checklist

- [ ] What parameters were searched?
- [ ] What ranges were searched?
- [ ] Why were those ranges chosen?
- [ ] How many trials were run?
- [ ] What objective was optimized?
- [ ] Does the objective penalize turnover/drawdown?
- [ ] Does the heatmap show a broad stable region?
- [ ] Are best parameters at search boundaries?
- [ ] Does out-of-sample performance match in-sample performance directionally?
- [ ] Was forward data protected?

---

## 9. Performance Metric Checklist

- [ ] Total return
- [ ] Annualized return
- [ ] Annualized volatility
- [ ] Sharpe ratio
- [ ] Sortino ratio
- [ ] Max drawdown
- [ ] Calmar ratio
- [ ] Hit rate
- [ ] Profit factor
- [ ] Average win/loss
- [ ] Trade expectancy
- [ ] Turnover
- [ ] Cost drag
- [ ] Exposure
- [ ] Leverage
- [ ] Beta
- [ ] Skewness
- [ ] Kurtosis
- [ ] Expected shortfall
- [ ] Capacity
- [ ] Number of trades
- [ ] Average holding period
- [ ] Drawdown duration

---

## 10. Robustness Checklist

- [ ] One-bar delay test
- [ ] Two-bar delay test
- [ ] Cost stress test
- [ ] Slippage stress test
- [ ] Spread stress test
- [ ] Start-date perturbation
- [ ] End-date perturbation
- [ ] Universe perturbation
- [ ] Parameter perturbation
- [ ] Walk-forward test
- [ ] Regime split
- [ ] Bootstrap confidence interval
- [ ] Trade-level autopsy
- [ ] Drawdown autopsy

---

## 11. Crypto-Specific Checklist

- [ ] Funding rates included for perpetual futures?
- [ ] Exchange fees match actual venue and tier?
- [ ] Quantity tick size respected?
- [ ] Price tick size respected?
- [ ] Minimum notional respected?
- [ ] Liquidation/margin constraints modeled?
- [ ] 24/7 annualization used?
- [ ] Stablecoin quote assumptions valid?
- [ ] Exchange outages or API gaps considered?
- [ ] Delisted coins handled?
- [ ] Liquidity collapse regimes tested?
- [ ] Maker/taker classification realistic?

---

## 12. Event-Driven Readiness Checklist

Move from vectorized to event-driven if:

- [ ] turnover is high
- [ ] strategy trades intraday
- [ ] fill price assumption materially affects PnL
- [ ] spread is large relative to expected edge
- [ ] signal half-life is short
- [ ] latency matters
- [ ] order type matters
- [ ] limit orders are used
- [ ] partial fills are likely
- [ ] capacity matters
- [ ] market impact matters

---

## 13. Paper Trading Readiness Checklist

Paper trade only if:

- [ ] vectorized backtest passes accounting review
- [ ] event-driven backtest passes execution review
- [ ] forward test is positive after costs
- [ ] logging is complete
- [ ] order reconciliation works
- [ ] risk limits are implemented
- [ ] kill switch exists
- [ ] monitoring dashboard exists
- [ ] paper/live config separation exists
- [ ] position and cash reconciliation are tested

---

## 14. Small Live Trading Readiness Checklist

Trade small live capital only if:

- [ ] paper trading agrees with event-driven backtest
- [ ] live data matches research data assumptions
- [ ] order execution is monitored
- [ ] slippage is measured live
- [ ] risk limits are enforced automatically
- [ ] max daily loss is enforced
- [ ] max position is enforced
- [ ] max leverage is enforced
- [ ] exchange failure behavior is defined
- [ ] strategy has explicit kill criteria

---

## 15. Final Verdict Template

```text
Verdict: PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE

Main issue:

Most dangerous assumption:

Most likely source of false alpha:

What must be fixed before trusting the result:

Next experiment:
```
