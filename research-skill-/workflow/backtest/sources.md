# Backtesting Skill Sources

This source list is intentionally curated toward credible practitioner, academic, and official documentation. It excludes random social media opinions.

## Core Practitioner Sources

### Ernest P. Chan

- `Quantitative Trading: How to Build Your Own Algorithmic Trading Business`
  - Relevance: practical backtesting, common biases, transaction cost realism, simple alpha research.
  - URL: https://asset.quant-wiki.com/pdf/Quantitative%20Trading_%20How%20to%20Build%20Your%20Own%20Algorithmic%20Trading%20Business-Wiley%20%282008%29.pdf
- `Backtesting and its Pitfalls`
  - Relevance: look-ahead bias, survivorship bias, data-snooping bias, why automated trading implementation often exposes backtest errors.
  - URL: https://epchan.com/img/links/Backtesting-and-its-Pitfalls.pdf

### Marcos López de Prado / David Bailey / Jonathan Borwein / Qiji Zhu

- `The Probability of Backtest Overfitting`
  - Relevance: PBO, CSCV, in-sample winners failing out-of-sample.
  - URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
  - PDF mirror: https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf
- `Advances in Financial Machine Learning`
  - Relevance: purged cross-validation, embargo, deflated Sharpe, financial ML research process.
  - URL: https://www.smallake.kr/wp-content/uploads/2018/07/SSRN-id3104847.pdf

### Andrew W. Lo

- `The Statistics of Sharpe Ratios`
  - Relevance: Sharpe ratios are estimates with sampling error; serial correlation can distort annualization.
  - URL: https://www.tandfonline.com/doi/abs/10.2469/faj.v58.n4.2453

---

## Academic Data-Snooping and Multiple-Testing Sources

### Halbert White

- `A Reality Check for Data Snooping`
  - Relevance: repeated use of the same dataset for model selection can produce false discoveries.
  - URL: https://www.ssc.wisc.edu/~bhansen/718/White2000.pdf

### Peter Reinhard Hansen

- `A Test for Superior Predictive Ability`
  - Relevance: SPA test improves model-comparison testing under data snooping.
  - URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=264569

### Campbell Harvey, Yan Liu, Heqing Zhu

- `... and the Cross-Section of Expected Returns`
  - Relevance: factor discovery is a multiple-testing problem; higher statistical hurdle is needed.
  - URL: https://academic.oup.com/rfs/article/29/1/5/1843824
  - PDF: https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF

---

## Market Microstructure and Execution Sources

These are included because realistic event-driven backtesting must model execution, spread, order book state, inventory, and impact.

### Maureen O'Hara

- `Market Microstructure Theory`
  - Relevance: trading mechanisms, information, inventory, and price formation.
  - URL: https://books.google.com/books/about/Market_Microstructure_Theory.html?id=D-PGBwAAQBAJ

### Avellaneda and Stoikov

- `High-frequency trading in a limit order book`
  - Relevance: inventory risk, limit order arrivals, market-making simulation.
  - URL: https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf

### Almgren and Chriss

- `Optimal Execution of Portfolio Transactions`
  - Relevance: transaction costs, volatility risk, permanent and temporary market impact.
  - URL: https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf

### Rama Cont

- `Empirical properties of asset returns: stylized facts and statistical issues`
  - Relevance: fat tails, volatility clustering, autocorrelation structure, non-Gaussian returns.
  - URL: https://rama.cont.perso.math.cnrs.fr/pdf/empirical.pdf

---

## Event-Driven Backtesting Framework References

### NautilusTrader

- `Backtesting`
  - Relevance: high-performance backtesting/live architecture; matching engine, fill price determination, L2/L3 book simulation.
  - URL: https://nautilustrader.io/docs/latest/concepts/backtesting/
- Project homepage
  - Relevance: Rust core, Python edge, same engine for backtesting and live trading.
  - URL: https://nautilustrader.io/

### QuantConnect LEAN

- `LEAN Engine`
  - Relevance: open-source algorithmic trading engine for research, backtesting, and live trading.
  - URL: https://www.quantconnect.com/docs/v2/lean-engine/getting-started
- `Trading and Orders`
  - Relevance: order lifecycle, order events, backtest fill simulation.
  - URL: https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/key-concepts
- `Understanding Time`
  - Relevance: event-based, streaming view of time.
  - URL: https://www.quantconnect.com/docs/v1/key-concepts/understanding-time

### Zipline / Quantopian

- Zipline documentation
  - Relevance: Pythonic event-driven backtesting.
  - URL: https://zipline.ml4trading.io/
- Zipline GitHub
  - Relevance: event-driven design and production history in Quantopian context.
  - URL: https://github.com/quantopian/zipline

### QuantStart

- `Event-Driven Backtesting with Python`
  - Relevance: clean educational architecture with DataHandler, Strategy, Portfolio, ExecutionHandler, event queue.
  - URL: https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-I/
  - URL: https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-III/
- `An Introduction to Backtesting with Python`
  - Relevance: backtesting definitions, event-driven vs vectorized comparison.
  - URL: https://s3.amazonaws.com/quantstart/media/powerpoint/an-introduction-to-backtesting.pdf

---

## Top-Tier Firm / Serious Engineering Signals

These are not strategy recipes. They inform engineering standards.

### Jane Street

- `Production Engineering When Trading Billions of Dollars a Day`
  - Relevance: operational failure modes, production discipline in trading systems.
  - URL: https://www.janestreet.com/tech-talks/production-engineering-when-trading-billions-of-dollars-a-day
- `How to Build an Exchange`
  - Relevance: matching/crossing engine design, message rates, latency, robustness.
  - URL: https://www.janestreet.com/tech-talks/building-an-exchange/

### D. E. Shaw

- Library page mentioning point-in-time/versioned datasets
  - Relevance: time-travel/versioned datasets are critical for reproducible, non-look-ahead quantitative research.
  - URL: https://www.deshaw.com/library

### Citadel Securities

- Research Platform Data Platform Engineer role
  - Relevance: large-scale simulations are critical to alpha/model development.
  - URL: https://www.citadelsecurities.com/careers/details/research-platform-data-platform-engineer/

---

## Data/API Sources

### Binance

- USDⓈ-M Futures WebSocket Market Streams
  - URL: https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams
- Kline/Candlestick REST Data
  - URL: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
- Aggregate Trade Streams
  - URL: https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Aggregate-Trade-Streams

### HyperLiquid

- Info endpoint
  - URL: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint
- WebSocket
  - URL: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket

### Polars

- Lazy API
  - URL: https://docs.pola.rs/user-guide/concepts/lazy-api/
- `scan_parquet`
  - URL: https://docs.pola.rs/docs/python/dev/reference/api/polars.scan_parquet.html
- `sink_parquet`
  - URL: https://docs.pola.rs/api/python/stable/reference/api/polars.LazyFrame.sink_parquet.html

### DuckDB

- Larger-than-memory workloads
  - URL: https://duckdb.org/docs/current/guides/performance/how_to_tune_workloads.html
- Memory management
  - URL: https://duckdb.org/2024/07/09/memory-management.html
- Parquet tips
  - URL: https://duckdb.org/docs/current/data/parquet/tips.html
