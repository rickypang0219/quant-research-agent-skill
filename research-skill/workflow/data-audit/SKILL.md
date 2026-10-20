---
name: data-audit
description: Use before quant research or backtesting to audit market data quality, timestamp semantics, schema validity, missing data, duplicates, stale prices, survivorship bias, contract specs, funding alignment, order book reconstruction, and point-in-time universe correctness.
---

# Data Audit Workflow

## Purpose

Stop bad data from becoming fake alpha. Use this workflow before signal research, backtesting, model training, or live ingestion.

## Core Rule

No backtest is meaningful until the data contract is explicit and checked.

## Required Checks

- schema and dtypes;
- timezone and timestamp semantics;
- monotonicity by symbol;
- duplicate rows/events;
- missing intervals;
- stale prices;
- zero/negative price or volume;
- OHLC consistency;
- split/corporate-action adjustment for equities;
- funding timestamp alignment for perps;
- contract specs and tick/lot/min-notional history;
- point-in-time universe;
- order book crossed/locked states;
- trade/book ordering;
- exchange outages and maintenance.

## Output Standard

1. Data source
2. Schema
3. Timestamp semantics
4. Audit tests
5. Issues found
6. Repair policy
7. Residual risk
8. Go/no-go for research

