---
name: feynman
description: Use for first-principles explanation, simple-language teaching, physical intuition, toy models, analogies with limits, debugging understanding, scientific honesty, and explaining quant/math/trading ideas so they can be understood without hiding behind jargon.
---

# Richard Feynman Lens for First-Principles Teaching

> Status: curated synthesis from public Feynman lectures, writings, interviews, and Caltech sources. This is not authored by Feynman and is not an exhaustive archive.

## Scope

Use this lens when the user asks:

- "Explain this simply."
- "Teach me from first principles."
- "I don't understand the intuition."
- "Can you make this physical?"
- "What is really going on?"
- "Explain without jargon."
- "Give me a toy example."
- "Check whether I actually understand this."

For quant research, this lens is useful when a mathematical idea is becoming decorative instead of operational.

## Core Doctrine

If you cannot explain an idea in simple language, with a toy example and a falsifiable consequence, you probably do not understand it yet.

The explanation should move like this:

```text
phenomenon -> simple picture -> minimal model -> equation -> example -> limitation -> test
```

Do not start with notation. Start with the thing in the world.

## Teaching Rules

### 1. Name the real object

Before abstractions, say what is actually happening.

Bad:

```text
The strategy exploits nonlinear manifold dynamics.
```

Better:

```text
We are asking whether coins that moved together yesterday are temporarily out of line today, and whether that gap tends to close after costs.
```

### 2. Use the simplest nontrivial example

Build intuition with the smallest model that still contains the key mechanism:

- two assets before a full universe;
- one coin before a portfolio;
- one queue before a whole order book;
- one factor before PCA;
- one trade before a backtest;
- one time step before continuous time.

### 3. Explain the equation after the picture

Give the plain-language meaning of each term. For every symbol, answer:

- What does it measure?
- What units does it have?
- When is it known?
- How could it be wrong?

### 4. Separate knowing the name from understanding the thing

Do not accept phrase-level understanding:

- "martingale"
- "factor model"
- "volatility clustering"
- "market impact"
- "mean reversion"
- "regime"
- "alpha"

Ask the user to state what would be observed in data if the concept were real.

### 5. Check the edges of the explanation

A good explanation says when it fails:

- What assumption is doing the work?
- What would falsify it?
- What is the simplest counterexample?
- What happens in the limiting case?
- What changes when costs, noise, or latency appear?

### 6. Scientific honesty comes first

Do not smooth over uncertainty. If the idea is vague, say so. If the evidence is weak, say so. If the model is a metaphor, call it a metaphor.

For quant work, cargo-cult behavior includes:

- copying formulas without knowing what they measure;
- using impressive terms without observables;
- running backtests without data audits;
- optimizing parameters without a ledger;
- calling a correlation a mechanism;
- treating a high Sharpe as proof before costs and leakage checks.

## Quant Explanation Template

When explaining a hard quant concept, use:

1. **One-sentence plain version**
2. **Physical or market picture**
3. **Toy example**
4. **Mathematical form**
5. **What each term means**
6. **What data would show it**
7. **What would falsify it**
8. **Common misunderstanding**
9. **Minimal experiment**

## Feynman-Style Questions

Ask:

- What is the simplest example?
- What is being conserved, transferred, or paid for?
- What are the units?
- What can we observe?
- What can we perturb?
- What would happen if the effect were zero?
- What would happen if costs doubled?
- What is the most embarrassing simple baseline?
- Are we naming the phenomenon or understanding it?

## Use With Other Skills

- Use with `prof/strang` to explain linear algebra geometrically.
- Use with `prof/shreve` to make stochastic calculus intuitive.
- Use with `prof/cont` to connect stochastic models to empirical facts.
- Use with `prof/boyd` to make optimization variables and constraints concrete.
- Use with `workflow/idea-to-hypothesis` when an idea is too vague.
- Use with `workflow/backtest-review` when a result looks sophisticated but may be cargo-cult science.

