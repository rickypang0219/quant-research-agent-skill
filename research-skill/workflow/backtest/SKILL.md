---
name: backtest-workflow
description: Use for converting a trading hypothesis into reproducible vectorized and event-driven backtests, including dataset construction, leakage checks, parameter search, walk-forward validation, transaction-cost modeling, fill simulation, and live-trading readiness review.
---

# Backtest Workflow Skill

## Purpose

This skill turns a trading idea into a disciplined research workflow.

It separates two different jobs:

1. **Vectorized backtesting** for fast alpha discovery.
2. **Event-driven backtesting** for realistic live-trading simulation.

The agent must be adversarial. A good backtest is not a pretty equity curve. A good backtest is a falsification machine: it tries to prove that the alpha is fake before the user risks capital.

---

## Core Principle

A backtest has no value unless it answers:

> Did this rule create tradable, out-of-sample edge after fees, slippage, latency, market impact, funding, borrow, leverage, and operational constraints?

The workflow should always move from:

```text
idea
→ hypothesis
→ vectorized prototype
→ leakage/data audit
→ parameter search
→ train/test split
→ walk-forward / forward test
→ transaction-cost stress
→ event-driven replay
→ paper trading
→ small live capital
→ monitoring
```

---

## Use This Skill When

Use this skill when the user asks about:

- vectorized backtesting
- event-driven backtesting
- walk-forward validation
- train/test or in-sample/out-of-sample split
- grid search or Optuna parameter search
- Sharpe, drawdown, turnover, hit rate, PnL attribution
- transaction costs, slippage, latency, partial fills
- mock live trading
- market data replay
- Binance, Coinbase, Bybit, HyperLiquid, CEX/DEX data
- Polars, DuckDB, Parquet data pipelines
- Python or Rust backtesting engine design
- converting a strategy hypothesis into testable rules

---

## Non-Negotiable Attitude

The assistant must not flatter weak research ideas.

When the user proposes a strategy, respond as a quant researcher:

1. State the hypothesis in testable form.
2. Identify the exact signal, instrument, bar size, execution assumption, and holding period.
3. Ask what information is available at decision time.
4. Check for look-ahead bias, survivorship bias, selection bias, stale data, timestamp errors, and data snooping.
5. Design the simplest falsification test before designing complex improvements.
6. Require out-of-sample evidence before claiming edge.
7. Require transaction-cost and turnover stress tests.
8. Only then move to event-driven simulation.

---

## Hypothesis Stage

A hypothesis must contain:

```text
Market:
    e.g. Binance BTCUSDT perpetual, Nifty futures, SPY ETF, top-50 crypto universe

Data:
    bars, trades, order book, funding, open interest, liquidation, macro, options, etc.

Signal:
    formula using only information known before the trade

Entry:
    exact rule

Exit:
    exact rule

Position sizing:
    dollars, quantity, volatility target, risk-per-trade, beta-neutral, factor-neutral, etc.

Execution assumption:
    next bar open, next bar VWAP, maker order, taker order, delayed order, order-book replay

Costs:
    fee, spread, slippage, market impact, funding, borrow, tax if relevant

Validation:
    train period, test period, walk-forward schedule, stress tests
```

Bad hypothesis:

```text
Use z-score to trade BTC.
```

Good hypothesis:

```text
On Binance BTCUSDT perpetual 1h bars from 2020-01-01 to 2026-01-01, compute a rolling 96-bar z-score of log price deviation from its 96-bar moving average. If z < -2, enter long at next bar open. If z > 0, exit. If z > 2, enter short. If z < 0, exit. Use 1x notional, 6 bps taker cost, no leverage compounding, no same-bar execution. Use 2020-2023 for parameter search and 2024-2026 for forward test.
```

---

## Vectorized Backtesting

### Role

Use vectorized backtesting for primary alpha research.

It is fast and should answer:

- Does the signal have predictive power?
- Is the rule robust over parameter ranges?
- Does the edge survive simple costs?
- Is performance concentrated in one tiny period?
- Does the strategy depend on impossible execution?

Vectorized backtesting is not the final truth. It is the first filter.

### Typical Models

Use basic transparent models first:

- z-score
- percentile rank
- rate of change
- moving average crossover
- rolling volatility
- rolling beta
- AR/ARMA residuals
- mean-reversion residuals
- momentum continuation
- cross-sectional rank
- spread/residual z-score
- funding-rate carry
- order-flow imbalance
- volatility breakout
- time-of-day/session effect

### Vectorized Rules

Always shift positions or signals to prevent look-ahead bias.

Wrong:

```python
pnl = signal_t * return_t
```

Right:

```python
pnl = position_t_minus_1 * return_t
```

or:

```python
signal_t = f(data_until_t)
position_t_plus_1 = execution(signal_t)
pnl_t_plus_1 = position_t_plus_1 * return_t_plus_1
```

### Parameter Search

Allowed:

- grid search
- random search
- Optuna
- coarse-to-fine search
- walk-forward optimization
- combinatorial purged cross-validation for overlapping labels

Required safeguards:

1. Split data into parameter-estimation and forward-test regions.
2. Do not choose final parameters using the forward-test result.
3. Plot heatmaps, not just the best point.
4. Prefer parameter plateaus over isolated spikes.
5. Penalize high turnover and high parameter complexity.
6. Track the number of trials; many trials inflate apparent Sharpe.
7. Run cost stress tests.
8. Run subperiod tests.
9. Run instrument-universe tests.
10. Record every experiment.

### Parameter Heatmap Interpretation

Good sign:

```text
Sharpe is positive over a wide region:
    z_entry in [1.5, 2.5]
    lookback in [48, 168]
```

Bad sign:

```text
Sharpe is excellent only at:
    z_entry = 2.17
    lookback = 93
```

A narrow optimum is usually a symptom of noise fitting.

---

## Train / Forward Test Protocol

Use at least:

```text
Research / backtest period:
    Used to build signal and choose parameters.

Forward test / out-of-sample period:
    Used once to evaluate whether the selected parameters generalize.
```

Better:

```text
Train 1 → Test 1
Train 2 → Test 2
Train 3 → Test 3
...
Aggregate OOS results
```

Best for overlapping labels or machine learning:

```text
purged cross-validation + embargo
combinatorial purged cross-validation
deflated Sharpe / probability of backtest overfitting
```

If forward-test Sharpe or PnL collapses, assume one of:

- overfitting
- look-ahead bias
- cost underestimation
- regime dependence
- weak economic rationale
- data quality issue
- execution assumption too optimistic

Do not rescue the strategy by tuning on the forward set. That turns the forward set into training data.

---

## Event-Driven Backtesting

### Role

Use event-driven backtesting to mock live trading.

It should answer:

- What happens if market data arrives as a stream?
- What order is submitted?
- When does it reach the simulated exchange?
- Is it filled, partially filled, rejected, canceled, expired, or resting?
- What is the queue position?
- What is the slippage?
- What is the latency?
- What is the order status lifecycle?
- What risk checks fire before execution?
- Can the same strategy code run in paper/live trading?

### Core Architecture

```text
MarketDataHandler
    Replays historical bars/trades/order books as if they arrive live.

EventQueue
    Holds MarketEvent, SignalEvent, OrderEvent, FillEvent, CancelEvent, RiskEvent.

Strategy
    Consumes MarketEvent and emits SignalEvent.

Portfolio / PositionManager
    Tracks cash, positions, margin, exposure, realized/unrealized PnL.

RiskManager
    Converts signals into allowed orders or rejects them.

ExecutionHandler / SimulatedExchange
    Applies latency, order book state, matching logic, fee model, fill model.

Accounting
    Records fills, orders, PnL, fees, funding, borrow, inventory, turnover.

Reporter
    Produces metrics, plots, logs, and experiment artifacts.
```

### Event Types

```text
MarketEvent:
    timestamp, symbol, bid, ask, mid, trade, bar, book update

SignalEvent:
    timestamp, symbol, direction, strength, target_position, reason

OrderEvent:
    timestamp, symbol, side, order_type, quantity, limit_price, time_in_force

FillEvent:
    timestamp, symbol, side, quantity, fill_price, fee, liquidity_flag

CancelEvent:
    timestamp, order_id, reason

RiskEvent:
    timestamp, order_id, rule_name, action, reason
```

### Simulated Exchange Requirements

Minimum:

- market orders
- limit orders
- cancel orders
- maker/taker fees
- spread crossing
- partial fills
- order status transitions
- rejected orders
- no fill without available liquidity

Better:

- queue model
- latency model
- book-depth consumption
- order book replay
- stochastic fill probability
- funding payments
- margin/liquidation model
- borrow/short availability
- trading halts/maintenance periods
- exchange-specific filters: tick size, lot size, min notional

### Latency Model

At minimum:

```text
decision_time
→ order_submit_time = decision_time + strategy_latency
→ exchange_receive_time = order_submit_time + network_latency
→ fill_time = exchange_receive_time + matching_latency
```

The backtest must use market state at `exchange_receive_time`, not at `decision_time`.

### Fill Model Ladder

Use the lowest model that is honest for the data.

```text
Level 0:
    next-bar open fill, used only for rough vectorized tests

Level 1:
    bid/ask spread model

Level 2:
    bar OHLC path assumption

Level 3:
    trade replay

Level 4:
    L2 book replay

Level 5:
    L3 order-by-order queue simulation
```

Never use Level 0 to claim live tradability of high-turnover strategies.

---

## Data Collection

### Public Data Sources

Allowed public sources:

- Binance
- Coinbase
- Bybit
- HyperLiquid
- exchange-provided REST APIs
- exchange-provided WebSocket APIs
- official public data dumps
- reputable commercial data vendors when available

Avoid random social media opinions and unofficial claims.

### Python Stack

Use:

```text
uv for dependency and virtual environment management
polars for primary dataframe processing
duckdb for larger-than-memory or SQL-style parquet analytics
numpy/scipy for numerical calculation
numba for JIT acceleration when pure NumPy is not enough
pydantic for data contracts
requests/httpx for REST APIs
asyncio + websockets/aiohttp for streaming
plotly/matplotlib for visualization
ruff for linting
ty for type checking
pytest for testing
```

### Rust Stack

Use:

```text
cargo.toml for package management
tokio for async runtime
reqwest for REST
tokio-tungstenite or fastwebsockets for WebSocket
serde for serialization
arrow/parquet for columnar data
polars-rs or datafusion for analytics
tracing for structured logs
criterion for benchmarks
```

### Data Storage

Use Parquet.

Suggested layout:

```text
/data/
  raw/
    exchange=binance/
      market=perp/
        symbol=BTCUSDT/
          datatype=ohlcv/
            timeframe=1h/
              year=2020/
                part-000.parquet
  cleaned/
    exchange=binance/
      market=perp/
        symbol=BTCUSDT/
          datatype=ohlcv/
            timeframe=1h/
              year=2020/
                part-000.parquet
  features/
    strategy=<strategy_name>/
      feature_set=<feature_set_name>/
        timeframe=1h/
          part-000.parquet
  backtests/
    strategy=<strategy_name>/
      run_id=<timestamp_or_hash>/
        config.yaml
        metrics.json
        trades.parquet
        orders.parquet
        equity.parquet
        positions.parquet
        report.md
```

User example:

```text
/data/raw/exchange=binance/market=perp/symbol=BTCUSDT/datatype=ohlcv/timeframe=1h/year=2020/*.parquet
```

This partitioned layout is usually better than one folder named:

```text
/data/BTC_perps_binance_1hr_ohlc/
```

because it scales across venues, symbols, timeframes, and data types.

---

## Data Cleansing Checklist

Before backtesting, verify:

- timestamps are timezone-normalized, preferably UTC
- timestamps are unique per symbol/timeframe
- bars are sorted
- no duplicate bars
- no missing bars unless exchange was closed or market unavailable
- OHLC constraints hold: `low <= open, high, close <= high`
- volume is non-negative
- price is positive
- symbol mapping is stable
- contract specs are versioned
- tick size, lot size, min notional are correct for the date
- delisted instruments are not silently removed
- funding/borrow/corporate-action data is point-in-time
- no future data is used in features
- train/test boundaries are respected
- features have explicit availability timestamps

For crypto, additionally check:

- exchange maintenance gaps
- funding timestamps
- perpetual contract specification changes
- stablecoin depegs
- symbol migrations
- contract delistings
- WebSocket sequence gaps
- REST pagination gaps
- rate-limit retry artifacts

---

## Minimum Viable Backtest Report

Every backtest must produce:

```text
1. Hypothesis
2. Instruments and data source
3. Date range
4. Feature definitions
5. Entry / exit rules
6. Execution assumptions
7. Costs and slippage
8. Parameter search space
9. Train/test split
10. Out-of-sample results
11. Sharpe / Sortino / max drawdown / turnover / hit rate
12. Monthly or weekly PnL
13. Exposure and leverage
14. Top winning and losing periods
15. Cost sensitivity
16. Latency sensitivity if event-driven
17. Failure modes
18. Decision: reject, revise, or promote
```

---

## Promotion Rules

### Promote from Idea to Vectorized Prototype

Only if:

- hypothesis is explicit
- signal uses available data only
- entry and exit are deterministic
- cost model is specified
- data source is identified

### Promote from Vectorized to Event-Driven

Only if:

- out-of-sample result is positive
- parameter heatmap shows robustness
- cost stress test does not kill performance immediately
- turnover is plausible
- holding period is compatible with data resolution
- signal has economic or microstructure rationale
- performance is not concentrated in a tiny number of trades

### Promote from Event-Driven to Paper Trading

Only if:

- order lifecycle works
- fill model is conservative
- latency stress is acceptable
- risk limits work
- position accounting matches expectations
- logs are sufficient to debug a bad trade
- paper/live code path is close to backtest code path

### Promote from Paper Trading to Small Capital

Only if:

- paper trading matches event-driven expectation within tolerance
- live data pipeline is stable
- order rejects and cancels are handled
- monitoring and kill switch exist
- capital at risk is small enough to survive full failure

---

## Common Failure Modes

### Vectorized Backtest Failure

- unshifted signal
- same-bar close-to-close execution
- survivorship bias
- choosing universe after seeing winners
- forward-filling unavailable data
- tuning on test data
- ignoring delisted assets
- ignoring fees
- ignoring spread
- ignoring funding
- ignoring turnover
- single lucky regime
- annualizing high-frequency Sharpe naively
- using too many parameters

### Event-Driven Failure

- simulated fill at prices that were never tradable
- market order filled at mid
- limit order filled without queue/availability logic
- latency ignored
- order book state read before order arrival
- cancel always succeeds immediately
- partial fills ignored
- exchange filters ignored
- risk manager not in the loop
- live code path differs from backtest code path
- no replay determinism

---

## Agent Response Template

When asked to backtest a strategy, structure the answer as:

```text
1. Restate the hypothesis.
2. Identify missing assumptions.
3. Define vectorized first-pass version.
4. Define train/test split.
5. Define metrics.
6. Define parameter search.
7. Define failure checks.
8. Define event-driven upgrade path.
9. Provide code or pseudocode.
10. State what evidence would reject the strategy.
```

---

## Strong Default Position

If the user asks whether a vectorized backtest is enough:

> No. It is enough for alpha research, not enough for live trading. Use vectorized testing to discover and falsify ideas quickly. Use event-driven replay to test whether the strategy survives realistic execution.

If the user asks whether a high Sharpe is good:

> Not by itself. Ask how many trials were run, whether the result is out-of-sample, whether serial correlation inflates the Sharpe, whether costs were included, and whether the strategy survives forward testing.

If the user asks whether bad forward-test performance means look-ahead bias:

> Maybe, but not necessarily. It can also mean overfitting, regime change, underestimated costs, weak economic rationale, or data quality problems. Treat it as a rejection signal until proven otherwise.
