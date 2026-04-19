# Data Audit Checklist

## Bars

- [ ] Timestamp timezone declared.
- [ ] Bars sorted by symbol and timestamp.
- [ ] No duplicate symbol/timestamp rows.
- [ ] Expected interval count checked.
- [ ] OHLC relationship valid: low <= open/close/high and high >= open/close/low.
- [ ] Volume non-negative.
- [ ] Zero-volume bars handled explicitly.
- [ ] Missing bars classified as outage, no-trade, or data failure.

## Trades

- [ ] Trade IDs unique where available.
- [ ] Timestamp ordering checked.
- [ ] Side/aggressor convention documented.
- [ ] Price and quantity positive.
- [ ] Duplicate trade events detected.

## Order Book

- [ ] Bid <= ask.
- [ ] Depth non-negative.
- [ ] Sequence gaps detected.
- [ ] Snapshot/delta reconciliation tested.
- [ ] Crossed/locked books classified.
- [ ] Book timestamp and local receive timestamp separated.

## Perps/Futures

- [ ] Funding timestamps aligned.
- [ ] Funding applies to held position at correct time.
- [ ] Contract multiplier known.
- [ ] Tick size, lot size, min notional known.
- [ ] Delisting/expiry handled.

