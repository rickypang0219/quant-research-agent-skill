# Backtest Review Report Template

## Strategy Name

`<strategy_name>`

## Review Date

`<YYYY-MM-DD>`

## Reviewer Verdict

- Status: `PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE`
- Confidence: `Low / Medium / High`
- Recommended next step: `abandon / fix accounting / run robustness / event-driven backtest / paper trade / small live`

---

## 1. Strategy Summary

### Hypothesis

What market behavior is this strategy trying to exploit?

### Instruments

What assets/contracts are traded?

### Timeframe

What bar/tick frequency is used?

### Entry Rule

Exact rule.

### Exit Rule

Exact rule.

### Position Sizing

Exact rule.

### Rebalance Frequency

Exact rule.

---

## 2. Data Review

### Data Source

### Data Period

### Raw Data Location

### Cleaned Data Location

### Feature Data Location

### Missing Data Handling

### Universe Construction

### Data Bias Risks

- Survivorship bias:
- Look-ahead bias:
- Selection bias:
- Corporate action / contract roll issue:
- Delisting issue:

### Data Verdict

`PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE`

---

## 3. PnL Accounting Review

### Position Unit

`quantity / notional / weight / target weight / other`

### PnL Formula

```text
<insert formula>
```

### Cost Formula

```text
<insert formula>
```

### Fill Price Formula

```text
<insert formula>
```

### Accounting Checks

- Previous position used for PnL? `Yes/No`
- Position lag correct? `Yes/No`
- Costs charged on delta position? `Yes/No`
- Fees included? `Yes/No`
- Slippage included? `Yes/No`
- Spread included? `Yes/No`
- Funding/borrow included? `Yes/No/Not Applicable`
- Cash reconciliation works? `Yes/No`

### Accounting Verdict

`PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE`

---

## 4. Execution Assumption Review

### Order Type

`market / limit / stop / mixed`

### Fill Assumption

### Latency Assumption

### Slippage Assumption

### Spread Assumption

### Volume / Capacity Assumption

### Execution Red Flags

### Execution Verdict

`PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE`

---

## 5. Validation Review

### Parameter Search Method

`manual / grid search / Optuna / Bayesian / other`

### Train Period

### Validation Period

### Forward Test Period

### Walk-Forward Design

### Number of Parameter Trials

### Parameter Stability

### Data-Snooping Risk

### Validation Verdict

`PASS / CONDITIONAL PASS / FAIL / INSUFFICIENT EVIDENCE`

---

## 6. Performance Summary

| Metric | Gross | Net | Comment |
|---|---:|---:|---|
| Total return | | | |
| Annualized return | | | |
| Annualized volatility | | | |
| Sharpe | | | |
| Sortino | | | |
| Max drawdown | | | |
| Calmar | | | |
| Hit rate | | | |
| Profit factor | | | |
| Turnover | | | |
| Cost drag | | | |
| Number of trades | | | |
| Average holding period | | | |
| Skewness | | | |
| Expected shortfall | | | |

---

## 7. Robustness Tests

| Test | Result | Verdict |
|---|---|---|
| 1-bar delay | | |
| 2-bar delay | | |
| 2x cost | | |
| 5x cost | | |
| spread stress | | |
| parameter perturbation | | |
| start-date perturbation | | |
| universe perturbation | | |
| walk-forward | | |
| regime split | | |

---

## 8. Red Flags

### Critical

1.
2.
3.

### Medium

1.
2.
3.

### Minor

1.
2.
3.

---

## 9. What Would Falsify This Strategy?

Define concrete failure conditions.

Example:

```text
The strategy is rejected if forward Sharpe < 0.5 after realistic costs,
or if net PnL becomes negative under 2x slippage,
or if walk-forward performance is positive in fewer than 50% of folds.
```

---

## 10. Required Next Experiments

1.
2.
3.

---

## 11. Final Decision

### Can continue research?

`Yes/No`

### Can move to event-driven backtest?

`Yes/No`

### Can paper trade?

`Yes/No`

### Can trade small live capital?

`Yes/No`

### Final Comment

Write the blunt truth here.
