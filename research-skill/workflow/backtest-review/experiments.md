# Backtest Review Experiments

Use these experiments to attack a backtest before trusting it.

---

## 1. Toy PnL Unit Test

Create a tiny dataset where PnL can be computed by hand.

Example:

```text
price:      100, 101, 103, 102
position:     0,   1,   1,  -1
```

Correct price PnL uses previous position:

```text
pnl_1 = 0 * (101 - 100) = 0
pnl_2 = 1 * (103 - 101) = 2
pnl_3 = 1 * (102 - 103) = -1
```

Expected total before costs:

```text
total = 1
```

If the vectorized code gives a different answer, the backtest accounting is wrong.

---

## 2. Signal Shift Test

Run three versions:

1. original signal
2. signal shifted by one bar later
3. signal shifted by two bars later

Expected behavior:

- For low-frequency strategies, performance should degrade gradually.
- For high-frequency strategies, performance may degrade quickly.
- If one-bar delay completely kills performance, execution timing is critical and event-driven testing is required.

Red flag:

- original Sharpe is high, but one-bar-lag Sharpe is negative.

---

## 3. Cost Stress Test

Run the strategy with multiple fee/slippage assumptions:

```text
base cost
2x cost
3x cost
5x cost
10x cost
```

Record:

- net PnL
- Sharpe
- max drawdown
- turnover
- cost drag

Pass condition:

- strategy remains acceptable under moderately worse costs.

Fail condition:

- edge disappears under slightly worse costs.

---

## 4. Spread Stress Test

For intraday strategies, test execution at:

```text
mid
mid +/- half spread
bid/ask
bid/ask + extra slippage
```

Expected:

- market orders should not be filled at mid without cost adjustment.
- limit orders should not assume guaranteed fills.

---

## 5. Turnover Decomposition

Decompose total turnover by:

- date
- asset
- signal component
- rebalance event
- entry vs exit

Questions:

- Which assets cause most turnover?
- Which dates cause most costs?
- Does PnL survive if turnover is capped?
- Does the strategy trade too frequently for its forecast horizon?

---

## 6. Gross vs Net PnL Bridge

Create a bridge table:

```text
gross_pnl
- fees
- spread_cost
- slippage
- funding
- borrow
- financing
= net_pnl
```

Reject any backtest that only reports net PnL without this decomposition.

---

## 7. Parameter Heatmap Review

For grid search:

- plot Sharpe heatmap
- plot return heatmap
- plot drawdown heatmap
- plot turnover heatmap
- plot net PnL after costs

Pass condition:

- broad stable region of acceptable parameters.

Fail condition:

- one isolated spike.

---

## 8. Optuna / Bayesian Search Audit

For Optuna or similar optimization:

Record:

- number of trials
- parameter ranges
- objective function
- train/test split
- best trial
- top 20 trials
- distribution of trial performance
- forward performance of selected trial

Red flags:

- too many trials on small dataset
- forward test used during tuning
- objective optimizes Sharpe only and ignores turnover/drawdown
- best trial is far better than median trial
- selected parameters lie at boundary of search space

---

## 9. Walk-Forward Experiment

Procedure:

1. choose a training window
2. choose a test window
3. optimize only on training data
4. trade on test window
5. roll forward
6. concatenate all test windows

Report:

- aggregate out-of-sample PnL
- Sharpe by fold
- parameter chosen by fold
- turnover by fold
- drawdown by fold

Pass condition:

- most folds are reasonable.

Fail condition:

- total PnL comes from one fold.

---

## 10. Start-Date Perturbation

Rerun the strategy with different start dates:

```text
start date + 1 day
start date + 1 week
start date + 1 month
start date + 3 months
```

The strategy should not depend heavily on one lucky start date.

---

## 11. End-Date Perturbation

Rerun with different end dates:

```text
end date - 1 day
end date - 1 week
end date - 1 month
end date - 3 months
```

This catches strategies where recent performance dominates the full result.

---

## 12. Universe Perturbation

For cross-sectional strategies, rerun after:

- removing top-volume asset
- removing top-performing asset
- removing bottom-performing asset
- removing random 10% of universe
- using only high-liquidity assets
- using only assets listed before the start date

Pass condition:

- performance degrades gracefully.

Fail condition:

- strategy depends on one asset or survivorship-biased universe.

---

## 13. Regime Split

Split performance by regime:

- bull market
- bear market
- sideways market
- high volatility
- low volatility
- high liquidity
- low liquidity
- high funding
- low funding
- crisis period

Ask:

- what regime pays the strategy?
- what regime kills it?
- is the strategy secretly short volatility or short liquidity?

---

## 14. Benchmark and Factor Exposure Test

Regress strategy returns on relevant factors:

```text
R_strategy = alpha + beta_market * R_market
           + beta_momentum * F_momentum
           + beta_value * F_value
           + beta_carry * F_carry
           + epsilon
```

For crypto, possible factors:

- BTC return
- ETH return
- market-cap weighted crypto index
- momentum factor
- volatility factor
- funding factor
- liquidity factor

If alpha disappears after factor adjustment, the strategy may just be repackaged beta.

---

## 15. Capacity Stress Test

Run with different capital levels:

```text
$5k
$50k
$500k
$5m
```

For each level, estimate:

- participation rate
- slippage
- impact
- unfilled quantity
- capacity-constrained PnL

For your own small capital, capacity may not be the main issue. For institutional relevance, it matters a lot.

---

## 16. Fill Model Comparison

Compare:

1. ideal close-to-close fills
2. next-open fills
3. bid/ask fills
4. bid/ask plus slippage
5. delayed fills
6. partial fills
7. no-fill when liquidity insufficient

If performance exists only under ideal fills, the strategy is not execution-realistic.

---

## 17. Latency Stress Test

Add delays:

```text
0 bars
1 bar
2 bars
5 bars
```

or for event-driven systems:

```text
10 ms
50 ms
100 ms
500 ms
1 s
5 s
```

Review how Sharpe, PnL, and turnover change.

---

## 18. Randomized Signal Test

Randomly permute signals while preserving approximate turnover.

The real strategy should outperform randomized strategies.

If randomized signals have similar Sharpe, the result may come from market drift, position bias, or flawed accounting.

---

## 19. Label Permutation Test

Shuffle future returns relative to signals.

Expected:

- alpha should disappear.

If performance remains, the backtest may have accounting or leakage issues.

---

## 20. Bootstrap Confidence Interval

Bootstrap returns or trade outcomes to estimate confidence interval for:

- mean return
- Sharpe
- max drawdown
- hit rate
- expectancy

Do not trust a Sharpe estimate without understanding its uncertainty.

---

## 21. Trade-Level Autopsy

Sort trades by PnL contribution.

Inspect:

- top 10 winning trades
- top 10 losing trades
- PnL concentration
- holding period distribution
- assets responsible for PnL
- dates responsible for PnL

Red flag:

- most PnL comes from one event.

---

## 22. Drawdown Autopsy

For every major drawdown, inspect:

- start date
- trough date
- recovery date
- market regime
- positions held
- signal behavior
- turnover during drawdown
- whether stop/risk logic worked

A strategy is not understood until its drawdowns are understood.

---

## 23. Live Shadow Test

Before paper trading or small live deployment, run a shadow test:

- generate signals in real time
- log hypothetical orders
- record actual bid/ask at decision time
- record theoretical fills
- compare against backtest assumptions

This tests whether the backtest is connected to live market reality.

---

## 24. Paper Trading Reconciliation

Compare paper trading against event-driven backtest replay over the same period.

Check:

- signal equality
- order equality
- fill difference
- fee difference
- slippage difference
- position difference
- PnL difference

If paper trading and backtest disagree, fix infrastructure before trading live.

---

## 25. Kill Criteria

Define before further research:

- minimum forward Sharpe
- maximum drawdown
- maximum cost drag
- maximum turnover
- minimum number of trades
- minimum capacity
- maximum parameter instability
- maximum beta exposure

Example:

```text
Kill the strategy if forward Sharpe < 0.5 after costs,
or if cost drag > 70% of gross PnL,
or if performance is negative in 3 consecutive walk-forward folds.
```

Without kill criteria, research becomes storytelling.
