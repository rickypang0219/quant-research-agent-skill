# Quant Trading System Source Map

Use this source map for trading-system architecture, event-driven backtesting, live execution, reconciliation, observability, and research-to-production workflows.

## Open-Source Trading Engine References

- NautilusTrader documentation: event-driven architecture, deterministic backtesting, live trading with reconciliation, Rust core, Python API, and research-to-live parity.
- QuantConnect LEAN documentation: open-source algorithmic trading engine, modular system design, research/backtest/live workflow, portfolio/accounting abstractions, survivorship-bias-aware data handling.

## Public Firm / Practitioner References

- Jane Street official technology material and OCaml public ecosystem material: static typing, in-house trading/risk systems, research tools, infrastructure, and cross-functional trading/research/engineering.
- Citadel/Citadel Securities official material: scientific hypothesis testing, large datasets, simulation, high-performance C++/HPC, electronic trading, market microstructure, and production ownership.
- Tower Research official material: market access, data, compute infrastructure, risk management, high-performance platform, and quant/core-engineering feedback loops.
- D. E. Shaw official material: systematic investing, quantitative tools, independent sources of return, collaboration, and risk/reward discipline.
- Renaissance Technologies official material: mathematical and statistical methods in investment-program design and execution.

## Engineering Claims These Sources Support

- Use deterministic event-driven simulation before live trading.
- Preserve semantic parity between research, backtest, paper, and live where possible.
- Build explicit order, fill, position, balance, and risk state machines.
- Reconcile internal state against venue state.
- Treat observability and incident handling as first-class system modules.
- Use strong typing and schemas at boundaries.
- Avoid overbuilding frameworks before a signal or system behavior is proven.

They do not support claims that any particular strategy has alpha.

