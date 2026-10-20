# Backtest Review Formulas

## 1. Price Return

Simple return:

```text
r_t = P_t / P_{t-1} - 1
```

Log return:

```text
r_t = log(P_t / P_{t-1})
```

Use simple returns for portfolio compounding and accounting. Use log returns for modeling when additivity is useful.

---

## 2. Position-Based PnL

For asset `i`:

```text
price_pnl_{i,t} = q_{i,t-1} * (P_{i,t} - P_{i,t-1})
```

Portfolio price PnL:

```text
price_pnl_t = sum_i q_{i,t-1} * (P_{i,t} - P_{i,t-1})
```

The previous position earns the current price change. This is the most important anti-look-ahead rule.

---

## 3. Target Notional to Quantity

If target position is defined in USD/USDT notional:

```text
target_qty_{i,t} = target_notional_{i,t} / fill_price_{i,t}
```

Trade quantity:

```text
delta_qty_{i,t} = target_qty_{i,t} - q_{i,t-1}
```

---

## 4. Transaction Cost

Percentage fee model:

```text
fee_{i,t} = abs(delta_qty_{i,t}) * fill_price_{i,t} * fee_rate_i
```

Portfolio fee:

```text
fee_t = sum_i fee_{i,t}
```

If maker/taker fees differ:

```text
fee_{i,t} = abs(delta_qty_maker_{i,t}) * fill_price_{i,t} * maker_fee_i
          + abs(delta_qty_taker_{i,t}) * fill_price_{i,t} * taker_fee_i
```

---

## 5. Spread Cost

Approximate spread crossing cost for market orders:

```text
spread_cost_{i,t} = abs(delta_qty_{i,t}) * half_spread_{i,t}
```

where:

```text
half_spread_t = (ask_t - bid_t) / 2
```

For a market buy:

```text
fill_price_t ≈ ask_t
```

For a market sell:

```text
fill_price_t ≈ bid_t
```

Never assume market orders fill at mid price unless spread cost is explicitly added.

---

## 6. Slippage Model

Simple bps slippage:

```text
slippage_cost_{i,t} = abs(delta_qty_{i,t}) * fill_price_{i,t} * slippage_bps / 10_000
```

Volatility-scaled slippage:

```text
slippage_cost_{i,t} = abs(delta_notional_{i,t}) * k * sigma_{i,t}
```

Participation-rate slippage:

```text
participation_{i,t} = abs(delta_qty_{i,t}) / market_volume_{i,t}
slippage_bps_{i,t} = a + b * participation_{i,t}
```

Square-root impact approximation:

```text
impact_bps_{i,t} = Y * sigma_{i,t} * sqrt(abs(delta_notional_{i,t}) / ADV_{i,t})
```

---

## 7. Net PnL

```text
net_pnl_t = price_pnl_t
          - fees_t
          - spread_cost_t
          - slippage_cost_t
          - funding_cost_t
          - borrow_cost_t
          - financing_cost_t
```

Gross PnL must always be separated from cost components.

---

## 8. Portfolio Value

```text
NAV_t = NAV_{t-1} + net_pnl_t
```

Portfolio return:

```text
R_t = net_pnl_t / NAV_{t-1}
```

Do not divide by `NAV_t`; that introduces a small timing inconsistency.

---

## 9. Weight-Based PnL

If `w_{i,t-1}` is previous portfolio weight:

```text
R_t = sum_i w_{i,t-1} * r_{i,t} - cost_t / NAV_{t-1}
```

If weights are target weights, they should usually be shifted before applying returns:

```text
R_t = sum_i target_w_{i,t-1} * r_{i,t}
```

---

## 10. Turnover

For quantity-based backtest:

```text
turnover_notional_t = sum_i abs(delta_qty_{i,t}) * fill_price_{i,t}
turnover_ratio_t = turnover_notional_t / NAV_{t-1}
```

For weight-based backtest:

```text
turnover_t = sum_i abs(w_{i,t} - w_{i,t-1}^{drifted})
```

Approximate drifted weight:

```text
w_{i,t-1}^{drifted} = w_{i,t-1} * (1 + r_{i,t}) / (1 + R_t^{pre_trade})
```

---

## 11. Annualized Return

For periodic returns `R_t` with `N` periods per year:

Arithmetic approximation:

```text
ann_return ≈ mean(R_t) * N
```

Geometric annualized return:

```text
ann_return = (prod_t (1 + R_t))^{N / T} - 1
```

Use geometric return for reporting realized performance.

---

## 12. Annualized Volatility

```text
ann_vol = std(R_t) * sqrt(N)
```

For crypto:

```text
N = 365          for daily bars
N = 365 * 24     for hourly bars
N = 365 * 24 * 4 for 15-minute bars
```

For US equities:

```text
N = 252          for daily bars
```

Use the correct trading calendar.

---

## 13. Sharpe Ratio

```text
Sharpe = mean(R_t - rf_t) / std(R_t - rf_t) * sqrt(N)
```

For high-frequency crypto, risk-free rate is often negligible over one bar but should still be considered for longer horizons.

Danger signs:

- high Sharpe with tiny sample
- high Sharpe before costs only
- Sharpe collapses after slippage
- Sharpe concentrated in one month
- Sharpe created by one parameter spike

---

## 14. Sortino Ratio

```text
Sortino = mean(R_t - MAR) / downside_std(R_t) * sqrt(N)
```

where:

```text
downside_std = std(min(R_t - MAR, 0))
```

Use Sortino when downside risk matters more than symmetric volatility.

---

## 15. Max Drawdown

Equity curve:

```text
E_t = E_0 * prod_{s<=t} (1 + R_s)
```

Running peak:

```text
Peak_t = max_{s<=t} E_s
```

Drawdown:

```text
DD_t = E_t / Peak_t - 1
```

Maximum drawdown:

```text
MDD = min_t DD_t
```

---

## 16. Calmar Ratio

```text
Calmar = annualized_return / abs(max_drawdown)
```

Useful for strategies where drawdown is more meaningful than daily volatility.

---

## 17. Hit Rate

```text
hit_rate = number_of_profitable_trades / number_of_trades
```

Hit rate alone is not enough. A strategy can have low hit rate and still be profitable if winners are much larger than losers.

---

## 18. Profit Factor

```text
profit_factor = gross_profit / abs(gross_loss)
```

Danger signs:

- profit factor driven by one massive trade
- profit factor before costs only
- profit factor unstable across regimes

---

## 19. Expectancy Per Trade

```text
expectancy = hit_rate * avg_win - (1 - hit_rate) * avg_loss
```

where `avg_loss` is a positive number representing loss magnitude.

After costs:

```text
net_expectancy = avg_net_pnl_per_trade
```

---

## 20. Exposure

Gross exposure:

```text
gross_exposure_t = sum_i abs(notional_{i,t}) / NAV_t
```

Net exposure:

```text
net_exposure_t = sum_i notional_{i,t} / NAV_t
```

Market beta exposure:

```text
beta_p,t = cov(R_p, R_m) / var(R_m)
```

For a market-neutral strategy, check both dollar neutrality and beta neutrality.

---

## 21. Concentration

Herfindahl-Hirschman Index:

```text
HHI_t = sum_i w_{i,t}^2
```

Effective number of bets:

```text
N_eff_t = 1 / HHI_t
```

A strategy with 50 assets but `N_eff = 3` is concentrated.

---

## 22. Tail Risk

Value at Risk at level `alpha`:

```text
VaR_alpha = quantile(R_t, alpha)
```

Expected shortfall:

```text
ES_alpha = mean(R_t | R_t <= VaR_alpha)
```

For crypto and intraday strategies, inspect tails directly. Gaussian assumptions are often too optimistic.

---

## 23. Cost Drag

```text
cost_drag = total_costs / gross_profit
```

or:

```text
cost_drag_return = sum(cost_t) / initial_NAV
```

If costs consume most of gross PnL, the strategy is fragile.

---

## 24. Capacity

Simple ADV capacity estimate:

```text
max_trade_notional_i = participation_limit * ADV_i
```

Strategy capacity:

```text
capacity ≈ min_i max_trade_notional_i / required_weight_i
```

For intraday strategies, use volume over the intended execution window, not daily volume.

---

## 25. Parameter Robustness

Given parameter vector `theta`, evaluate performance surface:

```text
S(theta) = Sharpe(theta)
```

Robust parameter region means nearby parameters also work:

```text
S(theta + epsilon) remains acceptable for small epsilon
```

Reject strategies where performance exists only at one isolated parameter point.

---

## 26. Train/Test/Forward Split

Example split:

```text
Train / parameter search:  2020-01-01 to 2023-12-31
Validation:                2024-01-01 to 2024-12-31
Forward test:              2025-01-01 to 2026-01-01
```

Rules:

- choose parameters only on train/validation
- touch forward test once
- do not retune after seeing forward result
- if retuned, create a new untouched forward period

---

## 27. Walk-Forward Testing

At each step `k`:

```text
train on [t_0, t_k]
select parameters theta_k
test on (t_k, t_{k+1}]
roll forward
```

Aggregate all out-of-sample windows into one forward equity curve.

---

## 28. Deflated Thinking for Sharpe

Observed Sharpe is inflated by:

- small sample size
- non-normal returns
- many parameter trials
- selecting the best run
- serial correlation
- reporting only successful experiments

Backtest review should always discount the observed Sharpe unless the experiment design controls for these effects.
