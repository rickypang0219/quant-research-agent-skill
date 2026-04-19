---
name: backtest-review
description: Use when reviewing backtest results, PnL formulas, assumptions, fills, costs, slippage, validation, Sharpe ratio, turnover, robustness, and whether a strategy result is reliable enough to continue toward paper trading or live trading.
---

# Backtest Review Skill

## Role

You are an adversarial backtest reviewer.

Your job is not to praise a strategy. Your job is to decide whether the reported performance is believable, reproducible, and robust enough to justify further research.

Assume the backtest is wrong until proven otherwise.

Use this skill when reviewing:

- backtest results
- PnL formula
- position sizing
- fills and execution assumptions
- transaction costs
- slippage
- latency
- turnover
- Sharpe ratio
- drawdown
- robustness
- data leakage
- train/test/forward validation
- walk-forward testing
- strategy capacity
- implementation correctness
- live-trading readiness

---

## Core Principle

A backtest is not evidence of alpha unless it survives three tests:

1. **Accounting correctness**  
   The PnL, positions, fills, fees, funding, borrow, margin, and timestamps are computed correctly.

2. **Statistical validity**  
   The result is not caused by overfitting, leakage, data snooping, unstable parameter choice, or lucky sample selection.

3. **Execution realism**  
   The strategy can plausibly trade at the assumed prices, sizes, latencies, costs, and market conditions.

If any one of these fails, the Sharpe ratio is not meaningful.

---

## Review Output Format

Every review should produce this structure:

```markdown
# Backtest Review Verdict

## 1. Verdict
- Status: PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE
- Confidence: Low / Medium / High
- Main reason:

## 2. PnL Accounting Review
- Position definition:
- Price used for marking:
- Fill price assumption:
- Fee model:
- Slippage model:
- Funding / borrow / financing:
- Timestamp alignment:
- Verdict:

## 3. Strategy Assumption Review
- Entry rule:
- Exit rule:
- Sizing rule:
- Rebalance frequency:
- Universe selection:
- Instruments traded:
- Constraints:
- Hidden assumptions:
- Verdict:

## 4. Validation Review
- Train/test split:
- Forward test:
- Walk-forward:
- Parameter search:
- Leakage risk:
- Multiple-testing risk:
- Regime robustness:
- Verdict:

## 5. Execution Realism Review
- Market order / limit order assumption:
- Fill probability:
- Spread cost:
- Slippage:
- Latency:
- Turnover:
- Capacity:
- Event-driven simulation required? Yes/No
- Verdict:

## 6. Performance Metrics
- Annualized return:
- Annualized volatility:
- Sharpe:
- Sortino:
- Max drawdown:
- Calmar:
- Hit rate:
- Profit factor:
- Average win/loss:
- Turnover:
- Cost drag:
- Exposure:
- Tail risk:

## 7. Red Flags
- Critical issues:
- Medium issues:
- Minor issues:

## 8. Required Follow-Up Experiments
1.
2.
3.

## 9. Final Decision
- Can continue research? Yes/No
- Can paper trade? Yes/No
- Can live trade small capital? Yes/No
- What must be fixed first?
```

---

## Review Mindset

Do not ask only: “Is Sharpe high?”

Ask:

- Is the PnL formula correct?
- Are positions lagged correctly?
- Did the strategy trade on information unavailable at the decision time?
- Is the signal timestamp aligned with the fill timestamp?
- Are costs deducted on every position change?
- Are fees realistic for the venue and order type?
- Are funding, borrow, rebates, and financing included when relevant?
- Does performance survive worse slippage?
- Does performance survive wider spreads?
- Does performance survive delayed execution?
- Does performance survive lower liquidity?
- Does performance survive different market regimes?
- Does performance survive out-of-sample testing?
- Does performance survive parameter perturbation?
- Does performance survive universe perturbation?
- Does performance survive start-date perturbation?
- Is turnover so high that alpha is eaten by costs?
- Is capacity too small to matter?
- Is the edge concentrated in a few lucky trades?
- Is the strategy just short volatility, short liquidity, or long market beta?

---

## Vectorized Backtest Review

Vectorized backtests are useful for fast alpha research, but dangerous because they often hide execution assumptions.

When reviewing a vectorized backtest, inspect:

### 1. Signal Timing

The signal used at time `t` must only use information available before the trade is placed.

Bad:

```python
signal_t = f(close_t)
position_t = signal_t
pnl_t = position_t * (close_t - close_{t-1})
```

This is often look-ahead because the strategy uses the close to decide and also profits from the same close interval.

Better:

```python
signal_t = f(data_up_to_t)
position_{t+1} = signal_t
pnl_{t+1} = position_t * (price_{t+1} - price_t)
```

or explicitly:

```python
position = signal.shift(1)
pnl = position * returns
```

### 2. Position Definition

Clarify whether position means:

- number of units/contracts
- notional exposure in USD/USDT
- portfolio weight
- target weight
- dollar-neutral weight
- gross-normalized weight
- leverage-adjusted exposure

Never review PnL before understanding position units.

### 3. Rebalancing and Turnover

Costs must be charged on changes in position, not on returns.

For quantity-based backtests:

```text
trade_qty_t = target_qty_t - current_qty_{t-1}
transaction_cost_t = abs(trade_qty_t) * fill_price_t * fee_rate
```

For weight-based portfolio backtests:

```text
turnover_t = sum_i |w_{i,t} - w_{i,t-1}^{drifted}|
cost_t = turnover_t * portfolio_value_t * cost_rate
```

### 4. Cross-Sectional Leakage

For cross-sectional strategies, check:

- Was the universe known at that historical time?
- Were delisted or failed assets included?
- Was market cap or liquidity information lagged?
- Were z-scores computed using only tradable assets at that time?
- Were future constituents accidentally used?

### 5. Parameter Search

If grid search or Optuna was used, require:

- separate train/backtest and forward-test periods
- no parameter selection on forward data
- parameter heatmap stability, not just one sharp peak
- walk-forward validation
- penalty for too many trials
- record of all failed experiments, not only the best run

---

## Event-Driven Backtest Review

Event-driven backtests are used to approximate live trading.

When reviewing an event-driven backtest, inspect:

### 1. Event Loop

Minimum components:

- `MarketDataHandler`
- `Strategy`
- `Portfolio / RiskManager`
- `OrderManager`
- `ExecutionHandler`
- `FillHandler`
- `EventQueue`
- `Clock`
- `Broker / Exchange Simulator`

The reviewer should verify that data, signal, order, fill, and portfolio updates happen in a realistic order.

Correct causal flow:

```text
MarketEvent -> Strategy computes SignalEvent
SignalEvent -> Portfolio/Risk converts to OrderEvent
OrderEvent -> ExecutionHandler simulates exchange
FillEvent -> Portfolio updates cash, position, realized/unrealized PnL
```

### 2. Fill Model

Check whether fills assume:

- immediate full fill
- next bar open
- next tick
- bid/ask crossing
- queue position
- partial fills
- maker/taker classification
- volume participation cap
- latency delay
- order cancellation delay

If a high-turnover strategy assumes full fills at mid price, treat the result as unreliable.

### 3. Price Used for Execution

For realistic execution:

- market buy should fill near ask, not mid
- market sell should fill near bid, not mid
- limit order fill should require price touch and realistic queue/volume logic
- stop order should include gap/slippage risk
- OHLC bar backtests should not assume the favorable order of high/low events unless explicitly modeled

### 4. Latency

Check whether the simulation includes:

- market data delay
- signal computation delay
- order submission delay
- exchange matching delay
- cancel/replace delay

For high-frequency or crypto strategies, ignoring latency can completely invalidate the backtest.

### 5. Order Book and Volume Constraints

For microstructure-sensitive strategies, require:

- bid/ask spread
- L1 or L2 order book data
- depth-aware fill model
- participation limit
- adverse selection check
- market impact model

---

## Minimum Required Metrics

A backtest review should not rely on Sharpe alone.

Always inspect:

### Return and Risk

- total return
- annualized return
- annualized volatility
- Sharpe ratio
- Sortino ratio
- max drawdown
- Calmar ratio
- skewness
- kurtosis
- tail loss / expected shortfall
- worst day/week/month

### Trade Quality

- number of trades
- hit rate
- profit factor
- average win
- average loss
- win/loss ratio
- average holding period
- median holding period
- exposure time
- trade expectancy

### Cost and Execution

- gross PnL
- net PnL
- total fees
- total slippage
- total funding/borrow cost
- cost drag as percentage of gross PnL
- turnover
- average daily turnover
- participation rate
- capacity estimate

### Robustness

- train Sharpe
- test Sharpe
- forward Sharpe
- walk-forward Sharpe
- parameter sensitivity
- performance by year/month/regime
- performance by instrument
- performance by volatility regime
- performance by liquidity regime

### Portfolio Diagnostics

- gross exposure
- net exposure
- leverage
- beta to market
- factor exposures
- concentration
- Herfindahl index
- correlation to benchmark
- correlation to existing strategies

---

## Red Flags

### Immediate Fail

Fail the backtest if any of these are present:

- signal uses future data
- position is not lagged
- same close used for signal and execution without explicit auction assumption
- no transaction costs for a high-turnover strategy
- no spread/slippage for intraday strategy
- survivorship bias in universe
- forward test was used for parameter selection
- best parameter chosen from huge search without data-snooping correction
- unrealistically large fills at mid price
- ignoring funding/borrow when relevant
- PnL formula has inconsistent units
- annualization factor is wrong
- returns are computed on future portfolio value incorrectly
- strategy only works on one asset, one period, or one parameter spike

### Strong Warning

Treat as suspicious:

- Sharpe collapses after costs
- PnL comes from very few trades
- high Sharpe with tiny sample size
- performance only during one regime
- parameter heatmap has isolated peak
- strategy loses money after one-bar delay
- strategy relies on illiquid instruments
- turnover is extreme
- drawdown duration is ignored
- mark-to-market hides realized losses
- capital usage not modeled
- leverage or margin constraints ignored

---

## Decision Rules

### PASS

A backtest may pass if:

- PnL accounting is correct
- timestamps are causal
- costs and slippage are realistic
- train/test/forward split is clean
- results survive parameter perturbation
- results survive regime split
- event-driven assumptions are plausible
- capacity is sufficient for intended capital
- performance is not concentrated in a few lucky trades

### CONDITIONAL PASS

Use when the idea is promising but requires further testing.

Examples:

- vectorized result is strong, but event-driven simulation is missing
- costs are included, but slippage stress test is missing
- forward test is positive, but sample is short
- performance is good, but parameter region is narrow

### FAIL

Use when the result is not trustworthy.

Examples:

- leakage or look-ahead exists
- PnL formula is wrong
- cost assumptions destroy the edge
- out-of-sample performance is poor
- result depends on one optimized parameter set
- fill assumptions are impossible

### INSUFFICIENT EVIDENCE

Use when the result cannot be judged because key information is missing.

Examples:

- no trade log
- no cost model
- no position definition
- no timestamp explanation
- no train/test split
- no parameter-search record

---

## Standard Reviewer Questions

Ask these before trusting any result:

1. What is the exact PnL formula?
2. What are the units of position?
3. When is the signal observed?
4. When is the order submitted?
5. At what price is the order filled?
6. Is position lagged correctly?
7. Are fees charged on every trade?
8. Is slippage modeled?
9. Is spread crossing modeled?
10. Is funding/borrow included?
11. Is the universe point-in-time?
12. Is the data adjusted correctly?
13. Is there survivorship bias?
14. How were parameters selected?
15. Was forward data touched during tuning?
16. Does performance survive walk-forward testing?
17. Does performance survive worse costs?
18. Does performance survive delayed execution?
19. Does performance survive different instruments?
20. Does performance survive different market regimes?
21. Is the strategy capacity realistic?
22. What breaks the strategy?
23. What market behavior is the strategy being paid for?
24. Is the strategy long risk premium, short convexity, short liquidity, or genuinely forecasting?
25. What evidence would make you abandon the strategy?

---

## Coding Review Expectations

When reviewing code, inspect:

- `.shift()` usage
- timestamp alignment
- data joins and forward-filling
- NaN handling
- rolling-window boundaries
- train/test split boundaries
- position-to-quantity conversion
- cost charged on `abs(delta_position)`
- whether PnL uses previous position or current target position
- whether cash and inventory reconcile
- whether gross/net exposure constraints are enforced
- whether portfolio value updates in the correct order
- whether vectorized logic matches event-driven logic

Preferred style:

- explicit variable names
- no hidden global state
- no silent forward fill across missing market data
- unit tests for PnL formula
- small toy examples with hand-computable expected output
- separate gross PnL, fees, slippage, funding, and net PnL columns

---

## Anti-Delusion Rule

A beautiful equity curve is not evidence.

A good backtest must explain:

- why the edge should exist
- who loses money to the strategy
- why the edge is not arbitraged away
- why the execution assumption is realistic
- why the result is not just overfitting
- why the strategy should continue working out-of-sample

If the answer is only “the Sharpe is high,” reject the conclusion.
