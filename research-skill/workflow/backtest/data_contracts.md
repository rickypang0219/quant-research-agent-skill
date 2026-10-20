# Data Contracts and Storage Layout

## Philosophy

A backtest is only as good as the timestamp discipline of its data.

Every dataset needs two timestamps:

```text
event_time:
    When the exchange says the market event happened.

available_time:
    When your strategy could have known the event.
```

For historical OHLCV, these are often treated as identical, but they are not conceptually identical.

For fundamentals, macro, funding, index membership, or exchange metadata, `available_time` is essential.

---

## Canonical OHLCV Schema

```text
exchange: str
market: str                # spot, perp, futures, options
symbol: str
instrument_id: str
timeframe: str             # 1m, 5m, 15m, 1h, 1d
open_time: datetime[UTC]
close_time: datetime[UTC]
available_time: datetime[UTC]
open: float64
high: float64
low: float64
close: float64
volume_base: float64
volume_quote: float64
trade_count: int64
source: str
ingested_at: datetime[UTC]
```

Validation:

```text
low <= open <= high
low <= close <= high
volume_base >= 0
volume_quote >= 0
open_time < close_time <= available_time
```

---

## Canonical Trade Schema

```text
exchange: str
market: str
symbol: str
trade_id: str
event_time: datetime[UTC]
available_time: datetime[UTC]
price: float64
quantity_base: float64
quantity_quote: float64
aggressor_side: str        # buy, sell, unknown
is_buyer_maker: bool | null
source_sequence: int64 | null
source: str
ingested_at: datetime[UTC]
```

---

## Canonical L2 Book Update Schema

```text
exchange: str
market: str
symbol: str
event_time: datetime[UTC]
available_time: datetime[UTC]
sequence_id: int64 | null
prev_sequence_id: int64 | null
side: str                  # bid or ask
price: float64
quantity_base: float64     # zero means delete level
action: str                # upsert/delete/snapshot
source: str
ingested_at: datetime[UTC]
```

---

## Canonical Funding Schema

```text
exchange: str
market: str
symbol: str
funding_time: datetime[UTC]
available_time: datetime[UTC]
funding_rate: float64
mark_price: float64 | null
index_price: float64 | null
source: str
ingested_at: datetime[UTC]
```

---

## Canonical Instrument Spec Schema

```text
exchange: str
market: str
symbol: str
instrument_id: str
valid_from: datetime[UTC]
valid_to: datetime[UTC] | null
tick_size: float64
lot_size: float64
min_qty: float64
min_notional: float64
contract_size: float64
quote_asset: str
base_asset: str
margin_asset: str | null
source: str
ingested_at: datetime[UTC]
```

Instrument specs must be versioned. Tick size, lot size, and min notional can change.

---

## Backtest Orders Schema

```text
run_id: str
order_id: str
parent_order_id: str | null
timestamp: datetime[UTC]
symbol: str
side: str                  # buy/sell
order_type: str            # market/limit/stop/post_only
quantity: float64
limit_price: float64 | null
time_in_force: str
status: str
reason: str | null
strategy_id: str
signal_id: str | null
```

---

## Backtest Fills Schema

```text
run_id: str
fill_id: str
order_id: str
timestamp: datetime[UTC]
symbol: str
side: str
quantity: float64
fill_price: float64
fee: float64
fee_asset: str
liquidity_flag: str        # maker/taker/unknown
slippage_bps: float64 | null
latency_ms: float64 | null
```

---

## Backtest Position Schema

```text
run_id: str
timestamp: datetime[UTC]
symbol: str
quantity: float64
mark_price: float64
notional: float64
unrealized_pnl: float64
realized_pnl: float64
fee_paid: float64
funding_paid: float64
```

---

## Backtest Equity Schema

```text
run_id: str
timestamp: datetime[UTC]
cash: float64
gross_exposure: float64
net_exposure: float64
equity: float64
pnl: float64
fees: float64
slippage: float64
funding: float64
drawdown: float64
leverage: float64
```

---

## Experiment Manifest

Every run should write:

```yaml
run_id: "2026-04-19T12-00-00Z_zscore_btc_1h"
strategy_name: "zscore_mean_reversion"
git_commit: "..."
data_version: "..."
start_date: "2020-01-01"
end_date: "2026-01-01"
train_start: "2020-01-01"
train_end: "2023-12-31"
test_start: "2024-01-01"
test_end: "2026-01-01"
execution_model: "next_bar_open"
cost_model:
  taker_fee_bps: 6
  maker_fee_bps: 3
  slippage_bps: 2
parameters:
  lookback: 96
  z_entry: 2.0
  z_exit: 0.0
```

---

## Directory Layout

```text
workflow/backtest/
  SKILL.md
  formulas.md
  experiments.md
  data_contracts.md
  sources.md

data/
  raw/
  cleaned/
  features/
  backtests/
```

Recommended partitioning:

```text
/data/raw/exchange=binance/market=perp/symbol=BTCUSDT/datatype=ohlcv/timeframe=1h/year=2020/part-000.parquet
```

---

## Reproducibility Requirements

A backtest is reproducible only if you can recover:

```text
code version
data version
environment lock file
strategy config
parameter search space
selected parameter set
random seed
cost model
execution model
train/test split
raw orders
raw fills
equity curve
metrics
```
