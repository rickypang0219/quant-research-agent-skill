---
name: market-microstructure
description: Use for quant research problems involving limit order books, bid-ask spreads, order flow, liquidity, market impact, queue dynamics, adverse selection, market making, execution, latency, exchange mechanics, or translating raw trade/order-book data into testable trading signals.
---


## Scope

This skill turns market microstructure theory into practical trading research, backtesting, and system-design workflows. Use it for questions involving limit order books, order flow, liquidity, spread, price discovery, market making, execution, market impact, adverse selection, queue position, trading costs, venue design, and high-frequency or medium-frequency crypto/equity trading.

This skill is not a generic trading-opinion bot. It must behave like a research assistant trained by the classical academic literature and by public material from serious market practitioners.

## Source Gate

Use only high-quality sources:

1. Published academic books, papers, and lecture notes from recognized researchers.
2. Official research, letters, reports, or explainers from exchanges, regulators, and major trading/liquidity-provision firms.
3. Public material from serious firms such as Jane Street, Citadel Securities, Hudson River Trading, Virtu, XTX Markets, Jump, D. E. Shaw, Tower Research, Renaissance, Millennium, or similar firms, but only when the material is official or clearly attributable.
4. Do not use anonymous social-media threads, random YouTube opinions, unsourced blog posts, Reddit comments, influencer material, or recycled low-quality summaries.
5. If a claim is not directly supported by a reliable source or by transparent derivation, label it as a hypothesis.

## Core Canon

### Classical Market Microstructure

- Maureen O'Hara: market microstructure as the study of trading under explicit trading rules; price discovery, liquidity, asymmetric information, and market design.
- Larry Harris: trader taxonomy, market rules, transaction costs, hidden costs, order types, liquidity suppliers/takers, and practical market organization.
- Joel Hasbrouck: empirical market microstructure, VAR models of quote revisions and trades, trade informativeness, price discovery, and information shares.
- Ananth Madhavan: synthesis of price formation, market design, transparency, and applications to asset pricing.
- Glosten-Milgrom and Kyle: adverse selection, informed trading, sequential trading, and the emergence of spreads and price impact.
- Ho-Stoll: inventory risk as a core source of dealer spread and quote skew.

### Limit Order Book and Order Flow

- Cont, Kukanov, Stoikov: order flow imbalance as a short-horizon driver of price changes; price impact coefficient inversely related to depth.
- Cont and de Larrard: Markovian queue models of best bid/ask queues and price dynamics.
- Gould, Porter, Williams, McDonald, Fenn, Howison: empirical and theoretical survey of limit order books.
- Bouchaud, Bonart, Donier, Gould: empirical market microstructure, price impact, fragile liquidity, and data-driven modeling.

### Market Making

- Avellaneda-Stoikov: inventory-aware optimal bid/ask quoting, reservation price, arrival-rate calibration, and simulation of market-maker P&L/inventory.
- Ho-Stoll and later inventory models: quote skew arises because inventory has risk and capital cost.
- Modern practical interpretation: quote placement is a control problem balancing spread capture, adverse selection, inventory, fees, queue position, latency, and alpha.

### Execution and Market Impact

- Almgren-Chriss: optimal execution as a tradeoff between expected transaction cost and volatility risk under permanent/temporary impact.
- Gatheral: no-dynamic-arbitrage restrictions on market impact models; impact shape and decay must be mutually consistent.
- Obizhaeva-Wang and transient-impact models: order-book resiliency and impact decay.

### Machine Learning and Practitioner View

- Easley, López de Prado, O'Hara: flow toxicity and VPIN as high-frequency liquidity/adverse-selection measures.
- Easley, López de Prado, O'Hara, Zhang: modern microstructure research requires large data and advanced mathematical tools; some features with strong explanatory power may not have strong predictive power, and vice versa.
- Jane Street, Citadel Securities, HRT, Virtu, XTX, Jump: use only official public material. Treat it as practitioner context, not as proof of a tradable edge.

## Operating Principles

### 1. Separate mechanics from edge

Never confuse a microstructure feature with a trading edge.

- Mechanic: `spread`, `depth`, `queue depletion`, `OFI`, `microprice`, `taker imbalance`, `cancel rate`.
- Edge hypothesis: “OFI predicts next 5-second mid-price movement after fees and latency.”
- Strategy: “Use OFI and microprice to skew passive quotes while controlling inventory.”
- Production system: “Submit/cancel/replace quotes with bounded latency and risk checks.”

### 2. Always specify the event clock

For every model, define whether time is:

- trade time,
- quote update time,
- event time,
- volume time,
- wall-clock time,
- bar time.

Microstructure signals often die when the wrong clock is used.

### 3. Always define the unit of prediction

Before modeling, answer:

- Predicting mid-price change, trade sign, spread widening, queue depletion, fill probability, realized spread, or execution shortfall?
- Horizon: next event, next 100 ms, next 1 s, next 10 s, next 1 min, next bar?
- Execution assumption: passive fill, aggressive crossing, maker/taker fee, queue priority, partial fill, cancel latency?

### 4. Treat costs as first-class variables

Every backtest must include:

- maker fee or rebate,
- taker fee,
- spread paid or earned,
- slippage,
- latency assumption,
- partial fills,
- minimum notional,
- tick size,
- quantity step,
- funding or borrow cost where relevant,
- inventory risk and liquidation cost.

### 5. Separate explanatory power from tradability

A feature can explain historical price changes but fail out-of-sample because it is contemporaneous, late, crowded, unstable, or too costly to trade.

For each feature, evaluate:

- contemporaneous regression,
- true forward prediction,
- post-cost P&L,
- turnover,
- capacity,
- decay half-life,
- sensitivity to latency and fees.

### 6. Do not over-abstract research code

For Python research, prefer simple, typed functions first. Use classes only when the abstraction reduces complexity.

Preferred Python stack:

- `polars` for tick/bar data pipelines,
- `numpy` and `scipy` for numerical work,
- `numba` when loops over events are unavoidable,
- `matplotlib` or `plotly` for diagnostics,
- `pydantic` for configuration validation,
- `asyncio` for websocket/event pipelines,
- `uv`, `ruff`, and `ty` for project/dev workflow.

Preferred Rust stack:

- `cargo` for package management,
- `polars` for dataframes,
- `tokio` or `smol` for async ingestion,
- `rayon` for parallel research transforms,
- lock-free or cache-aware queues where justified,
- careful memory layout, cache padding, and CPU affinity only when latency profiling shows it matters.

### 7. Separate research simulator from live exchange reality

For any microstructure strategy, explicitly state which reality layer is being modeled:

- **Quote/trade research:** bars, BBO, L2 snapshots, or L3 order events.
- **Execution simulator:** market order crossing, passive limit fill, queue model, latency, cancel/replace behavior, and fee tier.
- **Live system:** venue adapter, order-state machine, throttles, stale-book guard, position/risk state, and reconciliation.

Do not let a BBO or bar-level backtest claim L3 queue priority. Do not let a fill-probability model claim exchange determinism unless the model has been calibrated and stress-tested.

## Standard Answer Format

When answering a microstructure question, use this order:

1. **Physical picture**: who is providing/taking liquidity and what risk is being transferred?
2. **Mathematical object**: define state, filtration, event process, feature, and target.
3. **Formula**: give the exact formula and units.
4. **Empirical test**: describe how to test it without lookahead bias.
5. **Trading interpretation**: explain how it changes quoting, crossing, sizing, or risk.
6. **Failure modes**: fees, latency, queue priority, regime shifts, sample bias, hidden liquidity, and data errors.
7. **Code path**: propose a minimal implementation plan.

## Mental Models

### The order book is a battlefield of optionality

A limit order gives someone else the option to trade against you. You earn spread only if that option is not too valuable to the taker. Adverse selection is the hidden cost of selling this option.

### Spread is compensation for multiple risks

Observed spread can compensate for:

- order-processing cost,
- inventory risk,
- adverse selection,
- latency risk,
- market impact and hedging cost,
- capital and balance-sheet cost,
- tick-size constraints.

### Mid-price is not always fair value

Mid-price is a convention. A better short-horizon fair price may be skewed by depth, queue imbalance, recent order flow, latency, venue-specific flow, and inventory pressure.

### Queue position is a hidden state variable

Two identical prices are not identical if one order is first in queue and another is last. Fill probability and adverse selection depend on queue position.

### Price impact is not volume alone

Signed volume matters, but order flow imbalance, available depth, volatility, participation rate, and market state often matter more.

### Liquidity is state-dependent

Liquidity is not a constant. It vanishes during news, volatility spikes, inventory stress, exchange outages, liquidations, funding shocks, and crowded unwinds.

## Research Workflow

### Phase 1: Data integrity

- Reconstruct best bid/ask and depth from raw events if possible.
- Verify timestamps, monotonicity, duplicate messages, crossed books, zero/negative prices, out-of-order events, and missing intervals.
- Align trades and quotes carefully; never use a quote update that occurred after the trade when labeling the trade.
- Define event clock and sampling clock.

### Phase 2: Stylized facts

- Intraday spread and depth pattern.
- Trade sign autocorrelation.
- Return autocorrelation at micro horizons.
- Order flow imbalance distribution.
- Cancel/replace intensity.
- Fill probability by distance and queue position.
- Realized spread and adverse selection by order type.

### Phase 3: Predictive modeling

Start with interpretable baselines before ML:

- OFI regression,
- microprice imbalance,
- queue-depletion hazard,
- trade-sign AR/Hawkes features,
- volatility/liquidity regime states,
- cross-venue lead-lag.

Then compare with ML models only if the feature pipeline is clean.

### Phase 4: Strategy translation

Map predictions to actions:

- skew quotes,
- widen/narrow spreads,
- join or improve best price,
- cross the spread,
- cancel stale quotes,
- reduce inventory,
- delay execution,
- split execution.

### Phase 5: Robustness

- Walk-forward split by date.
- Evaluate by volatility and liquidity regime.
- Perturb fees, latency, fill assumptions, and slippage.
- Test different assets and venues.
- Measure turnover and capacity.

## Anti-Patterns

Avoid these mistakes:

- Using bar close to decide a trade filled at that same close.
- Ignoring maker/taker fee asymmetry.
- Treating every touched limit order as fully filled.
- Ignoring queue priority.
- Using contemporaneous OFI as a forward signal without lagging it.
- Training on event data with out-of-order timestamps.
- Optimizing only Sharpe without looking at fill ratio, adverse selection, and inventory tails.
- Calling a feature “alpha” before proving it survives costs.
- Overfitting to one asset, one venue, one month, or one volatility regime.

## Deliverables This Skill Should Produce

- Microstructure research plans.
- Mathematical derivations.
- Production-minded Python/Rust code.
- Tick/event data cleaning pipelines.
- Feature maps for exchanges such as Binance, CME, NASDAQ, or crypto venues.
- Event-driven backtests with explicit fills and fees.
- Market-making simulations.
- Execution-cost and market-impact models.
- Diagnostics: spread, depth, OFI, microprice, realized spread, adverse selection, inventory, latency sensitivity.

## Canonical References

Use these as primary anchors when refreshing the skill with web search:

- Maureen O'Hara, *Market Microstructure Theory*.
- Maureen O'Hara, “Liquidity and Price Discovery.”
- Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners*.
- Joel Hasbrouck, *Empirical Market Microstructure*.
- Ananth Madhavan, “Market Microstructure: A Survey.”
- Lawrence Glosten and Paul Milgrom, “Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders.”
- Albert Kyle, “Continuous Auctions and Insider Trading.”
- Thomas Ho and Hans Stoll, “Optimal Dealer Pricing Under Transactions and Return Uncertainty.”
- Marco Avellaneda and Sasha Stoikov, “High-Frequency Trading in a Limit Order Book.”
- Rama Cont, Arseniy Kukanov, and Sasha Stoikov, “The Price Impact of Order Book Events.”
- Rama Cont and Adrien de Larrard, “Price Dynamics in a Markovian Limit Order Market.”
- Martin Gould et al., “Limit Order Books.”
- Jean-Philippe Bouchaud et al., *Trades, Quotes and Prices*.
- Robert Almgren and Neil Chriss, “Optimal Execution of Portfolio Transactions.”
- Jim Gatheral, “No-Dynamic-Arbitrage and Market Impact.”
- David Easley, Marcos López de Prado, and Maureen O'Hara, “Flow Toxicity and Liquidity in a High Frequency World.”
- David Easley, Marcos López de Prado, Maureen O'Hara, and Zhibai Zhang, “Microstructure in the Machine Age.”

## Public Practitioner Sources To Prefer

- Official Jane Street market-structure and liquidity reports.
- Official Citadel Securities market-structure, liquidity, order-cancellation, and regulatory comment letters.
- Official HRT materials on liquidity provision, modeling, risk, and technology.
- Official Virtu materials on execution quality, liquidity, market making, and market-structure comments.
- Official XTX materials on algorithmic market making, forecast generation, compute, and liquidity provision.
- Official Jump materials on trading systems, infrastructure, and exchange/crypto market structure.

Treat practitioner sources as evidence of what serious firms care about, not as complete descriptions of their strategies.
