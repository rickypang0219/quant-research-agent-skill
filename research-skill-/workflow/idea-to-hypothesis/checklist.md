# Idea to Hypothesis Checklist

Before accepting any quant idea, check these gates.

## Market Logic

- [ ] Is there a real market mechanism?
- [ ] Can I explain who loses money and who makes money?
- [ ] Is this caused by behavior, liquidity, risk premium, structure, or microstructure?
- [ ] Why has this not been arbitraged away?
- [ ] Is the effect plausible at my trading horizon?
- [ ] Is the effect structural, or is it likely to decay quickly?

## Data Reality

- [ ] Can the idea be measured?
- [ ] Do I have the required data?
- [ ] Is the data timestamped correctly?
- [ ] Is the data available historically?
- [ ] Is the signal tradable at my frequency?
- [ ] Does the data include realistic bid/ask, fees, funding, and liquidity information where needed?
- [ ] Are there survivorship, selection, or delisting biases?

## Hypothesis Quality

- [ ] Is the hypothesis falsifiable?
- [ ] Is there a clear prediction?
- [ ] Is there a clear horizon?
- [ ] Is there a null hypothesis?
- [ ] Is there a baseline comparison?
- [ ] Can the hypothesis be rejected by a simple first experiment?
- [ ] Is the target variable defined before looking at the results?

## Strategy Reality

- [ ] Does it survive fees?
- [ ] Does it survive slippage?
- [ ] Does it survive funding costs?
- [ ] Does it survive liquidity constraints?
- [ ] Does it survive out-of-sample testing?
- [ ] Does it survive volatility regime changes?
- [ ] Is turnover reasonable?
- [ ] Is position sizing clearly defined?

## Live Trading Reality

- [ ] Is turnover reasonable?
- [ ] Is latency relevant?
- [ ] Is exchange risk relevant?
- [ ] Is there a kill switch?
- [ ] Can this be monitored?
- [ ] Can failure be detected quickly?
- [ ] Are orders, positions, fills, and balances reconciled?
- [ ] Is the idea ready for paper trading before real capital?

## Mandatory Decision

At the end of the workflow, classify the idea as one of:

```text
REJECT
REFINE
TEST
PROTOTYPE
PAPER TRADE
DO NOT LIVE TRADE
```
