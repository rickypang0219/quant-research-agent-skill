# Market Microstructure Experiments

This file converts microstructure theory into empirical experiments. Each experiment should be implemented with explicit timestamps, lagging rules, costs, and fill assumptions.

## Data Requirements

### Ideal data

- Level 3 order events: add, cancel, modify, execute, order ID, side, price, quantity, timestamp.
- Level 2 book snapshots: bid/ask prices and sizes across multiple levels.
- Trades: price, quantity, aggressor side, timestamp.
- Fees: maker/taker rates, rebates, minimum notional, tick size, quantity step.
- Venue metadata: matching rules, order types, rate limits, latency constraints.

### Minimum data for crypto research

- Best bid/ask snapshots or level 2 snapshots.
- Aggregate trades with aggressor side.
- OHLCV bars only if studying lower-frequency approximations.
- Funding rates and open interest for perpetuals.

### Data audit checklist

Before any experiment:

1. Check timestamp monotonicity.
2. Remove duplicate messages.
3. Detect crossed or locked books.
4. Verify positive prices and quantities.
5. Check missing intervals.
6. Align trades to the last known quote before the trade.
7. Convert all times to UTC.
8. Store raw data immutable; write derived data separately.

## Experiment 1: Spread, depth, and liquidity regimes

### Hypothesis

Liquidity is state-dependent. Spread and depth change with volatility, time of day, news, funding events, and market stress.

### Features

- `spread_bps`
- `depth_L1`, `depth_L5`, `depth_L10`
- realized volatility
- trade intensity
- OFI magnitude
- funding rate / basis for perps

### Procedure

1. Bucket data by 1s, 5s, 1m, and 5m.
2. Compute median spread and depth per bucket.
3. Segment by volatility quantile.
4. Plot spread/depth distributions by regime.
5. Test whether high-volatility regimes have wider spreads and thinner depth.

### Metrics

- median spread bps,
- median depth in notional,
- spread/depth ratio,
- volatility-normalized spread,
- tail spread during stress.

### Failure modes

- Snapshot sampling misses fast liquidity withdrawal.
- Exchange outages and data gaps look like liquidity shocks.
- Aggregated order book data can hide queue dynamics.

### Deliverable

A liquidity-regime report that says when the market is cheap or expensive to trade.

## Experiment 2: Microprice predictive power

### Hypothesis

When bid depth exceeds ask depth, the next mid-price move is more likely upward; when ask depth exceeds bid depth, next move is more likely downward.

### Feature

```math
microprice\_skew_t = \mu_t - m_t
```

or

```math
imbalance_t = \frac{B_t - A_t}{B_t + A_t}
```

### Target

```math
y_t = sign(m_{t+h} - m_t)
```

for `h = next event, 1s, 5s, 30s`.

### Procedure

1. Compute `microprice_skew_t` using only current book state.
2. Lag features correctly.
3. Predict future mid-price direction.
4. Compare against baseline `P(up)=0.5` and against spread state.
5. Evaluate by spread regime: one-tick spread vs multi-tick spread.

### Metrics

- directional accuracy,
- AUC,
- calibration curve,
- expected return after crossing fees,
- maker quote skew improvement.

### Failure modes

- Imbalance may be spoofed or quickly canceled.
- Deep queues can vanish before fills.
- Signal can be contemporaneous, not forward-looking.

## Experiment 3: OFI regression and depth-adjusted impact

### Hypothesis

Short-horizon mid-price changes are approximately linear in order flow imbalance, and the slope is inversely related to book depth.

### Model

```math
\Delta m_k = \alpha + \beta OFI_k + \varepsilon_k
```

Depth relation:

```math
\beta_k \approx \frac{c}{D_k}
```

### Procedure

1. Build event-level OFI.
2. Aggregate into buckets: 100 ms, 1s, 5s, 30s, 1m.
3. Run rolling regressions of `Δmid` on OFI.
4. Regress estimated `β` on inverse depth.
5. Compare raw signed volume vs OFI.

### Metrics

- in-sample `R²` for explanatory model,
- out-of-sample predictive `R²`,
- stability of `β`,
- t-stat by asset and regime,
- post-cost trading P&L if used as signal.

### Failure modes

- Using contemporaneous bucket OFI to trade at the same bucket close is lookahead.
- OFI explains price movement after it happened; prediction needs lagged OFI.
- Bucket choice changes results.

## Experiment 4: Trade-sign autocorrelation and hidden order splitting

### Hypothesis

Trade signs are autocorrelated because large participants split parent orders.

### Features

- trade sign `epsilon_i`,
- signed volume,
- signed notional,
- run length of same-side trades.

### Procedure

1. Compute trade signs from exchange aggressor flag.
2. Estimate autocorrelation of trade signs over lags.
3. Compare event time and clock time.
4. Test whether long same-side runs predict spread widening or price continuation.

### Metrics

- autocorrelation decay,
- half-life of trade-sign persistence,
- conditional return after buy/sell runs,
- turnover-adjusted P&L.

### Failure modes

- Aggregated trades can compress many child trades into one print.
- Trade-sign classification errors contaminate results.

## Experiment 5: Effective spread, realized spread, and adverse selection

### Hypothesis

Liquidity providers appear to earn spread at execution, but adverse selection reduces the realized spread after price moves.

### Procedure

1. For every trade, record trade price, aggressor sign, and prevailing mid.
2. Compute effective spread.
3. Compute realized spread at horizons `1s, 5s, 30s, 1m, 5m`.
4. Compute adverse-selection component.
5. Segment by trade size, volatility, OFI, and spread state.

### Metrics

- average effective spread,
- average realized spread,
- adverse selection by horizon,
- realized spread by trade-size decile,
- realized spread during high toxicity.

### Failure modes

- Need correct trade-to-quote alignment.
- Hidden liquidity and midpoint executions complicate interpretation.
- If using crypto, venue matching details matter.

## Experiment 6: Passive fill probability model

### Hypothesis

Fill probability depends on quote distance, queue-ahead, recent market-order intensity, cancellation intensity, and imbalance.

### Target

```math
P(fill \le \Delta t)
```

### Features

- distance from best price in ticks,
- queue ahead,
- spread,
- imbalance,
- recent market-order intensity,
- recent cancellation intensity,
- volatility.

### Procedure

1. Simulate joining best bid/ask at observed times.
2. Track queue-ahead using L3 if possible; approximate with L2 if not.
3. Label fill/no-fill within `Δt`.
4. Fit logistic, survival, or hazard model.
5. Calibrate by side and regime.

### Metrics

- Brier score,
- calibration curve,
- fill probability by distance,
- expected realized spread conditional on fill,
- fill-to-adverse-selection tradeoff.

### Failure modes

- L2 cannot accurately know queue position.
- Cancellations ahead of you are hard to infer without L3.
- Backtests often overestimate passive fills.

## Experiment 7: Queue depletion and next price move

### Hypothesis

The side of the book that depletes first determines the next mid-price move.

### Target

```math
P(ask\ queue\ depletes\ before\ bid\ queue)
```

### Features

- best bid/ask queue sizes,
- recent market buys/sells,
- cancellation rates,
- limit-order arrival rates,
- OFI,
- spread state.

### Procedure

1. Identify periods when spread is stable.
2. Track queue sizes until one side depletes.
3. Fit a depletion probability model.
4. Compare to microprice imbalance.
5. Use the model to improve short-horizon fair value.

### Metrics

- log loss,
- AUC,
- calibration,
- improvement over simple imbalance,
- strategy P&L from quote skew.

### Failure modes

- Queue jumps due to price improvements.
- Hidden orders and iceberg liquidity.
- Event aggregation can hide true sequence.

## Experiment 8: Avellaneda-Stoikov market-making simulation

### Hypothesis

Inventory-aware quote skew reduces inventory variance and tail risk compared with symmetric quoting.

### Baselines

1. Symmetric quotes around mid.
2. Reservation-price quotes.
3. Reservation-price plus alpha skew.
4. Reservation-price plus microprice skew.

### Procedure

1. Estimate volatility `sigma`.
2. Estimate fill intensity `lambda(delta)` from historical data.
3. Choose `gamma`, horizon `T`, and inventory limits.
4. Simulate mid-price paths and fills.
5. Include maker fees, taker liquidation cost, tick rounding, and min notional.
6. Stress test with volatility jumps and directional flow.

### Metrics

- average P&L,
- P&L volatility,
- max inventory,
- inventory variance,
- drawdown,
- realized spread,
- adverse-selection cost,
- probability of forced liquidation.

### Failure modes

- Poisson fill assumption may fail in clustered markets.
- Brownian mid-price is too simple for crypto jumps.
- Calibration can be regime-specific.

## Experiment 9: Quote skew from alpha vs quote skew from inventory

### Hypothesis

Alpha skew and inventory skew can conflict. The optimal quote balances expected price movement against inventory risk.

### Procedure

1. Build short-horizon alpha from OFI/microprice.
2. Build inventory penalty.
3. Define fair quote center:

```math
center_t = m_t + \alpha_t - \Gamma q_t
```

4. Run simulations under different `Gamma` values.
5. Evaluate whether alpha improves realized spread after controlling inventory.

### Metrics

- realized spread,
- inventory-adjusted P&L,
- inventory half-life,
- quote fill asymmetry,
- tail inventory.

### Failure modes

- Alpha may only predict fills, not mid-price movement.
- Strong inventory penalty can destroy alpha capture.
- Weak inventory penalty creates tail risk.

## Experiment 10: Market impact calibration

### Hypothesis

Price impact is concave in participation rate and depends on volatility and volume.

### Model

```math
E[\Delta p] = Y\sigma \left(\frac{Q}{V}\right)^\delta
```

### Procedure

1. Identify meta-orders if available; otherwise approximate with same-sign trade runs.
2. Estimate impact vs participation rate.
3. Separate temporary and permanent impact by measuring price reversion after completion.
4. Compare linear, square-root, and transient-impact models.

### Metrics

- impact coefficient,
- decay half-life,
- temporary/permanent split,
- model residual by regime,
- execution cost forecast error.

### Failure modes

- Meta-order reconstruction is hard without parent-order IDs.
- Same-sign trade runs can mix many participants.
- Impact and alpha are confounded.

## Experiment 11: Almgren-Chriss execution backtest

### Hypothesis

Optimal execution should trade faster when volatility risk dominates and slower when impact dominates.

### Strategies

- TWAP,
- VWAP,
- front-loaded Almgren-Chriss,
- liquidity-aware schedule,
- opportunistic schedule using spread/depth/OFI.

### Procedure

1. Define parent order size `Q` and horizon `T`.
2. Calibrate volatility, temporary impact, and permanent impact.
3. Generate execution schedules.
4. Simulate fills with spread, fees, and impact.
5. Compare implementation shortfall.

### Metrics

- mean shortfall,
- shortfall variance,
- tail shortfall,
- participation rate,
- completion risk,
- sensitivity to volatility and depth.

### Failure modes

- Historical replay may not reflect your own impact.
- Market impact model can create arbitrage if badly specified.
- Execution alpha and market impact are difficult to separate.

## Experiment 12: VPIN and toxicity stress indicator

### Hypothesis

Large volume-time buy/sell imbalance signals toxic flow and higher near-term volatility.

### Procedure

1. Classify trades as buyer/seller initiated.
2. Build equal-volume buckets.
3. Compute VPIN over rolling bucket windows.
4. Test whether high VPIN predicts future volatility, spread widening, or negative realized spread for passive orders.
5. Compare to simpler taker imbalance and OFI features.

### Metrics

- volatility forecast improvement,
- realized spread during high VPIN,
- false-positive rate,
- incremental value over realized volatility.

### Failure modes

- VPIN is sensitive to trade classification and bucket size.
- High toxicity can be contemporaneous with volatility, not predictive.
- It may be better as a risk-off filter than an entry signal.

## Experiment 13: Cross-venue lead-lag and price discovery

### Hypothesis

For crypto, one venue or instrument may lead others during certain regimes. Perpetual futures may lead spot during leverage/liquidation events.

### Data

- Binance spot/perp,
- Coinbase spot,
- OKX/Bybit perps,
- funding/open interest/liquidations if available.

### Procedure

1. Align venues to a common timestamp grid.
2. Compute mid-price returns at high frequency.
3. Estimate lead-lag correlations.
4. Fit VECM or lagged regression.
5. Segment by volatility, funding, and liquidity.

### Metrics

- lead-lag correlation,
- Granger causality tests,
- forecast error reduction,
- tradable latency-adjusted P&L,
- regime dependence.

### Failure modes

- Timestamp synchronization errors create fake lead-lag.
- Cross-venue fees and transfer constraints matter.
- Apparent lead may be untradeable after latency.

## Experiment 14: Crypto perp funding and microstructure interaction

### Hypothesis

Extreme funding or basis changes liquidity, order flow, and the relation between spot and perp returns.

### Features

- funding rate,
- basis,
- open interest,
- taker imbalance,
- OFI,
- spread/depth,
- liquidation notional if available.

### Procedure

1. Align funding intervals with high-frequency book/trade data.
2. Segment periods by funding quantile.
3. Test whether OFI impact coefficient changes under extreme funding.
4. Test whether perp leads spot more during high basis/funding periods.

### Metrics

- OFI beta by funding regime,
- spread/depth by funding regime,
- lead-lag by funding regime,
- post-cost strategy performance.

### Failure modes

- Funding is slow-moving relative to order book dynamics.
- Funding announcements may be known in advance.
- Liquidation data may not have historical depth.

## Experiment 15: Latency sensitivity for passive strategies

### Hypothesis

A strategy that looks profitable with zero latency may fail after quote/cancel delay.

### Procedure

1. Run the same backtest with latencies: `0 ms, 10 ms, 50 ms, 100 ms, 250 ms, 1 s`.
2. Delay signal observation, order submission, and cancel requests separately.
3. Reprice stale quotes using replayed book state.
4. Track fills that occur after adverse price movement.

### Metrics

- P&L decay by latency,
- adverse-selection increase,
- stale-fill rate,
- cancellation failure rate,
- inventory tail risk.

### Failure modes

- Data timestamp precision may be insufficient.
- Exchange gateway latency differs from local simulation latency.
- Queue priority is hard to simulate without order IDs.

## Experiment 16: Tick size, minimum notional, and fee threshold

### Hypothesis

Small accounts and small spreads can be structurally unprofitable after fees and tick/min-notional constraints.

### Procedure

1. Compute gross edge per trade in ticks or bps.
2. Subtract maker/taker fees.
3. Apply minimum notional and quantity step.
4. Compute breakeven spread capture.
5. Estimate number of trades needed to overcome variance.

### Metrics

- expected net edge per trade,
- breakeven spread in bps,
- min profitable notional,
- sensitivity to fee tier,
- capacity under available depth.

### Failure modes

- Ignoring the tick size of price and quantity.
- Assuming limit orders always earn the full spread.
- Ignoring adverse selection after fill.

## Experiment 17: Event-driven backtester validation

### Hypothesis

A microstructure strategy requires event-driven simulation; bar backtests overstate fill quality.

### Tests

1. Reconstruct book state from event stream.
2. Implement order state: submitted, live, partially filled, canceled, rejected.
3. Enforce tick size, lot size, min notional, and rate limits.
4. Simulate queue priority.
5. Compare event-driven backtest vs bar-based approximation.

### Metrics

- fill ratio,
- average queue wait,
- partial fill rate,
- slippage,
- stale fill rate,
- P&L difference between event and bar backtest.

### Failure modes

- L2 snapshots cannot fully reconstruct queue priority.
- Hidden liquidity changes real fills.
- Exchange matching details matter.

## Experiment 18: Market microstructure feature selection for medium-frequency stat arb

### Hypothesis

Microstructure features can improve medium-frequency crypto stat arb by filtering bad entries and identifying toxic liquidity regimes.

### Integration points

Use microstructure features to:

- avoid entering mean-reversion trades during toxic flow,
- size down when spread/depth is poor,
- delay execution when impact is high,
- choose passive vs aggressive execution,
- choose venue or instrument,
- improve residual return forecasts.

### Procedure

1. Build base stat-arb signal such as PCA residual s-score.
2. Add microstructure filters:
   - spread bps,
   - depth percentile,
   - OFI direction,
   - taker imbalance,
   - short-horizon volatility,
   - funding/basis for perps.
3. Compare baseline vs filtered strategy.
4. Decompose improvement into alpha improvement and cost reduction.

### Metrics

- Sharpe,
- turnover,
- transaction cost,
- hit rate,
- average entry spread,
- adverse selection after entry,
- performance by liquidity regime.

### Failure modes

- Microstructure features may reduce sample size and overfit.
- Filters can accidentally remove profitable stress opportunities.
- Need walk-forward and cross-asset validation.

## Milestone Plan

### Milestone 1: Market data foundation

Deliverables:

- raw data ingestion,
- normalized schema,
- data audit report,
- best bid/ask reconstruction,
- trade sign validation.

Success condition:

- Book and trade data align with no obvious timestamp or crossing errors.

### Milestone 2: Stylized facts dashboard

Deliverables:

- spread/depth plots,
- OFI distribution,
- trade-sign autocorrelation,
- volatility/liquidity regime segmentation,
- effective/realized spread diagnostics.

Success condition:

- You can explain when the market is liquid, toxic, jumpy, or expensive to trade.

### Milestone 3: Predictive baselines

Deliverables:

- microprice model,
- OFI model,
- queue-depletion model,
- simple trade-sign model.

Success condition:

- At least one feature improves out-of-sample prediction after proper lagging.

### Milestone 4: Execution-aware backtest

Deliverables:

- fee-aware P&L,
- passive/aggressive fill assumptions,
- latency sensitivity,
- tick/min-notional constraints.

Success condition:

- Strategy performance remains meaningful after realistic costs.

### Milestone 5: Strategy prototypes

Choose one:

1. Microprice/OFI quote-skew market maker.
2. OFI-based short-horizon directional strategy.
3. Liquidity-regime filter for medium-frequency stat arb.
4. Almgren-Chriss execution optimizer for crypto execution.
5. Cross-venue lead-lag execution strategy.

Success condition:

- The prototype has explicit edge source, cost model, risk limits, and failure-mode analysis.

## Standard Experiment Report Template

```markdown
# Experiment: <name>

## Question
What exactly are we testing?

## Hypothesis
What should happen if the microstructure theory is useful?

## Data
Asset, venue, dates, event type, sampling clock, timezone.

## Feature Construction
Exact formulas and lagging rules.

## Target
Prediction target and horizon.

## Backtest Assumptions
Fees, fills, latency, tick size, min notional, partial fills.

## Results
Tables, plots, metrics.

## Robustness
Different assets, dates, regimes, fees, latency, horizons.

## Interpretation
What changed in market intuition?

## Trading Decision
Use, reject, or keep as risk filter.

## Next Step
One concrete follow-up experiment.
```
