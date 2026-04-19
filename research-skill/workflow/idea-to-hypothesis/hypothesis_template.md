# Hypothesis Template

Use this template to convert a raw idea into a falsifiable quant research hypothesis.

## 1. Raw Idea

```text
[Write the original idea in the user's language.]
```

## 2. Plain Market Translation

```text
[Translate the analogy / intuition into market behavior.]
```

## 3. Market Mechanism

Possible mechanism:

```text
behavioral / structural / liquidity / volatility / funding / microstructure / statistical
```

Questions:

- Who is trading?
- Who is forced to trade?
- Who provides liquidity?
- Who consumes liquidity?
- Why should this pattern persist?
- Why should it not be arbitraged away?

## 4. Observable Variables

| Concept | Proxy | Formula | Data needed |
|---|---|---|---|
|  |  |  |  |

## 5. Falsifiable Hypothesis

```text
When [condition],
then [future outcome],
over [horizon],
after [cost/risk adjustment],
relative to [baseline].
```

## 6. Null Hypothesis

```text
The effect is zero after costs and risk adjustment.
```

Alternative nulls:

```text
The signal is only beta.
The signal is only volatility exposure.
The signal is only momentum.
The signal is caused by lookahead bias.
The signal disappears out-of-sample.
```

## 7. Minimum Test

```text
Feature:
Target:
Horizon:
Universe:
Sample:
Metric:
Success criterion:
```

## 8. Backtest Design

```text
Entry:
Exit:
Sizing:
Rebalance:
Fees:
Slippage:
Risk limits:
Data split:
Walk-forward method:
```

## 9. Failure Modes

```text
1.
2.
3.
```

Common failure modes:

- Signal is too weak after fees.
- Signal is only beta.
- Signal is only volatility exposure.
- Signal is unstable across regimes.
- Signal requires unrealistic liquidity.
- Signal has too much turnover.
- Signal is contaminated by lookahead bias.
- Signal works only in one historical period.

## 10. Decision

```text
REJECT / REFINE / TEST / PROTOTYPE / PAPER TRADE / DO NOT LIVE TRADE
```

Reason:

```text
[Explain why this decision was made.]
```
