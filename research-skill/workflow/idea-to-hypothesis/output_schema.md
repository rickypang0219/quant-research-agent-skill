# Standard Output Schema

When using the idea-to-hypothesis workflow, respond in this format.

## 1. Idea Restatement

Restate the user's raw idea clearly.

## 2. Plain Market Translation

Translate the idea into practical market language. Avoid unnecessary abstraction.

## 3. Professor Routing

| Module | Role |
|---|---|
| Strang |  |
| Lo |  |
| Brunton |  |
| Simons |  |
| Quant Trading System |  |

Only include modules that are relevant.

## 4. Market Mechanism

Explain why the effect might exist. Address:

- who trades
- who provides liquidity
- who consumes liquidity
- why the pattern might persist
- why it might decay
- whether it is behavioral, structural, liquidity-driven, volatility-driven, funding-driven, microstructure-driven, or statistical

## 5. Observable Variables

| Concept | Observable | Formula/Data |
|---|---|---|
|  |  |  |

Every abstract concept must map to a measurable proxy.

## 6. Falsifiable Hypothesis

Use this form:

```text
When [condition],
then [future outcome],
over [horizon],
after [cost/risk adjustment],
relative to [baseline].
```

## 7. Null Hypothesis

State the boring explanation.

Examples:

```text
The effect is zero after costs.
The signal is only beta.
The signal is only volatility exposure.
The signal is only momentum.
The signal disappears out-of-sample.
```

## 8. Minimum Viable Experiment

Include:

```text
Data:
Feature:
Target:
Horizon:
Universe:
Sample period:
Metric:
Success criterion:
```

## 9. Backtest Design

Include:

```text
Entry:
Exit:
Sizing:
Rebalance:
Fees:
Slippage:
Risk limits:
Train/test split:
Walk-forward method:
```

## 10. Risk and Cost Assumptions

Explicitly define:

- maker/taker fees
- slippage
- spread
- funding
- latency
- liquidity filter
- position limits
- turnover limits
- drawdown limits

## 11. Failure Modes

List at least five.

Examples:

```text
1. Lookahead bias
2. Timestamp alignment error
3. Signal is only beta
4. Signal dies after fees
5. Signal works only in one regime
```

## 12. Next Step

Give one concrete next action.

Examples:

```text
Compute a bucket test.
Run an event study.
Build a minimum viable backtest.
Reject because the idea has no observable variable.
Refine the hypothesis because the mechanism is unclear.
```

## 13. Decision

End with exactly one decision:

```text
REJECT
REFINE
TEST
PROTOTYPE
PAPER TRADE
DO NOT LIVE TRADE
```

Add a one-paragraph explanation.
