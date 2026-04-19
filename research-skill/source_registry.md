# Quant Research Source Registry

This registry gives the skill library a preferred source basis. Use these sources to shape questions, experiments, and engineering standards. Do not treat any source as proof that a strategy is tradable.

## Academic Market Microstructure

- Maureen O'Hara - *Market Microstructure Theory*: price discovery, liquidity, asymmetric information, and trading rules.
- Joel Hasbrouck - *Empirical Market Microstructure*: trade informativeness, quote revisions, VAR/event-study methods, and price discovery.
- Albert Kyle - "Continuous Auctions and Insider Trading": informed trading, market depth, and linear price impact.
- Glosten and Milgrom - sequential trade, adverse selection, and spread formation.
- Marco Avellaneda and Sasha Stoikov - "High-Frequency Trading in a Limit Order Book": inventory-aware market making, reservation price, quote spread, and arrival-rate calibration.
- Rama Cont, Arseniy Kukanov, and Sasha Stoikov - "The Price Impact of Order Book Events": order flow imbalance, depth, and short-horizon price changes.
- Robert Almgren and Neil Chriss - "Optimal Execution of Portfolio Transactions": execution cost/risk tradeoff and market-impact-aware schedules.
- Easley, Lopez de Prado, O'Hara, and Zhang - flow toxicity and modern machine-age microstructure.

## Statistical Arbitrage and Empirical Finance

- Avellaneda and Lee - PCA/ETF residual statistical arbitrage and mean-reverting residuals.
- Gatev, Goetzmann, and Rouwenhorst - distance-based pairs trading.
- Lo and MacKinlay - data-snooping risk and empirical finance discipline.
- Andrew Lo - Adaptive Markets Hypothesis and liquidity/crowding realism.
- Khandani and Lo - quant crowding and forced deleveraging.
- Fama-French, Carhart, Asness-Moskowitz-Pedersen, Frazzini-Pedersen - factor baselines that alpha must beat or neutralize.
- Bailey, Borwein, Lopez de Prado, and Zhu - probability of backtest overfitting.
- Bailey and Lopez de Prado - Deflated Sharpe Ratio.
- White and Hansen - data snooping and superior predictive ability tests.

## Public Practitioner / Firm Sources

Use official or clearly attributable material only:

- Jane Street: technology, OCaml, in-house trading/risk systems, research tools, and tight trading/research/engineering integration.
- Citadel and Citadel Securities: hypothesis-driven quantitative research, large datasets, simulation, compute, market making, market microstructure, and low-latency engineering.
- D. E. Shaw: systematic investing, quantitative tools, independent return sources, collaboration, and risk/reward discipline.
- Tower Research: high-performance technology platform, market access, data, compute, research infrastructure, risk management, and independent quant teams.
- Renaissance Technologies: mathematical and statistical methods for investment-program design and execution.
- NautilusTrader: event-driven research-to-live parity, live reconciliation, deterministic simulation, Rust/Python architecture.
- QuantConnect LEAN: open-source event-driven algorithm engine for research, backtesting, optimization, and live trading.

## How to Use This Registry

Convert sources into concrete work:

- source claim -> observable variable;
- model -> formula;
- formula -> feature/label;
- feature/label -> test;
- test -> backtest;
- backtest -> risk and execution review;
- review -> paper/live readiness decision.

If the source cannot be converted into an empirical or engineering object, it is context, not evidence.

