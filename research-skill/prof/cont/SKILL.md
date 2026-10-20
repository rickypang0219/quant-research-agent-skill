---
name: cont
description: Use for stochastic-process and mathematical-finance questions involving stylized facts, heavy tails, volatility clustering, jump processes, Levy processes, pathwise/functional Ito calculus, model risk, systemic risk, order-flow imbalance, limit-order-book queue models, market impact, and diffusion approximations for market microstructure.
---

# Rama Cont Lens for Stochastic Processes in Markets

> Status: curated synthesis from public academic and official sources, not a literal exhaustive archive of every message, interview, conference talk, paper, lecture, or opinion.

## Scope

Use this lens when a quant problem needs stochastic-process modeling that remains tied to empirical market facts. Cont-style reasoning is especially useful when the user is working with:

- heavy-tailed returns;
- volatility clustering;
- jumps and discontinuities;
- Levy or jump-diffusion models;
- path-dependent payoffs and functionals;
- functional/pathwise Ito calculus;
- stochastic models of order books;
- order flow imbalance;
- market impact;
- systemic risk and network contagion;
- diffusion approximations of high-frequency systems;
- model risk and calibration risk.

## Core Doctrine

Start from empirical facts before selecting a stochastic process.

```text
market data -> stylized facts -> stochastic object -> calibration -> falsification -> trading/risk decision
```

Do not begin with Brownian motion because it is mathematically convenient. Ask whether the data exhibit jumps, heavy tails, volatility clustering, rough/path-dependent behavior, microstructure noise, or state-dependent liquidity.

## Operating Principles

### 1. Stylized facts are constraints, not decoration

Before proposing a model, check:

- unconditional return tails;
- volatility clustering;
- linear return autocorrelation;
- absolute/squared return autocorrelation;
- aggregation across time scales;
- cross-asset dependence;
- intraday seasonality;
- spread/depth/liquidity state.

If the model contradicts dominant stylized facts, it is a toy unless the user explicitly wants a toy.

### 2. Jumps are not just fat tails

Jumps change:

- hedging error;
- option smiles/skews;
- risk-neutral vs physical calibration;
- tail risk;
- stop-loss behavior;
- liquidation risk;
- event-study interpretation.

For trading, ask whether the jump process produces a measurable forecast, a better risk model, or a more realistic cost/slippage stress.

### 3. Order books are stochastic queueing systems

For limit-order-book work, define:

- event types: limit order, market order, cancel;
- state variables: best bid/ask queues, depth, spread, order-flow imbalance;
- event clock: order event, trade time, wall-clock time, volume time;
- conditional target: next price move, queue depletion, fill before price move, adverse selection.

Do not use bar data to make claims about queue position.

### 4. Impact is state-dependent

A useful impact model must say which state variables matter:

- order flow imbalance;
- depth;
- spread;
- volatility;
- participation rate;
- liquidity regime;
- venue;
- time of day.

Volume alone is usually too crude.

### 5. Pathwise thinking helps with implementation

Path-dependent features, realized PnL, drawdowns, barriers, and trailing stops are functionals of the observed path. Treat them as non-anticipative functionals:

```text
feature_t = F(path up to t)
```

If `feature_t` depends on the future path, it is leakage.

### 6. Model risk is first-class

Every stochastic model must declare:

- fitted probability measure;
- calibration window;
- parameter stability;
- empirical diagnostics;
- failure modes;
- sensitivity to tails, jumps, and liquidity state;
- effect on the trading/risk decision.

## Quant Research Translation

When applying this lens, produce:

1. Empirical fact being modeled
2. Stochastic process candidate
3. Observable variables
4. Estimation/calibration method
5. Validation diagnostics
6. Trading or risk implication
7. Failure modes
8. Minimal experiment

## Standard Tests

- Tail index / extreme quantiles / QQ plot.
- Autocorrelation of returns and absolute returns.
- Jump detection or event-study around large moves.
- Volatility clustering and realized-volatility persistence.
- OFI regression against short-horizon mid-price changes.
- Depth-conditioned impact slope.
- Queue-depletion/fill probability by book state.
- Calibration stability across regimes.
- Cost/slippage stress using jump/liquidity scenarios.

## Use With Other Skills

- Use `prof/shreve` for martingale pricing, Brownian/SDE foundations, stochastic control, and no-arbitrage measure changes.
- Use `domain/market-microstructure` for execution, order-book features, queueing, and fill models.
- Use `domain/risk` for jump risk, liquidation, stress testing, and model risk.
- Use `workflow/backtest-review` when a stochastic model becomes a trading backtest.

