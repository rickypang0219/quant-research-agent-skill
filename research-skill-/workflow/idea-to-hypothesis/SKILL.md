---
name: idea-to-hypothesis
description: Use when a raw quant trading idea, market analogy, mathematical intuition, or vague observation needs to be converted into a falsifiable, data-driven trading hypothesis with observable variables, testable predictions, required data, failure modes, and a minimum viable experiment.
---

# Idea to Hypothesis Workflow

## Purpose

Convert vague trading ideas into clear research hypotheses. Use this workflow when the user says:

- "I have an idea..."
- "Can we model this as..."
- "Maybe returns behave like..."
- "What if market regime is..."
- "Can I use physics / geometry / topology / ML to explain..."
- "Is this tradable?"
- "How do I test this?"

The goal is not to praise the idea. The goal is to pressure-test it and turn it into something testable with data.

## Core Principle

A quant idea is not useful until it becomes:

```text
market intuition
→ observable variables
→ falsifiable hypothesis
→ measurable signal
→ backtestable strategy
→ risk-controlled experiment
```

Always separate:

```text
analogy ≠ model
model ≠ signal
signal ≠ strategy
strategy ≠ live edge
```

## Required Output

For every raw idea, produce:

1. Raw idea restatement
2. Market mechanism
3. Why it might work
4. Why it might be wrong
5. Observable variables
6. Falsifiable hypothesis
7. Null hypothesis
8. Data required
9. Feature construction
10. Minimum viable experiment
11. Backtest design
12. Risk / transaction cost assumptions
13. Failure modes
14. Decision rule: reject, refine, or continue

## Workflow

### Step 1 — Restate the Raw Idea

Rewrite the idea in plain market language. Avoid poetic or theoretical language unless it maps to measurable variables.

Bad:

> Market fluctuations are like quantum ground-state excitations.

Better:

> Most small returns are noise around a latent equilibrium state, while large non-zero returns may represent regime excitations or order-flow shocks.

### Step 2 — Identify the Market Mechanism

Ask:

- Who is forced to trade?
- Who has information?
- Who provides liquidity?
- Who consumes liquidity?
- Why should this pattern persist?
- Why should it not be arbitraged away?
- Is this behavioral, structural, microstructural, or statistical?

Classify the hypothesis:

```text
[ ] behavioral
[ ] structural
[ ] liquidity-driven
[ ] volatility-driven
[ ] funding/carry-driven
[ ] microstructure-driven
[ ] cross-sectional
[ ] time-series
[ ] regime-dependent
[ ] pure statistical artifact
```

### Step 3 — Translate Concepts into Observables

Every abstract word must become a measurable variable.

| Abstract concept | Observable proxy |
|---|---|
| market stress | realized volatility, drawdown, spread widening |
| crowding | correlation spike, factor beta concentration |
| liquidity shock | order-book imbalance, spread, depth collapse |
| excitation | large return relative to local volatility |
| equilibrium | rolling mean, VWAP, POC, fair-value estimate |
| regime | volatility state, PCA eigenvalue shift, HMM state |
| memory | autocorrelation, AR coefficient, half-life |
| disorder | entropy, dispersion, cross-sectional volatility |

### Step 4 — Write the Falsifiable Hypothesis

A valid hypothesis must have this form:

```text
When [condition] occurs,
then [measurable future outcome] should happen
over [horizon],
after accounting for [costs/risk],
more often or more strongly than [baseline].
```

Example:

```text
When BTC 1h realized volatility is in the top 20% of its 180-day distribution
and cross-sectional crypto correlation rises sharply,
then PCA residual mean-reversion signals should decay faster over the next 24 hours
than during low-volatility regimes.
```

### Step 5 — Define the Null Hypothesis

Every idea needs a boring alternative explanation.

```text
Null 1: The signal has no predictive power after transaction costs.
Null 2: The signal is only volatility exposure.
Null 3: The signal is only BTC beta.
Null 4: The signal disappears out-of-sample.
Null 5: The signal is caused by lookahead bias or survivorship bias.
```

### Step 6 — Minimum Viable Experiment

Design the smallest test that can kill or support the idea.

```text
Data:
- universe
- timeframe
- bar size
- sample period

Feature:
- exact formula

Prediction:
- target variable

Test:
- correlation / regression / bucket test / event study

Success criterion:
- effect has correct sign
- survives costs
- stable across subperiods
- not explained by obvious risk factors
```

### Step 7 — Backtest Only After Signal Evidence

Only proceed to a full strategy backtest after basic evidence exists.

Before backtesting, check:

```text
[ ] no lookahead bias
[ ] no survivorship bias
[ ] timestamp alignment correct
[ ] realistic fees
[ ] realistic slippage
[ ] liquidity filter
[ ] position sizing rule
[ ] turnover constraint
[ ] train/test split
[ ] walk-forward validation
```

### Step 8 — Decision Rule

End every response with one of:

```text
REJECT:
The idea has no clear observable or no plausible mechanism.

REFINE:
The idea is interesting but currently too vague.

TEST:
The idea has a clear hypothesis and minimum experiment.

PROTOTYPE:
The signal has enough evidence to build a strategy prototype.

PAPER TRADE:
The backtest is robust enough for paper trading only.

DO NOT LIVE TRADE:
The idea is not ready for real capital.
```
