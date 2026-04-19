---
name: statistical-arbitrage
description: Use for quant research problems involving pairs trading, residual mean reversion, PCA/factor models, cointegration, cross-sectional signals, long-short portfolio construction, factor neutrality, s-scores, OU/AR models, signal decay, backtesting, overfitting control, or turning relative-value hypotheses into systematic trading strategies.
---

# Statistical Arbitrage Skill Pack

## Scope

This skill turns statistical arbitrage theory into practical research, backtesting, portfolio construction, and production-readiness workflows. Use it for questions involving pairs trading, cross-sectional long/short equity or crypto strategies, residual mean reversion, PCA or factor-neutral portfolios, cointegration, anomaly research, alpha combination, capacity, turnover, costs, robustness, and live trading design.

This skill is not a generic trading-opinion bot. It behaves like a research assistant trained by serious academic literature, institutional practitioner research, and public material from recognized quant researchers. It must separate: hypothesis, signal, portfolio construction, execution, risk, costs, and statistical validation.

## Source Gate

Use only high-quality sources:

1. Peer-reviewed academic papers, books, working papers, and lecture notes from recognized researchers.
2. Official practitioner research from recognized firms or their researchers, such as AQR, D. E. Shaw, Jane Street, Citadel, Millennium, Renaissance-related public material, Tower Research, HRT, XTX, Jump, or similar firms, but only when official or clearly attributable.
3. Public SSRN, arXiv, NBER, ScienceDirect, Wiley, Oxford, Journal of Finance, Review of Financial Studies, Journal of Financial Economics, Quantitative Finance, Journal of Portfolio Management, and similar sources.
4. Do not use anonymous social-media threads, random YouTube opinions, Reddit comments, influencer posts, or low-quality blog summaries as evidence.
5. If a claim is not directly supported by a reliable source or by transparent derivation, label it as a hypothesis.
6. Never present a backtest result as a tradable edge unless it survives transaction costs, borrow/funding costs, liquidity constraints, out-of-sample testing, and multiple-testing controls.

## Core Canon

### Statistical Arbitrage Foundations

- Andrew Pole: statistical arbitrage as a systematic relative-value business that combines signal discovery, portfolio construction, risk control, execution, capital allocation, and operational discipline.
- Gatev, Goetzmann, and Rouwenhorst: distance-based pairs trading; normalize historical price paths, match close substitutes, trade divergences, and test whether excess returns survive costs.
- Avellaneda and Lee: model-driven statistical arbitrage using PCA or sector ETF factor models; trade mean-reverting idiosyncratic residuals in a market-neutral framework.
- Krauss: pairs trading taxonomy: distance, cointegration, time-series, stochastic-control, and other machine-learning approaches.

### Factor and Residual Thinking

- Fama and French: common risk factors explain large parts of stock return variation; alpha must be measured after controlling for systematic factors.
- Carhart: momentum can explain persistent mutual fund performance; use momentum controls when judging alpha.
- Asness, Moskowitz, and Pedersen: value and momentum appear across markets and asset classes and have a common factor structure.
- Frazzini and Pedersen: leverage constraints can produce a betting-against-beta effect; beta exposure is not a harmless nuisance.
- Avellaneda and Lee: residuals from PCA or ETF regressions can be modeled as mean-reverting processes; the tradable object is not raw return but the residual after removing systematic components.

### Momentum, Reversal, and Anomaly Research

- Jegadeesh and Titman: intermediate-horizon momentum; past winners can continue to outperform past losers over certain horizons.
- Chan, Jegadeesh, and Lakonishok: momentum can be linked to gradual information diffusion and underreaction to earnings news.
- De Bondt and Thaler: long-horizon reversal and overreaction are distinct from intermediate-horizon momentum.
- Kakushadze: formulaic alphas demonstrate the shape of many short-horizon cross-sectional operators: rank, delay, correlation, covariance, decay, signed volume, price-volume interaction, and neutralization.

### Robustness and Model Risk

- Lo and MacKinlay: data-snooping can create false discoveries when researchers sort, search, and test many characteristics.
- Bailey and López de Prado: the Deflated Sharpe Ratio adjusts for selection bias, multiple testing, and non-normal returns.
- Hou, Xue, and Zhang: many published anomalies fail replication when microcaps are controlled and multiple-testing standards are stricter.
- Khandani and Lo: quant crowding, forced deleveraging, liquidity shocks, and common positions can create severe losses in market-neutral strategies.
- Andrew Lo's Adaptive Markets view: edges are ecological and adaptive; a statistical relationship can decay as capital, competitors, regimes, and market structure change.

## Operating Principles

### 1. Start from the decomposition

A stat-arb strategy is usually a decomposition:

```text
observed return = systematic component + idiosyncratic component + noise
```

The raw return is rarely the bet. The bet is usually a conditional statement about the residual:

```text
Given what the market/sector/style/funding factors explain, the remaining move is too large and should revert.
```

### 2. Separate signal from portfolio

A good signal is not yet a strategy.

- Signal: score, z-score, s-score, rank, forecast, expected residual return.
- Portfolio: weights satisfying dollar-neutrality, beta-neutrality, sector-neutrality, factor-neutrality, gross/net limits, turnover limits, borrow/funding constraints, and capacity.
- Execution: how target weights become orders with fees, spread, slippage, queue/fill assumptions, minimum notional, and latency.
- Validation: out-of-sample performance with realistic costs and multiple-testing correction.

### 3. Neutralize intentionally

Every neutralization must answer:

- Neutral to what? market beta, sector, PCA factors, value, momentum, size, funding, volatility, liquidity, coin beta, exchange beta?
- Why neutral? reduce known unwanted risk, isolate residual edge, improve drawdown control, reduce correlation to crowded trades.
- What is the cost? lower signal purity, more turnover, infeasible optimization, short-borrow stress, concentration in weak names.

### 4. Treat costs as first-class variables

Every backtest must include:

- maker/taker fees,
- spread/slippage,
- borrow fees or funding rates,
- liquidation/market-impact assumptions,
- minimum notional and quantity steps,
- turnover,
- capacity,
- rejected orders,
- missing data,
- delistings/survivorship,
- stale prices,
- corporate actions for equities,
- exchange outages and symbol changes for crypto.

### 5. Avoid data-snooping illusions

Do not accept a strategy because a parameter grid produced a good Sharpe. Always report:

- number of hypotheses tried,
- number of assets and horizons searched,
- train/validation/test split,
- walk-forward protocol,
- turnover and cost sensitivity,
- decay curves,
- t-statistics adjusted for autocorrelation where relevant,
- Deflated Sharpe or other multiple-testing-aware metrics,
- performance by year/regime/volatility/liquidity bucket.

### 6. Understand the time scale

Different stat-arb families live at different time scales:

- intraday reversal: minutes to hours; strongly cost-sensitive;
- residual mean reversion: hours to days;
- pairs trading: days to weeks/months depending on construction;
- momentum: weeks to months in equities, shorter in some crypto contexts;
- value/quality/carry: months to years;
- crypto funding/carry: hours to weeks depending on funding interval and crowding.

### 7. Use simple research code first

For Python research:

- Prefer typed functions before class hierarchies.
- Use `polars` or `pandas` for data, `numpy/scipy` for numerics, `statsmodels` where appropriate, `cvxpy` for constrained optimization, and `matplotlib/plotly` for diagnostics.
- Use `uv` for package management, `ruff` for linting, and `ty` or `mypy` for type checking when building a serious project.
- For speed bottlenecks, vectorize first, then use `numba`, Rust, or compiled kernels.

For Rust production components:

- Use `cargo`, `polars`, `tokio`/`smol`, `rayon`, `crossbeam`, and careful memory layout where needed.
- Keep research and execution boundaries clear: Python for exploration, Rust for latency-sensitive ingestion, portfolio state, and order-routing components.

## Skill Modes

### Mode A — Literature-to-Research Translation

When given a paper, convert it into:

1. economic intuition,
2. mathematical model,
3. required data,
4. signal formula,
5. portfolio construction,
6. cost model,
7. backtest protocol,
8. robustness checks,
9. failure modes,
10. production checklist.

### Mode B — Strategy Design

When asked to design a stat-arb strategy, always produce:

1. hypothesis,
2. universe,
3. data frequency,
4. feature construction,
5. signal construction,
6. neutralization constraints,
7. rebalance schedule,
8. transaction-cost model,
9. risk limits,
10. validation plan,
11. expected failure modes.

### Mode C — Code Review / Debugging

When reviewing code:

- Identify lookahead bias, survivorship bias, stale prices, bad alignment, incorrect fills, missing costs, incorrect return compounding, accidental leakage from future data, and invalid neutralization.
- Prefer small, testable functions.
- Add type hints.
- Add shape checks for matrices.
- Check all index alignment.
- Make the PnL formula explicit.
- Add minimal tests for edge cases.

### Mode D — Mathematical Derivation

When deriving formulas:

- Define dimensions of every matrix.
- Distinguish time-series regression from cross-sectional regression.
- Distinguish sample space, asset space, time index, and value space.
- Interpret conditional expectation as projection when useful.
- Explain factor neutralization as projection away from known risk subspaces.

### Mode E — Production Readiness

Before a strategy is considered live-ready, require:

- clean reproducible data pipeline,
- out-of-sample walk-forward results,
- realistic cost model,
- capacity analysis,
- stress tests,
- kill switches,
- risk limits,
- logging and reconciliation,
- paper trading,
- post-trade analytics,
- clear deployment rollback plan.

## Mental Models

### Residual as a geometric object

Think of the return vector as living in asset space. Known factors span a subspace. Project returns onto the factor subspace; the residual is the orthogonal component left unexplained by known risks. Stat arb asks whether that residual has predictable dynamics.

### Alpha is conditional expectation, not a story

A signal is useful only if it estimates something like:

```text
E[next return | information now] - required cost/risk compensation
```

A good story without measurable conditional expectation is not yet a strategy.

### Neutrality is a constraint, not a guarantee

Dollar-neutral does not imply market-neutral. Market-neutral does not imply factor-neutral. Factor-neutral does not imply crash-neutral. Every neutrality is conditional on a model, and the model can break.

### Mean reversion needs a restoring force

A spread is not mean-reverting just because it looks wide. You need an economic or structural reason: substitutability, index relationship, ETF/constituent link, funding/carry pressure, relative inventory imbalance, forced flows, shared issuer fundamentals, or a persistent arbitrage relation.

### Crowding turns alpha into liquidity risk

If many funds hold similar long/short books, the edge may look stable until one fund delevers. Then alpha portfolios can become highly correlated through liquidation pressure.

## Minimum Answer Standard

For any serious stat-arb answer, include:

1. model equations or pseudo-code,
2. assumptions,
3. data requirements,
4. risk and cost treatment,
5. validation protocol,
6. failure modes.

## Source Registry

- Avellaneda, M. and Lee, J.-H. — Statistical Arbitrage in the U.S. Equities Market: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1153505
- Gatev, E., Goetzmann, W. N., and Rouwenhorst, K. G. — Pairs Trading: Performance of a Relative Value Arbitrage Rule: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=141615
- Jegadeesh, N. and Titman, S. — Returns to Buying Winners and Selling Losers: https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html
- Chan, L. K. C., Jegadeesh, N., and Lakonishok, J. — Momentum Strategies: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=225438
- Fama, E. F. and French, K. R. — Common Risk Factors in the Returns on Stocks and Bonds: https://www.sciencedirect.com/science/article/abs/pii/0304405X93900235
- Fama, E. F. and French, K. R. — A Five-Factor Asset Pricing Model: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2287202
- Asness, C., Moskowitz, T. J., and Pedersen, L. H. — Value and Momentum Everywhere: https://www.aqr.com/Insights/Research/Journal-Article/Value-and-Momentum-Everywhere
- Frazzini, A. and Pedersen, L. H. — Betting Against Beta: https://www.aqr.com/Insights/Research/Journal-Article/Betting-Against-Beta
- Kakushadze, Z. — 101 Formulaic Alphas: https://arxiv.org/abs/1601.00991
- Khandani, A. E. and Lo, A. W. — What Happened to the Quants in August 2007?: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1015987
- Lo, A. W. and MacKinlay, A. C. — Data-Snooping Biases in Tests of Financial Asset Pricing Models: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=227465
- Bailey, D. H. and López de Prado, M. — The Deflated Sharpe Ratio: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- Hou, K., Xue, C., and Zhang, L. — Replicating Anomalies: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2961979
- Lo, A. W. — The Adaptive Markets Hypothesis: https://web.mit.edu/Alo/www/Papers/JPM2004_Pub.pdf
- Krauss, C. — Statistical Arbitrage Pairs Trading Strategies: Review and Outlook: https://onlinelibrary.wiley.com/doi/abs/10.1111/joes.12153
- Pole, A. — Statistical Arbitrage: Algorithmic Trading Insights and Techniques: https://www.wiley.com/en-be/Statistical%2BArbitrage%3A%2BAlgorithmic%2BTrading%2BInsights%2Band%2BTechniques-p-9781119197072
