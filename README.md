# Quant Research Agent Skill Library

This folder is a skill library for a quant research and live-trading development assistant. It is designed to make the assistant behave less like a generic chatbot and more like an adversarial quant research partner, code reviewer, risk critic, and production engineering assistant.

The core rule is simple:

```text
idea -> observable -> hypothesis -> test -> backtest -> risk review -> paper/live readiness
```

No trading idea should be treated as serious until it specifies data, signal, position rule, PnL formula, costs, validation method, failure modes, and live-execution constraints.

## Folder Layout

```text
.
├── AGENTS.md
└── research-skill/
    ├── prof/
    ├── domain/
    ├── workflow/
    └── source_registry.md
```

## `AGENTS.md`

`AGENTS.md` is the top-level operating manual. It tells the assistant:

- how to behave;
- which skills to inspect;
- how to route quant, trading, math, backtest, code-review, risk, and live-trading tasks;
- what output formats to use for new ideas, strategy reviews, code reviews, and hard research questions.

Start here when changing the assistant's overall behavior.

## `research-skill/prof/`

Professor-style lenses for mathematical and scientific reasoning:

- `simons/` - hidden structure, empirical signal testing, geometry/topology of market states.
- `strang/` - linear algebra, PCA, projections, covariance, factor models, residuals.
- `lo/` - adaptive markets, empirical finance, realism, crowding, liquidity, risk.
- `cont/` - stochastic processes grounded in market data, jumps, stylized facts, pathwise calculus, LOB queue models, OFI, impact.
- `shreve/` - martingales, Brownian motion, stochastic calculus, SDEs, risk-neutral pricing, stochastic control, transaction costs.
- `boyd/` - convex optimization, constrained portfolios, duality, ADMM, solver diagnostics.
- `engle/` - volatility econometrics, ARCH/GARCH, realized volatility, DCC, VaR/ES, volatility targeting.
- `gatheral/` - implied volatility surface, rough volatility, variance risk premium, no-dynamic-arbitrage impact.
- `robust-statistics/` - outliers, heavy tails, robust regression, median/MAD, robust covariance, influence diagnostics.
- `bertsekas/` - dynamic programming, stochastic control, MDPs, approximate DP, execution/inventory control.
- `feynman/` - first-principles explanation, simple language, toy examples, physical intuition, cargo-cult research checks.
- `ng/` - machine learning discipline, labels, baselines, leakage control, validation.
- `brunton/` - dynamical systems, SINDy, Koopman, DMD, state-space thinking.

Use these when a question needs mathematical framing or research taste.

## `research-skill/domain/`

Domain skills for concrete trading and engineering areas:

- `statistical-arbitrage/` - pairs, residual mean reversion, PCA stat arb, cross-sectional ranking, neutrality.
- `market-microstructure/` - order books, spread, order flow, market making, execution, queueing, impact.
- `quant-trading-system/` - event-driven backtesting, data ingestion, execution engines, observability, Rust/Python architecture.
- `risk/` - exposure, leverage, drawdown, liquidity, funding, concentration, stress tests, kill switches.
- `live-trading/` - paper/live trading, exchange APIs, reconciliation, monitoring, deployment readiness.

Use these when the task is about a specific trading strategy, data pipeline, system component, or risk problem.

## `research-skill/workflow/`

Workflow skills for turning ideas into disciplined work:

- `idea-to-hypothesis/` - converts vague ideas into observables, hypotheses, baselines, and minimum tests.
- `data-audit/` - checks schema, timestamps, missing data, stale prices, funding alignment, and point-in-time correctness.
- `signal-diagnostics/` - tests IC, rank IC, bucket monotonicity, signal decay, turnover, exposures, and cost-adjusted edge.
- `experiment-ledger/` - records configs, dataset versions, parameter searches, rejected variants, and anti-p-hacking evidence.
- `backtest/` - builds reproducible vectorized and event-driven backtests.
- `backtest-review/` - reviews PnL, costs, leakage, validation, robustness, and execution realism.
- `paper-trading-review/` - reviews live-vs-sim drift, fills, latency, slippage, feature drift, and reconciliation.
- `model-validation/` - independently validates assumptions, data lineage, leakage, robustness, parity, and monitoring.
- `research-to-production-handoff/` - turns research notebooks into modules, configs, tests, contracts, and runbooks.
- `postmortem/` - reviews incidents, losses, outages, bad fills, and risk breaches.
- `code-review/` - reviews quant research and trading-system code.
- `production-readiness/` - decides whether something is ready for paper trading, small live, or scaling.

Use these to control the shape of the response and the next concrete action.

## How To Use

For a non-trivial task, do not read every file. Select the relevant skills:

```text
PCA stat arb:
    prof/strang
    prof/boyd
    prof/lo
    domain/statistical-arbitrage
    domain/risk
    workflow/data-audit
    workflow/signal-diagnostics
    workflow/backtest-review

Microstructure strategy:
    prof/cont
    prof/lo
    prof/engle
    domain/market-microstructure
    domain/risk
    workflow/data-audit
    workflow/signal-diagnostics
    workflow/idea-to-hypothesis

Stochastic calculus / derivative pricing:
    prof/shreve
    prof/cont
    prof/gatheral
    prof/lo
    domain/risk

ML alpha model:
    prof/ng
    prof/lo
    prof/robust-statistics
    domain/statistical-arbitrage
    domain/risk
    workflow/data-audit
    workflow/signal-diagnostics
    workflow/backtest

Live trading system:
    domain/quant-trading-system
    domain/live-trading
    domain/risk
    workflow/research-to-production-handoff
    workflow/paper-trading-review
    workflow/production-readiness

Code review:
    workflow/code-review
    plus the relevant domain skill
```

Each skill folder uses `SKILL.md` as the main entry point. Supporting files such as `sources.md`, `mental_models.md`, `formulas.md`, `experiments.md`, `architecture.md`, and `checklists.md` provide extra detail when needed.

## Source Discipline

The library prefers academic and serious practitioner sources: O'Hara, Hasbrouck, Kyle, Richard Feynman, Rama Cont, Steven Shreve, Stephen Boyd, Robert Engle, Jim Gatheral, Peter Huber, Dimitri Bertsekas, Avellaneda-Stoikov, Cont-Kukanov-Stoikov, Almgren-Chriss, Lo, Bailey/Lopez de Prado, White, Hansen, Fama-French, Jane Street, Citadel/Citadel Securities, D. E. Shaw, Tower Research, Renaissance, NautilusTrader, and QuantConnect LEAN.

These sources are used to create testable research objects and engineering standards. They are not used as authority theater or proof of alpha.

## Expected Assistant Behavior

The assistant should be:

- skeptical;
- precise;
- data-driven;
- implementation-minded;
- conservative about live trading;
- explicit about assumptions, costs, leakage, and failure modes.

The assistant should not accept vague strategy ideas, pretty equity curves, or elegant math unless they become measurable, testable, and implementable.
