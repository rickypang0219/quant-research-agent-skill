# Backtesting Experiments

## Experiment 0 — Data Integrity Gate

### Goal

Reject bad data before running any strategy.

### Inputs

- OHLCV bars
- trades
- order book snapshots/deltas
- funding rates
- contract specs
- fee schedule

### Tests

1. Timestamp monotonicity.
2. Duplicate timestamps.
3. Missing intervals.
4. OHLC validity.
5. Negative volume.
6. Zero or negative price.
7. Symbol mapping changes.
8. Timezone normalization.
9. REST pagination completeness.
10. WebSocket sequence gaps.
11. Contract spec availability by date.
12. Funding timestamp alignment.
13. Exchange maintenance gaps.

### Pass Condition

The dataset has a written quality report and known gaps are explicitly marked.

---

## Experiment 1 — Vectorized Baseline Backtest

### Goal

Build the simplest possible alpha test.

### Example

Mean-reversion z-score:

```text
X_t = log price
z_t = (X_t - rolling_mean_L) / rolling_std_L
long when z_t < -z_entry
short when z_t > z_entry
exit when z_t crosses 0
execute at next bar open
```

### Required Outputs

- equity curve
- PnL series
- position series
- trade list
- Sharpe
- Sortino
- max drawdown
- turnover
- fee paid
- monthly PnL
- exposure

### Rejection Criteria

Reject immediately if the result only works with same-bar execution or no costs.

---

## Experiment 2 — Parameter Heatmap

### Goal

Separate robust behavior from noise-fitted parameters.

### Grid

Example:

```text
lookback ∈ [24, 48, 96, 168, 336]
z_entry ∈ [1.0, 1.5, 2.0, 2.5, 3.0]
z_exit ∈ [0.0, 0.25, 0.5, 1.0]
```

### Output

- heatmap of train Sharpe
- heatmap of forward Sharpe
- heatmap of turnover
- heatmap of max drawdown
- heatmap of trade count

### Interpretation

Prefer parameter plateaus over isolated spikes.

### Rejection Criteria

Reject if the only profitable parameter is isolated.

---

## Experiment 3 — Train / Forward Split

### Goal

Test whether selected parameters generalize.

### Procedure

1. Split data:

```text
train: 2020-01-01 to 2023-12-31
forward: 2024-01-01 to 2026-01-01
```

2. Search parameters only on train.
3. Freeze one parameter set.
4. Evaluate once on forward.

### Pass Condition

Forward performance remains acceptable after costs.

### Rejection Criteria

If forward Sharpe or PnL collapses, assume overfitting until proven otherwise.

---

## Experiment 4 — Walk-Forward Optimization

### Goal

Simulate repeated parameter selection over time.

### Example Schedule

```text
train window: 365 days
test window: 30 days
step: 30 days
```

For each fold:

1. Optimize on train.
2. Freeze parameters.
3. Trade on next test window.
4. Append OOS PnL.

### Outputs

- fold-level selected parameters
- fold-level OOS metrics
- aggregate OOS equity
- parameter stability plot
- fold Sharpe distribution

### Rejection Criteria

Reject if parameters jump randomly and OOS result is dominated by one fold.

---

## Experiment 5 — Optuna Search With Anti-Overfit Controls

### Goal

Use smarter search without lying to yourself.

### Required Controls

- fixed train/validation/forward split
- maximum trial count
- logged random seed
- logged search space
- pruning disabled unless justified
- cost included inside objective
- turnover penalty inside objective
- final untouched forward test

### Objective Example

```text
maximize:
    train Sharpe
    - λ_turnover * turnover
    - λ_drawdown * max_drawdown_penalty
```

### Rejection Criteria

Reject if Optuna discovers a sharp parameter needle that fails forward.

---

## Experiment 6 — Cost Stress Test

### Goal

Find whether the strategy is only profitable because costs are underestimated.

### Procedure

Run the selected strategy with:

```text
cost multiplier ∈ [0, 0.5, 1, 2, 3, 5]
```

Include:

- maker/taker fee
- half-spread
- slippage
- impact
- funding
- borrow if relevant

### Outputs

- Sharpe vs cost multiplier
- CAGR/PnL vs cost multiplier
- turnover vs cost multiplier
- break-even fee bps

### Rejection Criteria

Reject high-turnover strategies that die under small cost increases.

---

## Experiment 7 — Latency Stress Test

### Goal

Determine whether execution speed assumptions are critical.

### Applies To

- event-driven backtests
- trade/order-book based strategies
- intraday crypto
- market making
- statistical arbitrage with short holding period

### Procedure

Run the strategy under:

```text
latency ∈ [0 ms, 50 ms, 100 ms, 250 ms, 1 s, 5 s, 30 s]
```

Use market state at order arrival time.

### Outputs

- fill price degradation
- fill probability
- PnL vs latency
- missed signal rate
- adverse selection after fill

### Rejection Criteria

Reject if the edge disappears under realistic latency.

---

## Experiment 8 — Spread and Slippage Model Ladder

### Goal

Move from rough vectorized fills to more realistic fills.

### Levels

```text
L0: next-bar open
L1: bid/ask spread
L2: bar OHLC path model
L3: trade replay
L4: L2 book replay
L5: L3 queue replay
```

### Procedure

Run the same strategy under each fill model.

### Output

- performance degradation by realism level
- fill rate
- average slippage
- PnL attribution: signal alpha vs execution alpha

### Rejection Criteria

Reject if profit exists only under unrealistic fills.

---

## Experiment 9 — Event-Driven Order Lifecycle Test

### Goal

Verify that the engine behaves like a live trading system.

### Test Cases

1. Market order fills immediately against available liquidity.
2. Limit order rests if not marketable.
3. Limit order partially fills.
4. Limit order cancels after timeout.
5. Cancel fails if order already filled.
6. Order rejected due to min notional.
7. Order rejected due to tick/lot size.
8. Position limit rejects order.
9. Risk manager blocks leverage violation.
10. Funding payment changes equity.
11. Exchange downtime pauses trading.
12. Latency changes fill price.

### Pass Condition

Every state transition is logged and deterministic.

---

## Experiment 10 — Vectorized vs Event-Driven Reconciliation

### Goal

Understand why the fast research backtest differs from realistic replay.

### Procedure

1. Run vectorized version with next-bar open.
2. Run event-driven version with equivalent bar-level fills.
3. Compare trades one by one.
4. Then turn on spread, slippage, latency, and partial fills.

### Outputs

- trade count difference
- entry time difference
- exit time difference
- fill price difference
- PnL difference
- attribution of degradation

### Rejection Criteria

Reject or debug if the two engines disagree before realism effects are enabled.

---

## Experiment 11 — Capacity and Impact

### Goal

Estimate how much capital the strategy can absorb.

### Procedure

Run notional scale:

```text
capital ∈ [1k, 5k, 10k, 50k, 100k, 500k, 1m]
```

Impact model:

```text
impact bps = a + b * participation_rate
```

or square-root impact.

### Outputs

- PnL vs capital
- Sharpe vs capital
- turnover vs capital
- participation rate
- max single-trade participation
- capacity estimate

### Rejection Criteria

Reject if target size requires unrealistic participation in volume.

---

## Experiment 12 — Regime Robustness

### Goal

Check if performance is concentrated in one market regime.

### Slices

- bull market
- bear market
- high volatility
- low volatility
- high funding
- low funding
- high spread
- low spread
- high volume
- low volume
- pre/post major exchange rule change

### Outputs

- metrics by regime
- trade count by regime
- exposure by regime
- drawdown by regime

### Rejection Criteria

Reject or restrict if the strategy only works in one unexplained regime.

---

## Experiment 13 — Null Strategy / Randomization Test

### Goal

Check whether the result is better than random timing.

### Procedure

Compare against:

- randomly permuted signals
- randomly shifted signals
- random entry with same holding period
- random sign with same turnover
- bootstrapped returns
- block-bootstrapped returns

### Pass Condition

The real strategy beats the null distribution after costs.

---

## Experiment 14 — Multiple Testing Audit

### Goal

Quantify how many times you tried to find alpha.

### Record

- number of parameter combinations
- number of instruments tested
- number of feature variants
- number of bar sizes
- number of execution assumptions
- number of manual revisions

### Output

- experiment ledger
- adjusted significance threshold
- probability of backtest overfitting estimate if possible
- deflated Sharpe estimate if possible

### Rejection Criteria

A strategy with 1 good result after 10,000 tries is probably noise unless it has strong OOS evidence and economic rationale.

---

## Experiment 15 — Paper Trading Shadow Test

### Goal

Verify the event-driven engine against live market data without risking capital.

### Procedure

1. Run the same strategy code in paper mode.
2. Subscribe to live WebSocket data.
3. Generate orders but do not send real orders.
4. Simulate fills using the live order book.
5. Compare paper fills with what exchange state allowed.

### Outputs

- signal log
- paper orders
- simulated fills
- rejected orders
- latency measurements
- drift from event-driven backtest assumptions

### Promotion Condition

Paper results resemble event-driven simulation after realistic costs.

---

## Experiment 16 — Small-Capital Live Canary

### Goal

Discover live-only problems with minimal capital.

### Procedure

Use tiny size.

Test:

- API auth
- order creation
- cancel/replace
- min notional
- precision
- rate limits
- reconnect logic
- kill switch
- monitoring
- PnL accounting
- funding accounting

### Rejection Criteria

Stop immediately if logs cannot explain every position and order.

---

## Experiment 17 — Research Notebook to Production Config

### Goal

Prevent notebook-only research from becoming unrepeatable.

### Required Artifacts

```text
config.yaml
data_manifest.json
git_commit.txt
environment.lock
metrics.json
orders.parquet
fills.parquet
positions.parquet
equity.parquet
report.md
```

### Pass Condition

A new machine can reproduce the same backtest result from the saved artifacts.

---

## Experiment 18 — Crypto CEX/DEX Data Pipeline Test

### Goal

Validate public data ingestion.

### REST

Use REST for historical backfill:

- klines/candles
- trades
- funding
- open interest
- exchange info

### WebSocket

Use WebSocket for live/paper trading:

- trades
- order book
- best bid/ask
- liquidation if available
- funding updates if available

### Storage

Store raw data exactly as received.

Then create cleaned normalized tables.

### Pass Condition

Raw data is immutable and cleaned data is reproducible from raw data.
