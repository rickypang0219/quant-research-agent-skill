# Steven Shreve Lens Examples

## Example 1 - Backtest Leakage as Filtration Error

Bad code idea:

```text
Use close_t to compute signal_t and earn close_t - close_{t-1}.
```

Shreve-style diagnosis:

```text
The position is not predictable with respect to the trading filtration. It uses information from the interval whose return it claims to earn.
```

Fix:

```text
signal_t = function(data available at t)
position_{t+1} = execution(signal_t)
pnl_{t+1} = position_t * return_{t+1}
```

## Example 2 - Physical vs Risk-Neutral Probability

Question:

```text
If option-implied probability says a crash is likely, should I short spot?
```

Answer:

```text
Not directly. Option-implied probabilities are risk-neutral and include risk premia, supply/demand, and hedging pressure. A trading signal under the physical measure must be estimated separately and tested after costs.
```

## Example 3 - Stochastic Control for Execution

Problem:

```text
Liquidate inventory q_0 over [0, T] while balancing impact cost and price risk.
```

State:

- inventory `q_t`;
- price `S_t`;
- liquidity/volatility state;
- time remaining.

Control:

- trading rate `v_t`.

Objective:

```text
minimize expected cost + risk penalty + terminal inventory penalty
```

Implementation warning:

```text
Continuous trading rate must become child orders with tick size, lot size, participation cap, and exchange latency.
```

## Example 4 - Transaction Costs Break Continuous Rebalancing

Frictionless delta hedging says rebalance continuously. With spread and fees, this can be impossible or uneconomic.

Better formulation:

- define no-trade band around target delta;
- rebalance only when delta exits the band;
- stress transaction costs and volatility;
- measure hedging error versus cost.

## Example 5 - Diffusion Approximation for LOB Queues

Question:

```text
Can we approximate bid/ask queue sizes by a diffusion under high event intensity?
```

Check:

- event arrivals are high frequency;
- first and second moments are stable enough;
- state constraints at zero are handled;
- approximation is tested against actual queue depletion probabilities.

Reject if:

- venue has sparse updates;
- hidden liquidity dominates;
- event clustering invalidates simple diffusion scaling;
- crypto exchange data quality is poor.

