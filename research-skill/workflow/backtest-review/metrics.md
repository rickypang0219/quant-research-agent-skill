# Backtest Review Metrics

## Metric Philosophy

No single metric proves a strategy is good.

A useful review separates metrics into six groups:

1. return
2. risk
3. drawdown
4. trade quality
5. execution cost
6. robustness

---

## 1. Return Metrics

### Total Return

Measures total compounded return over the backtest.

Problem:

- does not adjust for risk
- can be dominated by long sample length

### Annualized Return

Normalizes return to yearly scale.

Use geometric annualization for realized performance.

### Average Period Return

Useful for checking arithmetic expectations and Sharpe calculation.

---

## 2. Risk Metrics

### Annualized Volatility

Measures standard deviation of returns.

Weakness:

- treats upside and downside volatility equally
- unstable under fat tails

### Sharpe Ratio

Measures excess return per unit volatility.

Weakness:

- sensitive to sample size
- assumes volatility is a meaningful risk proxy
- can be inflated by smoothing, illiquidity, or serial correlation
- does not reveal tail risk

### Sortino Ratio

Uses downside volatility instead of total volatility.

Useful when upside volatility should not be penalized.

### Skewness

Negative skew suggests crash risk or short-volatility exposure.

### Kurtosis

High kurtosis suggests fat tails and jump risk.

### Expected Shortfall

Average loss conditional on being in the tail.

More informative than VaR for tail-heavy strategies.

---

## 3. Drawdown Metrics

### Max Drawdown

Worst peak-to-trough loss.

Key question:

```text
Can the trader survive this drawdown psychologically, financially, and operationally?
```

### Drawdown Duration

How long it takes to recover.

A strategy with acceptable max drawdown but multi-year recovery may be unusable.

### Calmar Ratio

Annual return divided by max drawdown.

Useful for capital allocation.

---

## 4. Trade Quality Metrics

### Number of Trades

Small trade count means weak statistical evidence.

### Hit Rate

Fraction of winning trades.

Must be interpreted with average win/loss.

### Average Win / Average Loss

Shows payoff asymmetry.

### Profit Factor

Gross profit divided by gross loss.

### Expectancy

Expected PnL per trade after costs.

### Holding Period

Compare holding period to signal horizon.

If average holding period is much shorter than expected, turnover may be too high.

---

## 5. Execution Metrics

### Turnover

Measures how much the strategy trades.

High turnover is not bad by itself, but it requires strong execution modeling.

### Cost Drag

Costs divided by gross PnL.

If cost drag is high, small execution errors can destroy the edge.

### Slippage Per Trade

Compare assumed vs realized slippage.

### Fill Rate

For limit-order strategies:

```text
fill_rate = filled_orders / submitted_orders
```

### Participation Rate

```text
participation = traded_quantity / market_volume
```

High participation means impact and capacity matter.

---

## 6. Exposure Metrics

### Gross Exposure

Total absolute exposure.

### Net Exposure

Long exposure minus short exposure.

### Leverage

Gross exposure divided by NAV.

### Beta

Exposure to market benchmark.

### Factor Exposures

Exposure to known risk factors.

### Concentration

Use HHI or effective number of bets.

---

## 7. Robustness Metrics

### Train Sharpe vs Test Sharpe vs Forward Sharpe

Healthy pattern:

```text
train Sharpe > test Sharpe ≈ forward Sharpe > 0
```

Suspicious pattern:

```text
train Sharpe very high, forward Sharpe negative
```

### Parameter Stability

Good strategies have broad parameter regions.

### Regime Stability

Check performance across market regimes.

### Bootstrap Confidence Interval

Estimate uncertainty of Sharpe and mean return.

---

## 8. Suggested Minimum Metric Table

| Category | Metric | Required? |
|---|---|---|
| Return | total return | yes |
| Return | annualized return | yes |
| Risk | annualized volatility | yes |
| Risk | Sharpe | yes |
| Risk | Sortino | recommended |
| Drawdown | max drawdown | yes |
| Drawdown | drawdown duration | recommended |
| Drawdown | Calmar | recommended |
| Trade | number of trades | yes |
| Trade | hit rate | yes |
| Trade | profit factor | yes |
| Trade | expectancy | yes |
| Execution | turnover | yes |
| Execution | cost drag | yes |
| Execution | average slippage | yes if intraday |
| Execution | fill rate | yes if limit orders |
| Exposure | gross exposure | yes |
| Exposure | net exposure | yes |
| Exposure | beta | recommended |
| Tail | skewness | recommended |
| Tail | expected shortfall | recommended |
| Robustness | train/test/forward Sharpe | yes |
| Robustness | parameter stability | yes |
| Robustness | regime split | yes |

---

## 9. Metric Interpretation Rules

### High Sharpe Does Not Automatically Mean Good

Ask:

- how many trades?
- after costs?
- out-of-sample?
- stable parameters?
- realistic fills?
- realistic capacity?

### Low Drawdown May Be Fake

Drawdown can be understated by:

- stale prices
- smoothed marks
- missing costs
- illiquid fills
- unrealized losses hidden by marking assumptions

### High Hit Rate Can Be Dangerous

High hit-rate strategies may have rare large losses.

Check skewness, max loss, and expected shortfall.

### Strong Net PnL With Huge Turnover Needs Execution Proof

If turnover is large, the backtest must become event-driven before being trusted.
