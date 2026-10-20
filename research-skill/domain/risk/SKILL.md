---
name: risk
description: Use for quant trading risk: volatility, drawdown, leverage, exposure, factor risk, liquidity, funding, basis, tail risk, liquidation risk, portfolio constraints, sizing, capital allocation, stress testing, and live risk controls.
---

# Quant Risk Skill

## Scope

Use this skill whenever a strategy, backtest, portfolio, or live system involves sizing, leverage, exposure, drawdown, liquidation, factor risk, concentration, capacity, funding, or operational loss.

Risk is not a post-processing metric. Risk is part of the strategy definition.

## Source Basis

Use:

- Andrew Lo for adaptive markets, serial correlation, liquidity stress, and systemic/crowding risk.
- Khandani and Lo for quant crowding and forced deleveraging in market-neutral strategies.
- Avellaneda-Stoikov and Ho-Stoll for inventory risk in market making.
- Almgren-Chriss and market-impact literature for execution/capacity risk.
- Fama-French/Carhart/Asness-style factors for exposure attribution.
- Official firm material only as engineering/risk-practice context: risk systems, monitoring, simulation, and infrastructure.

## Non-Negotiable Risk Questions

For any strategy ask:

1. What can lose money?
2. How fast can it lose money?
3. What position state creates the loss?
4. What market state makes that loss more likely?
5. What operational failure amplifies it?
6. What limit prevents it?
7. What monitor detects it?
8. What action reduces it?
9. What is the kill switch?
10. Who or what reconciles actual state against expected state?

## Risk Dimensions

Always consider:

- market beta and factor exposure;
- gross/net exposure;
- leverage and margin;
- realized and forecast volatility;
- drawdown and drawdown duration;
- liquidity and capacity;
- concentration;
- funding/borrow/basis;
- correlation breakdown;
- tail losses and gap risk;
- liquidation distance for perps/futures;
- inventory risk for market making;
- exchange/API/ops failure;
- model risk and parameter fragility.

## Position Sizing Principles

Sizing must be tied to a risk unit:

- volatility target;
- expected shortfall target;
- max loss per trade;
- liquidity participation cap;
- margin/liquidation distance;
- factor-risk budget;
- inventory bound;
- per-symbol and sector caps.

Reject vague sizing such as:

```text
Use 1x because it seems safe.
```

Prefer:

```text
Set target notional so ex-ante daily volatility contribution is <= 20 bps of equity, per-asset notional <= 5% of trailing 1h dollar volume, liquidation distance >= 5 sigma, and portfolio gross <= 1.5.
```

## Stress Tests

Minimum stress set:

- fees +50% and +100%;
- spread/slippage 2x and 3x;
- volatility 2x;
- liquidity 50% lower;
- funding/borrow 2x worse;
- delayed execution by 1, 5, and 30 seconds for intraday systems;
- top asset unavailable;
- exchange outage;
- correlated unwind;
- largest historical drawdown replay;
- parameter perturbation;
- signal sign flip in one regime.

## Output Standard

When invoked, produce:

1. Risk inventory
2. Exposure table
3. Sizing rule
4. Loss scenarios
5. Limits
6. Monitoring
7. Kill-switch conditions
8. Required tests
9. Verdict

