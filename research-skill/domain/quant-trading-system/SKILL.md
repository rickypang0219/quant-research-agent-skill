---
name: quant-trading-system
description: Use for building, debugging, and productionizing quant trading systems, including event-driven backtesting engines, research prototypes, paper-trading pipelines, Rust live-trading infrastructure, market-data ingestion, execution/risk engines, observability, databases, numerical safety, network failure handling, and implementation planning.
---


# SKILLS.md — Quant Trading System Builder

## 0. Skill identity

**Skill name:** `quant-trading-system-builder`  
**Default path:** `/skills/quant-trading-system/SKILLS.md`  
**Purpose:** Help build, debug, and evolve quant trading research systems, event-driven backtesting engines, paper-trading systems, and production-grade Rust execution systems.

Use this skill whenever the user asks about:

- event-driven backtesting engines
- live-trading architecture
- paper trading
- market-data ingestion
- order book / matching engine simulation
- execution engine design
- portfolio/risk engine design
- strategy research infrastructure
- Python-to-Rust migration
- performance debugging
- numerical robustness
- observability, metrics, and monitoring
- AWS deployment for quant systems
- data engineering for trading systems

This skill is **not** a promise that a strategy is profitable. It is an engineering, research, debugging, and risk-control skill.

---

## 1. Core philosophy

Build trading systems in layers:

```text
research idea
    ↓
minimal prototype
    ↓
deterministic backtest
    ↓
paper trading
    ↓
production hardening
    ↓
small-capital live deployment
    ↓
scale only after evidence
```

Default rule:

> Python is for research, prototyping, diagnostics, paper trading, and exploratory analytics.  
> Rust is for production execution, low-latency components, correctness-critical state machines, and live trading.

Always start with a **proof of concept**. Do not build a huge framework before the core idea is tested.

---

## 2. Non-negotiable engineering principles

### 2.1 Prototype first

For a brand-new project:

1. Implement only the minimum useful core.
2. Use real or realistic data as early as possible.
3. Verify event ordering, fills, PnL, and risk accounting.
4. Add abstractions only when repeated code or complexity demands it.
5. Avoid framework-building before proof of concept.

Bad default:

```text
Build full exchange adapter + strategy framework + portfolio engine + optimizer + UI before testing one signal.
```

Good default:

```text
Load data → emit market events → generate orders → simulate fills → compute PnL/risk → inspect failure modes.
```

### 2.2 Functions first, abstractions later

In Python:

- prefer functions and small modules first
- avoid over-abstracting everything into classes, ABCs, factories, and inheritance trees
- introduce classes only when they represent stable stateful concepts:
  - `BacktestState`
  - `PortfolioState`
  - `OrderBook`
  - `ExecutionReport`
  - `RiskLimits`
  - `StrategyConfig`
- introduce protocols/ABCs only when there are multiple concrete implementations:
  - historical data feed vs live data feed
  - simulated exchange vs real exchange
  - paper broker vs real broker

### 2.3 Better names over excessive comments

Use names that reveal intent.

Prefer:

```python
def compute_target_quantity(position_notional: float, mark_price: float) -> float:
    ...
```

Avoid:

```python
def calc(x: float, y: float) -> float:
    ...
```

Comments should explain **why**, not restate **what**.

### 2.4 Type everything at function boundaries

Every Python function must have type hints for parameters and return values.

```python
def compute_log_returns(prices: pl.DataFrame, price_columns: list[str]) -> pl.DataFrame:
    ...
```

Use `pydantic` for external input validation, configuration, API payloads, exchange messages, and persisted schemas.

### 2.5 Determinism first

Backtests must be deterministic:

- stable event ordering
- stable random seeds
- stable fill rules
- explicit timestamp semantics
- no hidden look-ahead
- no accidental future data
- reproducible configuration
- versioned datasets

Never trust a backtest until it can be rerun and produce the same result.

---

## 3. Example project structure

Use this structure for new projects unless the user already has a better one.

```text
quant-trading-system/
├── README.md
├── pyproject.toml
├── uv.lock
├── Cargo.toml
├── .python-version
├── .gitignore
├── .env.example
├── Makefile
├── configs/
│   ├── research.yaml
│   ├── paper.yaml
│   └── live.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── notebooks/
├── reports/
│   ├── figures/
│   └── backtests/
├── python/
│   └── qts/
│       ├── __init__.py
│       ├── data/
│       │   ├── load_ohlcv.py
│       │   ├── validate_bars.py
│       │   └── feature_store.py
│       ├── research/
│       │   ├── signals.py
│       │   ├── portfolio.py
│       │   └── diagnostics.py
│       ├── backtest/
│       │   ├── events.py
│       │   ├── engine.py
│       │   ├── fills.py
│       │   ├── accounting.py
│       │   └── metrics.py
│       ├── paper/
│       │   ├── broker.py
│       │   ├── risk_gate.py
│       │   └── order_proposals.py
│       ├── observability/
│       │   ├── metrics.py
│       │   └── logging.py
│       └── schemas/
│           ├── market_data.py
│           ├── orders.py
│           └── configs.py
├── rust/
│   ├── crates/
│   │   ├── qts-core/
│   │   │   ├── Cargo.toml
│   │   │   └── src/
│   │   ├── qts-execution/
│   │   │   ├── Cargo.toml
│   │   │   └── src/
│   │   ├── qts-market-data/
│   │   │   ├── Cargo.toml
│   │   │   └── src/
│   │   └── qts-risk/
│   │       ├── Cargo.toml
│   │       └── src/
│   └── benches/
├── schemas/
│   ├── order_event.schema.json
│   ├── market_event.schema.json
│   └── execution_report.schema.json
├── sql/
│   ├── init_postgres.sql
│   ├── hypertables.sql
│   └── indexes.sql
├── infra/
│   ├── docker-compose.yml
│   ├── prometheus.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── datasources/
│   └── aws/
│       ├── lambda/
│       ├── iam/
│       └── secrets/
├── tests/
│   ├── python/
│   └── rust/
└── skills/
    └── quant-trading-system/
        └── SKILLS.md
```

If integrating with the existing professor-skill structure, use:

```text
/prof/strang/SKILLS.md
/prof/lo/SKILLS.md
/prof/brunton/SKILLS.md
/prof/simons/SKILLS.md
/skills/quant-trading-system/SKILLS.md
/skills/quant-research-router.md
```

---

## 4. How to combine with professor skills

When solving a quant-system problem, route through these modules:

```text
Strang  → linear algebra, projections, PCA, least squares, numerical modeling
Lo      → financial economics, Adaptive Markets, risk, market realism, AI in finance
Brunton → dynamical systems, DMD, SINDy, Koopman, data-driven discovery/control
Simons  → empirical rigor, statistical arbitrage, signal testing, research culture
QTS     → software architecture, backtesting, debugging, production trading systems
```

Default routing:

| Problem | Skill mix |
|---|---|
| PCA residual stat-arb backtest | Strang + Lo + Simons + QTS |
| SINDy / DMD feature discovery | Brunton + Lo + QTS |
| Event-driven backtest design | QTS + Simons |
| Risk and live-trading controls | Lo + QTS + Simons |
| Order book / low-latency engine | QTS + Strang |
| Strategy research plan | Lo + Simons + Brunton + Strang + QTS |
| Debugging Python prototype | QTS |
| Migrating Python prototype to Rust | QTS + Simons |

---

## 5. Event-driven backtesting engine requirements

Build the backtester as an event-driven simulator inspired by NautilusTrader-like research-to-live architecture.

### 5.1 Core events

Minimum event types:

```text
MarketDataEvent
SignalEvent
OrderIntentEvent
OrderAcceptedEvent
OrderRejectedEvent
OrderFilledEvent
OrderCancelledEvent
RiskLimitBreachedEvent
PortfolioValuationEvent
EndOfBarEvent
EndOfDayEvent
DeadLetterEvent
```

### 5.2 Minimal Python event model

Prefer simple dataclasses or Pydantic models.

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True, slots=True)
class MarketDataEvent:
    symbol: str
    ts_ns: int
    bid: float | None
    ask: float | None
    last: float | None
    volume: float


@dataclass(frozen=True, slots=True)
class OrderIntentEvent:
    strategy_id: str
    symbol: str
    side: OrderSide
    quantity: float
    order_type: Literal["MARKET", "LIMIT"]
    limit_price: float | None
    ts_ns: int
```

### 5.3 Backtest event loop

A minimal engine should:

1. read market events
2. update market state
3. call strategy logic
4. create order intents
5. pass intents through risk gate
6. simulate fills
7. update portfolio/accounting
8. record metrics and logs
9. push malformed/unhandled events to dead-letter queue

Skeleton:

```python
def run_backtest(
    market_events: Iterable[MarketDataEvent],
    strategy: StrategyFn,
    state: BacktestState,
    config: BacktestConfig,
) -> BacktestResult:
    for market_event in market_events:
        update_market_state(state, market_event)

        order_intents = strategy(market_event, state)

        for intent in order_intents:
            risk_result = check_order_risk(intent, state, config.risk_limits)
            if not risk_result.is_allowed:
                record_risk_rejection(intent, risk_result, state)
                continue

            fill_events = simulate_fills(intent, state.market_state, config.fill_model)
            for fill in fill_events:
                apply_fill(fill, state)
                record_fill(fill, state)

        mark_portfolio_to_market(state, market_event.ts_ns)

    return build_backtest_result(state)
```

### 5.4 Required backtest features

The engine should eventually support:

- event-time ordering
- bar, tick, quote, trade, and order-book events
- no look-ahead bias
- exchange calendars or 24/7 crypto calendars
- latency model
- slippage model
- fee model
- market impact model
- partial fills
- rejected orders
- cancelled orders
- time-in-force
- order queue position approximation
- borrow/funding model
- funding fees for perpetual futures
- liquidation checks
- portfolio margin constraints
- configurable risk limits
- reproducible run metadata

### 5.5 Backtest realism checks

Every backtest report must answer:

1. Did the strategy use future information?
2. Were all fills achievable?
3. Were fees/slippage/funding included?
4. Was liquidity/capacity checked?
5. Were delisted/missing assets handled?
6. Were timestamps aligned correctly?
7. Is performance concentrated in a few trades/days/assets?
8. Does the strategy survive parameter perturbation?
9. Does the signal decay out-of-sample?
10. Would live execution change the result materially?

---

## 6. Python stack

Use Python for research, prototyping, diagnostics, batch analytics, and paper trading.

### 6.1 Package and environment management

Use `uv`.

Recommended commands:

```bash
uv init quant-trading-system
uv python pin 3.12
uv add polars numpy scipy numba pydantic requests httpx websockets plotly matplotlib sqlalchemy psycopg[binary] prometheus-client
uv add --dev ruff ty pytest pytest-cov hypothesis
uv lock
```

Notes:

- `uv` is the default Python package/project manager.
- `ruff` is the default linter and formatter.
- `ty` is allowed in the dev group, but because it is currently beta, do not make it the only production gate unless explicitly requested.
- For stricter production type checking, optionally also support `pyright` or `mypy`.

### 6.2 Suggested `pyproject.toml`

```toml
[project]
name = "quant-trading-system"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "polars",
    "numpy",
    "scipy",
    "numba",
    "pydantic",
    "requests",
    "httpx",
    "websockets",
    "plotly",
    "matplotlib",
    "sqlalchemy",
    "psycopg[binary]",
    "prometheus-client",
]

[dependency-groups]
dev = [
    "ruff",
    "ty",
    "pytest",
    "pytest-cov",
    "hypothesis",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "C4", "ARG", "PL"]
ignore = ["PLR0913"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ty]
environment = { python = ".venv" }
```

### 6.3 Data processing

Default:

- `polars` for large tabular/time-series data
- `numpy` for arrays and vectorized numerical routines
- `scipy` for optimization, statistics, linear algebra, signal processing
- `numba` for JIT acceleration of tight numerical loops
- `pandas` only when required by third-party libraries or quick notebook compatibility

### 6.4 Visualization

Use:

- `plotly` for interactive research reports
- `matplotlib` for static figures, papers, and minimal dependencies
- every plot must have a clear diagnostic purpose

### 6.5 API and streaming

Use:

- `requests` for simple blocking HTTP calls
- `httpx` for modern sync/async HTTP clients
- `asyncio` for async workflows
- `websockets` or exchange-specific SDKs for websocket streams
- `asyncio.Queue` for async event queues
- timeouts on all network operations
- retries with exponential backoff for safe/idempotent calls
- no infinite retry without circuit breaker

---

## 7. Rust stack

Use Rust for production trading, low-latency systems, strongly typed execution logic, state machines, and components where correctness and performance matter.

### 7.1 Package management

Use `Cargo.toml`.

Workspace structure:

```toml
[workspace]
members = [
    "rust/crates/qts-core",
    "rust/crates/qts-market-data",
    "rust/crates/qts-execution",
    "rust/crates/qts-risk",
]
resolver = "2"

[workspace.package]
edition = "2021"
license = "MIT"
```

### 7.2 Suggested Rust crates

Use as appropriate:

```toml
[dependencies]
anyhow = "1"
thiserror = "1"
tracing = "0.1"
tracing-subscriber = "0.3"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tokio = { version = "1", features = ["full"] }
reqwest = { version = "0.12", features = ["json"] }
tokio-tungstenite = "0.26"
polars = { version = "0.46", features = ["lazy", "parquet"] }
rayon = "1"
crossbeam = "0.8"
parking_lot = "0.12"
dashmap = "6"
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "chrono", "rust_decimal"] }
rust_decimal = "1"
chrono = { version = "0.4", features = ["serde"] }
```

Version numbers may change. Verify current crate versions when starting a new project.

### 7.3 Async runtime

Default to `tokio` for production network systems because it has a mature ecosystem for async I/O, timers, synchronization, and networking.

Use `smol` only for smaller async applications where simplicity is preferred and ecosystem requirements are limited.

### 7.4 Multiprocessing and concurrency

Use:

- `rayon` for CPU-bound parallel computation
- `tokio` for network I/O and async tasks
- `crossbeam` channels for low-level concurrency
- SPSC queues or disruptor-like ring buffers for low-latency pipelines
- bounded queues for backpressure
- cache padding to prevent false sharing in hot paths
- CPU affinity for latency-sensitive threads
- explicit core pinning only after profiling

Avoid:

- unbounded channels in live execution
- blocking calls inside async runtime workers
- mixing locks and async awaits without care
- global mutable state
- excessive cloning in hot paths

### 7.5 Low-latency principles

For production execution components:

1. Keep hot-path data structures contiguous and cache-friendly.
2. Avoid heap allocation in tight loops.
3. Preallocate buffers.
4. Avoid dynamic dispatch in hot paths unless profiling says it is fine.
5. Use bounded queues.
6. Separate ingestion, strategy, risk, and execution threads.
7. Measure p50, p95, p99, and p99.9 latency.
8. Track dropped messages and queue depth.
9. Pin hot threads to CPU cores only after proving it improves tail latency.
10. Keep risk checks deterministic and fast.

### 7.6 Rust coding style

Follow idiomatic Rust:

- explicit ownership
- small structs with clear responsibility
- `Result<T, E>` for recoverable errors
- `thiserror` for domain errors
- `anyhow` only at application boundaries
- no `unwrap()` in production paths
- no `panic!()` in live trading paths except unrecoverable startup validation
- use `tracing` for structured logs
- write tests for state transitions and risk logic
- use benchmarks for performance-sensitive code

---

## 8. Database and storage

### 8.1 Default choice

Use PostgreSQL as the default relational database.

Use TimescaleDB when time-series scale matters because it extends PostgreSQL with time-series-oriented storage and query features.

Use object storage for large immutable datasets:

- local Parquet for research
- S3 for shared historical data
- PostgreSQL/TimescaleDB for indexed metadata, bars, trades, metrics, and state snapshots

### 8.2 Suggested database usage

Use PostgreSQL/TimescaleDB for:

- OHLCV bars
- trades
- quotes
- order book snapshots
- signals
- orders
- fills
- positions
- risk snapshots
- strategy run metadata
- monitoring metadata

Use S3 for:

- raw exchange payload archives
- large Parquet datasets
- backtest artifacts
- research reports
- model checkpoints

Use DynamoDB only when:

- low-latency key-value access is useful
- relational/time-series queries are not needed
- simple state lookup is enough
- live-trading latency requirements do not require colocated/local storage

### 8.3 Schema principles

Every market data table must include:

```text
exchange
symbol
timestamp_exchange
timestamp_received
data_type
source
ingestion_run_id
```

Every order/fill table must include:

```text
strategy_id
account_id
exchange
symbol
client_order_id
exchange_order_id
side
quantity
price
status
timestamp_sent
timestamp_ack
timestamp_exchange
timestamp_received
```

---

## 9. Observability and monitoring

Use Prometheus + Grafana for metrics and dashboards.

### 9.1 Required metrics

For backtesting:

```text
backtest_events_processed_total
backtest_orders_simulated_total
backtest_fills_simulated_total
backtest_dead_letter_events_total
backtest_runtime_seconds
backtest_max_drawdown
backtest_sharpe
backtest_turnover
```

For paper/live trading:

```text
market_data_messages_total
market_data_lag_ms
websocket_reconnects_total
event_queue_depth
event_processing_latency_ms
order_submit_latency_ms
order_ack_latency_ms
order_rejects_total
fills_total
position_notional
gross_exposure
net_exposure
realized_pnl
unrealized_pnl
drawdown
risk_rejections_total
dead_letter_events_total
kill_switch_state
```

For system health:

```text
process_cpu_seconds_total
process_resident_memory_bytes
gc_pause_seconds
network_request_failures_total
database_write_latency_ms
database_read_latency_ms
```

### 9.2 Logging

Use structured logs.

Each log event should include:

```text
timestamp
service
environment
strategy_id
symbol
event_type
correlation_id
message
severity
```

Never log secrets, private keys, API keys, or full authentication headers.

### 9.3 Alerting

Alert on:

- stale market data
- websocket reconnect storm
- rising queue depth
- missing heartbeats
- p99 latency spike
- high order rejection rate
- position exceeds risk limit
- drawdown exceeds threshold
- database write failures
- dead-letter queue growth
- kill switch triggered
- unexpected process restart

---

## 10. Error handling and undefined behavior

### 10.1 Numerical safety

Always handle:

- divide by zero
- overflow / underflow
- NaN
- infinite values
- empty arrays
- zero variance
- singular matrices
- ill-conditioned covariance matrices
- missing timestamps
- duplicated timestamps
- negative or zero prices
- impossible volumes
- unsupported symbols

Use explicit guards:

```python
def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0.0:
        return default
    value = numerator / denominator
    if not np.isfinite(value):
        return default
    return float(value)
```

For vectorized code:

```python
def safe_log_returns(prices: np.ndarray) -> np.ndarray:
    prices = np.asarray(prices, dtype=np.float64)
    valid = np.isfinite(prices) & (prices > 0.0)

    out = np.full(prices.shape, np.nan, dtype=np.float64)
    log_prices = np.full(prices.shape, np.nan, dtype=np.float64)
    log_prices[valid] = np.log(prices[valid])
    out[1:] = log_prices[1:] - log_prices[:-1]
    return out
```

### 10.2 Network safety

For every network request:

- set connect timeout
- set read timeout
- handle no response
- handle non-2xx response
- handle malformed JSON
- handle rate limit
- handle auth failure
- handle clock skew
- handle duplicate messages
- handle out-of-order messages
- handle disconnect/reconnect
- handle idempotency for order submission

### 10.3 Dead-letter queue

Use a dead-letter queue for:

- malformed market data
- unknown event type
- failed schema validation
- unhandled execution report
- order state transition violation
- database write failure after retries
- message that cannot be safely processed

Dead-letter records should include:

```text
event_id
event_type
raw_payload
error_type
error_message
first_seen_timestamp
last_seen_timestamp
retry_count
service
strategy_id
symbol
```

Do not silently drop messages.

---

## 11. Risk management requirements

Every trading system must include a risk gate before orders reach the execution adapter.

Minimum checks:

```text
max_order_notional
max_symbol_position
max_gross_exposure
max_net_exposure
max_leverage
max_daily_loss
max_drawdown
max_order_rate
max_cancel_rate
max_open_orders
symbol_allowlist
exchange_allowlist
min_liquidity
max_spread
max_market_data_staleness
```

Live trading requires:

- kill switch
- manual override
- position flattening path
- exchange disconnect behavior
- stale data protection
- order idempotency
- heartbeat monitor
- daily loss limit
- persistent order state
- reconciliation with exchange
- audit log

Never send live orders directly from a newly written strategy without:

1. backtest
2. paper trading
3. risk review
4. config review
5. secret-management review
6. small-capital staged rollout

---

## 12. AWS deployment preferences

Use AWS when infrastructure is needed.

### 12.1 Preferred services

Use:

- AWS Secrets Manager for API keys, DB passwords, and exchange credentials
- AWS Lambda for CRON-style jobs and lightweight scheduled tasks
- EventBridge Scheduler for schedules
- S3 for raw data and research artifacts
- RDS PostgreSQL or Timescale-compatible PostgreSQL for relational/time-series storage
- ECS/Fargate for long-running services
- CloudWatch for logs and infrastructure metrics
- IAM roles instead of static credentials
- KMS for encryption
- DynamoDB for simple key-value state when relational/time-series queries are unnecessary

### 12.2 Secrets rule

Never store real secrets in:

```text
.env
.env.local
notebooks
Git
Markdown docs
plain config files
logs
```

Use `.env.example` only for variable names and fake placeholders.

---

## 13. Testing requirements

### 13.1 Python tests

Use:

- `pytest`
- `hypothesis` for property-based tests
- deterministic fixtures
- small synthetic datasets
- known-answer tests

Minimum tests:

```text
test_no_lookahead_bias
test_event_ordering_is_stable
test_fill_model_market_order
test_fill_model_limit_order
test_position_accounting_after_fill
test_fee_model
test_pnl_calculation
test_risk_rejects_large_order
test_dead_letter_on_bad_event
test_safe_divide_handles_zero
test_signal_has_expected_shape
```

### 13.2 Rust tests

Use:

- unit tests for state transitions
- integration tests for exchange adapters
- property tests where appropriate
- benchmarks for hot paths
- load tests for queues

Minimum Rust checks:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo bench
```

### 13.3 Python checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
uv run pytest
```

Because `ty` is beta, a project may optionally add `pyright` or `mypy` for stricter production CI.

---

## 14. Implementation plan template

For every new project, produce an implementation plan with:

```text
1. Objective
2. Non-goals
3. Core assumptions
4. Minimal viable prototype
5. Data requirements
6. Event model
7. Backtest design
8. Risk controls
9. Observability
10. Testing plan
11. Production migration path
12. Timeline / milestones
13. Failure modes
14. Open questions
```

### 14.1 Phase 0 — Project skeleton

Deliverables:

- `pyproject.toml`
- `Cargo.toml`
- folder structure
- lint/type/test commands
- README
- minimal config files

Exit criteria:

- Python tests run
- Rust tests run
- CI-like commands documented

### 14.2 Phase 1 — Data ingestion prototype

Deliverables:

- load historical OHLCV
- validate timestamps
- store to Parquet/PostgreSQL
- compute simple features
- plot diagnostics

Exit criteria:

- no duplicated timestamps
- no impossible prices
- data coverage report produced

### 14.3 Phase 2 — Minimal event-driven backtester

Deliverables:

- event definitions
- event loop
- one simple strategy
- fill model
- fee model
- PnL accounting
- metrics report

Exit criteria:

- deterministic rerun
- no look-ahead bias
- known-answer tests pass

### 14.4 Phase 3 — Strategy research loop

Deliverables:

- feature pipeline
- signal module
- portfolio sizing
- risk constraints
- walk-forward split
- report generator

Exit criteria:

- out-of-sample report
- parameter sensitivity report
- transaction cost included

### 14.5 Phase 4 — Paper trading

Deliverables:

- live market data adapter
- paper broker
- order proposal stream
- risk gate
- Prometheus metrics
- Grafana dashboard

Exit criteria:

- paper trades reconcile
- no unhandled events
- kill switch works
- stale data protection works

### 14.6 Phase 5 — Rust production migration

Deliverables:

- Rust market-data service
- Rust risk gate
- Rust execution adapter
- persistent order state
- reconciliation loop
- latency metrics

Exit criteria:

- p99 latency measured
- exchange failure simulated
- restart recovery tested
- small-capital rollout checklist complete

---

## 15. Debugging protocol

When debugging code, follow this order:

1. Reproduce the error.
2. Identify the minimal failing example.
3. Classify the error:
   - syntax
   - type
   - data shape
   - timestamp alignment
   - numerical
   - state transition
   - concurrency
   - network
   - database
   - performance
4. Check assumptions.
5. Add a failing test.
6. Fix the smallest root cause.
7. Rerun tests.
8. Explain the bug in trading-system terms.

### 15.1 Common quant-system bugs

Watch for:

- look-ahead bias
- survivorship bias
- wrong timestamp alignment
- using close price to trade at the same close
- assuming full fills
- ignoring fees/funding/slippage
- double-counting positions
- sign errors in short PnL
- annualizing Sharpe incorrectly
- unstable covariance inverse
- resampling across gaps incorrectly
- timezone bugs
- NaN silently becoming zero
- order state machine invalid transitions
- duplicate websocket messages
- dropped reconnect messages
- race conditions in shared state

---

## 16. Code style preferences

### 16.1 Python naming

Prefer verbs for functions:

```text
load_ohlcv
validate_bars
compute_log_returns
build_market_events
simulate_order_fills
apply_fill_to_portfolio
mark_portfolio_to_market
calculate_max_drawdown
create_order_proposal
check_order_risk
record_dead_letter_event
```

Prefer nouns for data structures:

```text
BacktestState
RiskLimits
MarketDataEvent
OrderIntent
ExecutionReport
PortfolioSnapshot
```

### 16.2 Rust naming

Follow Rust conventions:

```text
snake_case for functions
CamelCase for structs/enums
SCREAMING_SNAKE_CASE for constants
```

Prefer explicit domain names:

```rust
fn apply_fill_to_position(...)
fn check_order_notional_limit(...)
fn update_order_state(...)
fn publish_execution_report(...)
```

---

## 17. Live-trading safety policy

For live trading:

- do not bypass the risk gate
- do not expose exchange secrets
- do not place real orders from unreviewed code
- do not rely on ChatGPT as an autonomous trader
- generate order proposals first
- require human approval before real capital
- use small notional rollout
- monitor continuously
- keep a kill switch
- reconcile positions with exchange

Order proposal format:

```json
{
  "strategy_id": "mean_reversion_v1",
  "symbol": "BTCUSDT",
  "side": "BUY",
  "order_type": "LIMIT",
  "quantity": 0.001,
  "limit_price": 65000.0,
  "max_loss_usdt": 10.0,
  "reason": "Signal crossed entry threshold after risk checks",
  "risk_checks_passed": true,
  "requires_human_approval": true
}
```

---

## 18. Agent response format

When this skill is active, respond in this structure for system-building tasks:

```text
1. Goal
2. Assumptions
3. Minimal design
4. Implementation plan
5. Code or pseudocode
6. Tests
7. Risk / failure modes
8. Next step
```

For debugging tasks:

```text
1. Root cause
2. Minimal reproduction
3. Fix
4. Corrected code
5. Test
6. Why this matters in trading
```

For architecture tasks:

```text
1. System boundary
2. Components
3. Event flow
4. State model
5. Data model
6. Failure handling
7. Observability
8. Deployment path
9. What to prototype first
```

---

## 19. Source basis

This skill is inspired by and should remain compatible with these public tooling and architecture references:

- NautilusTrader-style event-driven, research-to-live trading architecture
- Python official typing and asyncio practices
- Astral `uv`, `ruff`, and `ty`
- Rust Book and Cargo Book
- Tokio async runtime
- PostgreSQL and TimescaleDB for relational/time-series storage
- Prometheus and Grafana for observability
- AWS Secrets Manager and AWS deployment patterns

When exact CLI commands, library versions, or APIs matter, verify the latest documentation before generating production setup instructions.
