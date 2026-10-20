# Data Audit Examples

## Example 1 - Missing Crypto Bars

If BTCUSDT 1h bars have missing timestamps:

```text
Do not forward-fill price and pretend trading was possible.
```

Classify:

- exchange outage;
- collector outage;
- no-trade interval;
- bad API pagination.

Then rerun the backtest with those intervals disabled or repaired transparently.

## Example 2 - Funding Leakage

If a strategy uses funding rate announced at `t` to trade before `t`, verify the exchange publication and settlement convention.

Verdict:

```text
Funding data is not usable until its availability timestamp is known.
```

