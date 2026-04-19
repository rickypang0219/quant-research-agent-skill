# quant-research-router.md

Use this router when combining professor skill packs with the quant trading system builder skill.

## Paths

```text
research-skill/prof/strang/SKILL.md
research-skill/prof/lo/SKILL.md
research-skill/prof/brunton/SKILL.md
research-skill/prof/simons/SKILL.md
research-skill/prof/cont/SKILL.md
research-skill/prof/shreve/SKILL.md
research-skill/prof/boyd/SKILL.md
research-skill/prof/engle/SKILL.md
research-skill/prof/gatheral/SKILL.md
research-skill/prof/robust-statistics/SKILL.md
research-skill/prof/bertsekas/SKILL.md
research-skill/prof/feynman/SKILL.md
research-skill/prof/ng/SKILL.md
research-skill/domain/statistical-arbitrage/SKILL.md
research-skill/domain/market-microstructure/SKILL.md
research-skill/domain/quant-trading-system/SKILL.md
research-skill/domain/risk/SKILL.md
research-skill/domain/live-trading/SKILL.md
research-skill/workflow/data-audit/SKILL.md
research-skill/workflow/signal-diagnostics/SKILL.md
research-skill/workflow/experiment-ledger/SKILL.md
research-skill/workflow/paper-trading-review/SKILL.md
research-skill/workflow/model-validation/SKILL.md
research-skill/workflow/research-to-production-handoff/SKILL.md
research-skill/workflow/postmortem/SKILL.md
```

## Routing

- Use Strang for linear algebra, PCA, projections, least squares, numerical modeling.
- Use Lo for market realism, Adaptive Markets, financial economics, risk, AI in finance.
- Use Brunton for dynamical systems, SINDy, DMD, Koopman, control, high-dimensional modeling.
- Use Simons for empirical rigor, signal testing, stat-arb culture, research discipline.
- Use Cont for stochastic processes grounded in empirical stylized facts, jumps, pathwise calculus, order-flow imbalance, LOB queue models, and model risk.
- Use Shreve for martingales, filtrations, Brownian motion, Ito calculus, risk-neutral pricing, stochastic control, and transaction costs.
- Use Boyd for convex optimization, constrained portfolios, turnover penalties, robust optimization, and solver diagnostics.
- Use Engle for volatility econometrics, ARCH/GARCH, realized volatility, DCC, VaR/ES, and volatility targeting.
- Use Gatheral for volatility surfaces, rough volatility, variance risk premium, and no-dynamic-arbitrage market impact.
- Use Robust Statistics for outliers, heavy tails, robust regression, robust covariance, and influence diagnostics.
- Use Bertsekas for dynamic programming, MDPs, approximate DP, reinforcement learning sanity checks, and execution/inventory control.
- Use Feynman for simple-language teaching, first-principles explanation, toy models, physical intuition, and cargo-cult research checks.
- Use Ng for ML label design, train/validation/test discipline, leakage control, baselines, error analysis, and model iteration.
- Use Statistical Arbitrage for residuals, factor models, pairs, cross-sectional ranking, neutralization, and portfolio construction.
- Use Market Microstructure for order books, order flow, market making, execution, queueing, impact, and venue mechanics.
- Use Risk for sizing, leverage, exposure, drawdown, liquidity, funding, concentration, and kill-switch design.
- Use Live Trading for paper/live deployment, exchange APIs, order state, monitoring, reconciliation, and incident handling.
- Use Quant Trading System Builder for code, backtesting engines, paper/live architecture, Rust/Python implementation, observability, deployment, and debugging.
- Use Data Audit before research/backtesting whenever data provenance, timestamps, gaps, stale data, or contract specs matter.
- Use Signal Diagnostics before full backtesting to test whether the feature has standalone information.
- Use Experiment Ledger whenever many variants, parameters, or datasets are tried.
- Use Paper Trading Review, Model Validation, Research-to-Production Handoff, and Postmortem for the research-to-live lifecycle.

## Default quant research workflow

1. Define the market hypothesis.
2. Define the data and timestamp assumptions.
3. Build the smallest possible prototype.
4. Backtest with deterministic event ordering.
5. Add realistic fees, slippage, latency, and liquidity constraints.
6. Run robustness and failure-mode tests.
7. Paper trade with risk gates and monitoring.
8. Migrate production-critical components to Rust.
9. Deploy only after reconciliation, monitoring, and kill-switch tests pass.
