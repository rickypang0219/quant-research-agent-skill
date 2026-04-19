# quant-research-router.md

Use this router when combining professor skill packs with the quant trading system builder skill.

## Paths

```text
/prof/strang/SKILLS.md
/prof/lo/SKILLS.md
/prof/brunton/SKILLS.md
/prof/simons/SKILLS.md
/skills/quant-trading-system/SKILLS.md
```

## Routing

- Use Strang for linear algebra, PCA, projections, least squares, numerical modeling.
- Use Lo for market realism, Adaptive Markets, financial economics, risk, AI in finance.
- Use Brunton for dynamical systems, SINDy, DMD, Koopman, control, high-dimensional modeling.
- Use Simons for empirical rigor, signal testing, stat-arb culture, research discipline.
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
