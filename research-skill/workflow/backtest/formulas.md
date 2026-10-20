# Backtesting Formulas

## 1. Returns

Simple return:

```math
r_t = \frac{P_t - P_{t-1}}{P_{t-1}}
```

Log return:

```math
x_t = \log P_t - \log P_{t-1}
```

For a multi-asset universe:

```math
\mathbf{r}_t = (r_{1,t}, r_{2,t}, \dots, r_{N,t})^\top
```

---

## 2. Signal, Position, and Look-Ahead Safety

A signal must be computed from information available at or before time `t`:

```math
s_t = f(\mathcal{F}_t)
```

If the trade is executed on the next bar, then:

```math
w_{t+1} = g(s_t)
```

PnL from `t` to `t+1` should use the previous executable position:

```math
\text{PnL}_{t+1} = w_{t+1} r_{t+1}
```

In code, this usually means:

```python
signal = compute_signal(data).shift(1)
position = position_rule(signal)
pnl = position.shift(1) * returns
```

The exact shift depends on when the signal is observed and when the order is filled.

---

## 3. Single-Asset Price-Change PnL

Let:

```math
q_t = \text{target quantity after rebalance at time } t
```

Then price-change PnL from last quantity is:

```math
\text{PricePnL}_t = q_{t-1}(P_t - P_{t-1})
```

Transaction cost:

```math
\text{Cost}_t = |q_t - q_{t-1}| P_t c
```

where `c` is the proportional fee/slippage rate.

Net PnL:

```math
\text{PnL}_t = q_{t-1}(P_t - P_{t-1}) - |q_t - q_{t-1}| P_t c
```

This is the correct style when the position is stored in quantity units.

---

## 4. Target Quantity from USD Notional

If target position is in USD/USDT notional:

```math
V_t = \text{target notional}
```

then:

```math
q_t = \frac{V_t}{P_t}
```

For a long position, `V_t > 0`.

For a short position, `V_t < 0`.

---

## 5. Multi-Asset Portfolio PnL

Let:

```math
\mathbf{q}_t = (q_{1,t}, \dots, q_{N,t})^\top
```

```math
\mathbf{P}_t = (P_{1,t}, \dots, P_{N,t})^\top
```

Price PnL:

```math
\text{PricePnL}_t =
\mathbf{q}_{t-1}^\top(\mathbf{P}_t - \mathbf{P}_{t-1})
```

Transaction cost:

```math
\text{Cost}_t =
\sum_{i=1}^N |q_{i,t} - q_{i,t-1}| P_{i,t} c_i
```

Net PnL:

```math
\text{PnL}_t =
\mathbf{q}_{t-1}^\top(\mathbf{P}_t - \mathbf{P}_{t-1})
-
\sum_{i=1}^N |q_{i,t} - q_{i,t-1}| P_{i,t} c_i
```

---

## 6. Turnover

Dollar turnover:

```math
\text{Turnover}_t =
\sum_{i=1}^N |q_{i,t} - q_{i,t-1}| P_{i,t}
```

Portfolio turnover relative to gross exposure:

```math
\text{TurnoverRate}_t =
\frac{\sum_i |q_{i,t} - q_{i,t-1}|P_{i,t}}
{\sum_i |q_{i,t-1}|P_{i,t}}
```

High turnover strategies must be punished hard in cost stress tests.

---

## 7. Equity Curve

Starting capital:

```math
E_0
```

Equity:

```math
E_t = E_{t-1} + \text{PnL}_t
```

Return on equity:

```math
R_t = \frac{\text{PnL}_t}{E_{t-1}}
```

---

## 8. Sharpe Ratio

Mean return:

```math
\bar{R} = \frac{1}{T}\sum_{t=1}^T R_t
```

Sample volatility:

```math
\sigma_R = \sqrt{\frac{1}{T-1}\sum_{t=1}^T(R_t-\bar{R})^2}
```

Per-period Sharpe:

```math
SR = \frac{\bar{R}}{\sigma_R}
```

Naive annualized Sharpe:

```math
SR_{\text{ann}} = \sqrt{K} \frac{\bar{R}}{\sigma_R}
```

where `K` is periods per year:

```text
daily crypto: 365
hourly crypto: 365 * 24
15m crypto: 365 * 24 * 4
1m crypto: 365 * 24 * 60
US equities daily: 252
```

---

## 9. Serial-Correlation-Adjusted Sharpe

If returns are autocorrelated, naive annualization can overstate Sharpe.

Let `q` be the number of periods in the annualization block and let `rho_k` be return autocorrelation at lag `k`.

Adjustment factor:

```math
A_q =
\sqrt{
q + 2 \sum_{k=1}^{q-1}(q-k)\rho_k
}
```

Adjusted annualized Sharpe:

```math
SR_{\text{adj}} =
\frac{q \bar{R}}{\sigma_R A_q}
```

Equivalent form:

```math
SR_{\text{adj}} =
\frac{\sqrt{q}\bar{R}/\sigma_R}
{\sqrt{1 + 2\sum_{k=1}^{q-1}(1-k/q)\rho_k}}
```

---

## 10. Sortino Ratio

Downside deviation:

```math
\sigma_- =
\sqrt{
\frac{1}{T}
\sum_{t=1}^T \min(R_t - R_f, 0)^2
}
```

Sortino:

```math
\text{Sortino} =
\frac{\bar{R} - R_f}{\sigma_-}
```

---

## 11. Maximum Drawdown

Running peak:

```math
M_t = \max_{u \le t} E_u
```

Drawdown:

```math
D_t = \frac{E_t - M_t}{M_t}
```

Maximum drawdown:

```math
\text{MDD} = \min_t D_t
```

---

## 12. Calmar Ratio

```math
\text{Calmar} =
\frac{\text{Annualized Return}}
{|\text{Maximum Drawdown}|}
```

---

## 13. Hit Rate and Payoff Ratio

Hit rate:

```math
p = \frac{\#\{\text{winning trades}\}}{\#\{\text{all trades}\}}
```

Average win:

```math
\bar{W}
```

Average loss magnitude:

```math
\bar{L}
```

Expected trade PnL:

```math
E[\text{trade}] = p\bar{W} - (1-p)\bar{L}
```

A strategy can be profitable with low hit rate if payoff ratio is high.

---

## 14. Z-Score Signal

Rolling mean:

```math
\mu_t = \frac{1}{L}\sum_{i=t-L+1}^t X_i
```

Rolling standard deviation:

```math
\sigma_t =
\sqrt{
\frac{1}{L-1}
\sum_{i=t-L+1}^t(X_i-\mu_t)^2
}
```

Z-score:

```math
z_t = \frac{X_t - \mu_t}{\sigma_t}
```

Mean-reversion example:

```text
long if z_t < -z_entry
exit long if z_t >= -z_exit
short if z_t > z_entry
exit short if z_t <= z_exit
```

---

## 15. Percentile Rank Signal

For window `L`:

```math
u_t =
\frac{1}{L}
\sum_{i=t-L+1}^t
\mathbf{1}\{X_i \le X_t\}
```

Mean-reversion:

```text
long if percentile < 0.05
short if percentile > 0.95
```

Momentum:

```text
long if percentile > 0.95
short if percentile < 0.05
```

---

## 16. Rate of Change

```math
ROC_t(L) = \frac{P_t - P_{t-L}}{P_{t-L}}
```

or:

```math
ROC_t(L) = \log P_t - \log P_{t-L}
```

---

## 17. Volatility Targeting

Estimated volatility:

```math
\hat{\sigma}_t =
\sqrt{K}
\operatorname{std}(R_{t-L+1}, \dots, R_t)
```

Target leverage:

```math
\ell_t =
\frac{\sigma_{\text{target}}}{\hat{\sigma}_t}
```

Capped leverage:

```math
\ell_t =
\min(\ell_{\max}, \ell_t)
```

Position:

```math
w_t = \ell_t s_t
```

---

## 18. Funding PnL for Perpetual Futures

If position notional is `V_t` and funding rate paid at timestamp `τ` is `F_τ`:

```math
\text{FundingPnL}_\tau = -V_{\tau^-} F_\tau
```

Sign convention depends on exchange. Always verify:

```text
long pays when funding > 0
short receives when funding > 0
```

for the specific venue.

---

## 19. Slippage Model

Flat bps slippage:

```math
\text{SlippageCost}_t =
|\Delta q_t| P_t s
```

Spread-based slippage:

```math
\text{BuyFill} = Ask_t
```

```math
\text{SellFill} = Bid_t
```

Half-spread approximation:

```math
\text{SpreadCost}_t =
|\Delta q_t| \frac{Ask_t - Bid_t}{2}
```

---

## 20. Linear Market Impact

For trade notional `Q_t` and participation rate:

```math
\pi_t = \frac{|Q_t|}{ADV_t}
```

A simple impact model:

```math
\text{ImpactBps}_t = a + b\pi_t
```

Cost:

```math
\text{ImpactCost}_t =
|Q_t| \cdot \frac{\text{ImpactBps}_t}{10^4}
```

For crypto, use rolling dollar volume over a relevant horizon instead of ADV if trading intraday.

---

## 21. Square-Root Market Impact

Common empirical form:

```math
\text{Impact}_t =
Y \sigma_t \sqrt{\frac{|Q_t|}{V_t}}
```

where:

- `Y` is impact coefficient
- `sigma_t` is volatility
- `Q_t` is trade size
- `V_t` is volume over the execution horizon

This is more realistic for larger orders, but harder to calibrate.

---

## 22. Limit Order Fill Probability

Toy model:

```math
P(\text{fill before cancel}) =
1 - \exp(-\lambda \Delta t)
```

where `λ` depends on:

- queue position
- market order arrival rate
- cancel rate ahead of you
- distance from mid
- spread state
- volatility
- toxicity/order-flow imbalance

This is not enough for production, but useful for sensitivity testing.

---

## 23. Avellaneda-Stoikov Reservation Price

For market making intuition:

```math
r_t = S_t - q_t \gamma \sigma^2 (T-t)
```

where:

- `S_t` is mid price
- `q_t` is inventory
- `γ` is risk aversion
- `σ` is volatility
- `T-t` is remaining horizon

Interpretation:

```text
If inventory is long, reservation price moves lower to encourage selling.
If inventory is short, reservation price moves higher to encourage buying.
```

This belongs more to event-driven simulation than to simple vectorized backtesting.

---

## 24. Probability of Backtest Overfitting — Conceptual CSCV

Given many candidate strategies or parameter sets:

1. Split data into many combinations of train/test folds.
2. For each split, choose the best strategy in-sample.
3. Measure its rank out-of-sample.
4. Convert OOS rank to a logit score.
5. Estimate:

```math
PBO = P(\lambda < 0)
```

where negative `λ` means the selected in-sample winner performs worse than median out-of-sample.

Use this when many parameter combinations have been tried.

---

## 25. Probabilistic Sharpe Ratio

Approximate form:

```math
PSR(SR^*) =
\Phi
\left(
\frac{(\widehat{SR} - SR^*)\sqrt{T-1}}
{\sqrt{
1 - \hat{\gamma}_3 \widehat{SR}
+
\frac{\hat{\gamma}_4 - 1}{4}\widehat{SR}^2
}}
\right)
```

where:

- `SR*` is benchmark Sharpe
- `γ3` is skewness
- `γ4` is kurtosis
- `T` is number of observations
- `Φ` is normal CDF

This adjusts the confidence in a Sharpe estimate for non-normality.

---

## 26. Deflated Sharpe Ratio

The Deflated Sharpe Ratio applies the PSR idea after increasing the benchmark Sharpe to reflect multiple testing.

Conceptually:

```math
DSR =
PSR(SR^*_{\text{multiple trials}})
```

Use when the research process tested many variants.

---

## 27. White Reality Check

Let `d_{k,t}` be the performance difference between strategy `k` and benchmark at time `t`.

Mean performance:

```math
\bar{d}_k = \frac{1}{T}\sum_{t=1}^T d_{k,t}
```

The test statistic uses the best observed model:

```math
T_{\max} =
\max_k \sqrt{T}\bar{d}_k
```

Bootstrap the distribution of this maximum to correct for data snooping across many tested strategies.

---

## 28. Hansen Superior Predictive Ability Test

The SPA test improves on the Reality Check by reducing the influence of poor and irrelevant alternatives.

Conceptually:

```text
Reality Check:
    Is the best model truly better after accounting for all tried models?

SPA:
    Same question, but with a more powerful test statistic and less penalty from obviously bad models.
```

Use for large grids of technical rules or parameter variants.

---

## 29. Purging and Embargo

If a label from time `t` uses future data until `t+h`, then training examples overlapping a test window leak information.

Purging:

```text
Remove training samples whose label window overlaps the test window.
```

Embargo:

```text
Remove a buffer of training samples immediately after the test window.
```

This is crucial for overlapping returns, triple-barrier labels, and many medium-frequency strategies.

---

## 30. Decision Thresholds

A strategy is not promoted just because Sharpe is positive.

A stronger checklist:

```text
OOS Sharpe > 0 after conservative costs
max drawdown acceptable
turnover plausible
parameter plateau exists
performance not concentrated in one regime
capacity not obviously tiny
event-driven simulation does not destroy edge
paper trading resembles backtest
```
