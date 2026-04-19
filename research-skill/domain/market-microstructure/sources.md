# Market Microstructure Source Map

Use this file when grounding order book, market making, execution, spread, liquidity, adverse selection, and market-impact claims.

## Core Academic Sources

- Maureen O'Hara - *Market Microstructure Theory*. Use for price discovery, liquidity, asymmetric information, and trading rules.
- Larry Harris - *Trading and Exchanges*. Use for trader taxonomy, order types, hidden costs, liquidity, and practical market organization.
- Joel Hasbrouck - *Empirical Market Microstructure*. Use for trade informativeness, quote revision, VAR/event-study methods, and price discovery.
- Albert Kyle - "Continuous Auctions and Insider Trading". Use for informed trading, depth, and price impact.
- Glosten and Milgrom - adverse selection and bid-ask spread formation under sequential trade.
- Ho and Stoll - inventory risk and dealer quote behavior.
- Avellaneda and Stoikov - "High-Frequency Trading in a Limit Order Book". Use for reservation price, inventory penalty, optimal spread, and quote simulation.
- Cont, Kukanov, and Stoikov - "The Price Impact of Order Book Events". Use for order flow imbalance and depth-scaled short-horizon impact.
- Cont and de Larrard - Markovian best-queue models.
- Almgren and Chriss - "Optimal Execution of Portfolio Transactions". Use for execution schedules and impact/risk tradeoffs.
- Gatheral - no-dynamic-arbitrage restrictions on market impact.
- Easley, Lopez de Prado, O'Hara, and Zhang - flow toxicity and microstructure in the machine age.

## Public Practitioner Sources

Use only official or clearly attributable public material:

- Jane Street official technology and market-structure material.
- Citadel Securities market-structure, liquidity, equities/options, and quantitative research material.
- Tower Research quantitative-trading and engineering material.
- HRT, Virtu, XTX, Jump, and similar firm material when official.

Practitioner material should inform system design and operational realism, not serve as proof that a feature is tradable.

## Required Translation

For every source-inspired idea, define:

- event clock;
- observable state;
- feature formula;
- forward target;
- horizon;
- cost model;
- fill/latency assumption;
- validation split;
- failure mode.

