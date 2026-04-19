# Backtest Code Review Guide

## 1. Core Anti-Look-Ahead Pattern

Correct vectorized pattern:

```python
signal = compute_signal(data)          # uses data available at t
position = signal.shift(1)             # position active on next bar
returns = close.pct_change()
pnl = position * returns
```

Dangerous pattern:

```python
signal = compute_signal(close)
pnl = signal * close.pct_change()
```

The second pattern often uses the same close for both decision and profit.

---

## 2. Quantity-Based PnL Pattern

Preferred explicit accounting:

```python
# target_notional[t] is decided at t after observing allowed data
target_qty = target_notional / fill_price

# trade to target
delta_qty = target_qty - qty.shift(1).fill_null(0)
fee = abs(delta_qty) * fill_price * fee_rate

# previous position earns price move
price_pnl = qty.shift(1).fill_null(0) * (price - price.shift(1))

net_pnl = price_pnl - fee - slippage - funding
nav = initial_nav + net_pnl.cumsum()
```

Review points:

- `qty.shift(1)` should earn price movement.
- `delta_qty` should generate cost.
- fill price should be realistic.

---

## 3. Polars Review Points

Check:

- `shift(1)` is applied in the correct group for multi-asset data.
- `over("symbol")` is used where needed.
- rolling windows do not include future values.
- joins are `asof` joins only when causally safe.
- forward fills do not cross asset boundaries.
- timezone conversion is explicit.
- lazy queries are collected only after filters/projections are applied.

Example group-safe lag:

```python
pl.col("signal").shift(1).over("symbol").alias("position")
```

---

## 4. Pandas Review Points

Check:

- `shift()` direction
- `groupby().shift()` for multi-asset data
- accidental alignment by index
- joins that create future data leakage
- `fillna(method="ffill")` across assets
- rolling features with `center=True`
- use of full-sample mean/std in z-scores

Dangerous:

```python
df["z"] = (df["x"] - df["x"].mean()) / df["x"].std()
```

For time-series research, this uses future information.

Better:

```python
mu = df["x"].rolling(window).mean()
sigma = df["x"].rolling(window).std()
df["z"] = (df["x"] - mu) / sigma
```

Then shift signal before trading.

---

## 5. Event-Driven Code Review Points

Check event ordering:

```text
MarketEvent
-> SignalEvent
-> OrderEvent
-> FillEvent
-> PortfolioUpdate
```

Common bugs:

- portfolio updated before fill
- signal sees future market event
- fill generated without order
- order filled at impossible price
- cancel fills after cancellation without latency model
- partial fills not reflected in remaining order quantity
- cash not reduced by fees
- rejected orders ignored

---

## 6. Required Unit Tests

### Test 1: Previous Position Earns Return

Use hand-computable prices and positions.

### Test 2: Fees Charged on Position Change

No position change means no fee.

### Test 3: Round Trip Trade

Buy then sell at same price should lose fees/spread.

### Test 4: No Data, No Trade

Missing price should not create fake PnL.

### Test 5: Multi-Asset Group Lag

Asset A signal must not leak into asset B.

### Test 6: Train/Test Boundary

Rolling features at the start of test period must not use future test values for parameter fitting.

---

## 7. Minimal Toy Test

```python
import numpy as np

price = np.array([100.0, 101.0, 103.0, 102.0])
qty = np.array([0.0, 1.0, 1.0, -1.0])

price_pnl = np.r_[0.0, qty[:-1] * np.diff(price)]
expected = np.array([0.0, 0.0, 2.0, -1.0])

assert np.allclose(price_pnl, expected)
```

If the production backtest cannot pass simple tests like this, do not trust the full equity curve.
