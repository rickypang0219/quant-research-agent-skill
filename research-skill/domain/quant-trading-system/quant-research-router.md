# quant-research-router.md

Use this router when combining professor skill packs with the quant trading system builder skill.

## Paths

```text
research-skill/prof/strang/SKILL.md
research-skill/prof/lo/SKILL.md
research-skill/prof/brunton/SKILL.md
research-skill/prof/simons/SKILL.md
research-skill/prof/ng/SKILL.md
research-skill/domain/statistical-arbitrage/SKILL.md
research-skill/domain/market-microstructure/SKILL.md
research-skill/domain/quant-trading-system/SKILL.md
research-skill/domain/risk/SKILL.md
research-skill/domain/live-trading/SKILL.md
```

## Routing

- Use Strang for linear algebra, PCA, projections, least squares, numerical modeling.
- Use Lo for market realism, Adaptive Markets, financial economics, risk, AI in finance.
- Use Brunton for dynamical systems, SINDy, DMD, Koopman, control, high-dimensional modeling.
- Use Simons for empirical rigor, signal testing, stat-arb culture, research discipline.
- Use Ng for ML label design, train/validation/test discipline, leakage control, baselines, error analysis, and model iteration.
- Use Statistical Arbitrage for residuals, factor models, pairs, cross-sectional ranking, neutralization, and portfolio construction.
- Use Market Microstructure for order books, order flow, market making, execution, queueing, impact, and venue mechanics.
- Use Risk for sizing, leverage, exposure, drawdown, liquidity, funding, concentration, and kill-switch design.
- Use Live Trading for paper/live deployment, exchange APIs, order state, monitoring, reconciliation, and incident handling.
- Use Quant Trading System Builder for code, backtesting engines, paper/live architecture, Rust/Python implementation, observability, deployment, and debugging.

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
