# Quant Trading System Experiments

## Experiment 1 - Deterministic Event Replay

Goal:

Verify that the same input event stream produces identical orders, fills, positions, and PnL across repeated runs.

Pass condition:

- identical output files or hashes;
- stable ordering for equal timestamps;
- no hidden dependency on wall-clock time.

## Experiment 2 - PnL Toy Ledger

Goal:

Prove accounting correctness on a small hand-computable example.

Cases:

- buy then price rises;
- buy then sell with fee;
- partial fill;
- funding payment;
- short position;
- rejected order.

## Experiment 3 - Risk Gate Breach

Goal:

Verify that risk checks block invalid orders before execution.

Cases:

- max notional breached;
- max gross breached;
- stale data;
- max daily loss;
- liquidation-distance breach;
- disabled symbol.

## Experiment 4 - Restart and Reconciliation

Goal:

Prove the system can restart and reconcile internal state against exchange state.

Pass condition:

- open orders recovered;
- positions and balances matched;
- unknown fills handled;
- trading remains disabled until reconciliation completes.

## Experiment 5 - Latency and Slippage Stress

Goal:

Measure whether strategy performance survives delayed decision/order/fill timing.

Stress:

- 100 ms;
- 500 ms;
- 1 s;
- 5 s;
- 30 s;
- next bar.

Reject if profitability relies on impossible timing.

