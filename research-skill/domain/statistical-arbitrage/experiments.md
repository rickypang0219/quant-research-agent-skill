# Statistical Arbitrage Experiments

This file turns the literature into practical experiments. Each experiment should produce code, diagnostics, plots, and a go/no-go decision. The goal is not to find a lucky backtest; the goal is to build research instincts about residual structure, cross-sectional structure, neutralization, costs, robustness, and crowding.

## Research Philosophy

A statistical arbitrage experiment should answer five questions:

1. **What is the relative mispricing?** Define the object: spread, residual, rank, factor-adjusted return, basis, funding dislocation, or cross-sectional anomaly.
2. **Why should it exist?** Identify the economic mechanism: slow information diffusion, inventory pressure, forced flows, leverage constraints, index/ETF linkage, funding/carry, liquidity provision, behavioral overreaction, or structural segmentation.
3. **Why should it decay?** Define the restoring force and expected horizon.
4. **Can it be harvested after costs?** Include fees, spread, slippage, borrow/funding, turnover, and capacity.
5. **Why will it survive research bias?** Use out-of-sample testing, multiple-testing controls, and stress tests.

---

## Experiment 1 — Distance-Based Pairs Trading

### Canonical source

Gatev, Goetzmann, and Rouwenhorst: pairs are selected by minimum distance between normalized historical price paths, then traded when they diverge.

### Hypothesis

Assets with historically similar normalized price paths are close substitutes. Temporary divergence between them may revert.

### Data

- Equities: daily adjusted close, volume, sector, market cap, borrow availability if shorting.
- Crypto: hourly or 4-hour close, volume, exchange status, funding if using perps.

### Formation

1. Choose universe after survivorship controls.
2. Normalize price paths over a formation window, e.g. 3-12 months.
3. Compute pairwise distance.
4. Select top `K` closest pairs per rebalance date.

### Trading

1. Compute spread `S_t = X_{t,A} - X_{t,B}`.
2. Enter when `|S_t - mean(S)| > k * std(S)`.
3. Long the underperformer, short the outperformer.
4. Exit when spread crosses mean or z-score falls below exit threshold.
5. Stop on extreme divergence or pair breakdown.

### Required diagnostics

- Pair distance distribution.
- Spread z-score examples.
- Holding-period distribution.
- PnL by pair.
- PnL by sector / coin category.
- Cost sensitivity.
- Number of active pairs over time.
- Correlation between pair returns and market/sector factors.

### Failure modes

- Pair relation was spurious.
- Pair breaks due to fundamentals/regime change.
- Profits are bid-ask bounce or stale price effects.
- Short borrow/funding destroys returns.
- Pair selection is overfit.

### Go/no-go

Go only if returns survive realistic costs, delayed execution, pair turnover, and out-of-sample formation/trading splits.

---

## Experiment 2 — Cointegration Basket Trading

### Hypothesis

A stationary linear combination of log prices implies a long-run equilibrium. Deviations from the equilibrium should mean-revert.

### Data

- Prefer assets with strong economic relation: dual listings, ETFs and constituents, futures/spot, similar equities, L1/L2 crypto competitors, liquid perps/spot pairs.
- Use adjusted prices for equities.
- Use consistent exchange and quote currency for crypto.

### Procedure

1. Pre-screen assets by sector/theme/liquidity.
2. Run rolling Engle-Granger or Johansen tests.
3. Estimate hedge vector `beta`.
4. Construct spread `S_t = beta^T log(P_t)`.
5. Test stationarity and half-life.
6. Trade spread z-score.

### Robustness checks

- Rolling beta stability.
- Rolling ADF p-values.
- Half-life stability.
- Spread variance stability.
- Walk-forward re-estimation.
- Out-of-sample spread stationarity.

### Failure modes

- Cointegration disappears out-of-sample.
- Test has low power or false positives.
- Hedge ratio changes faster than trading horizon.
- Costs exceed mean-reversion profit.

---

## Experiment 3 — Avellaneda-Lee PCA Residual Mean Reversion

### Canonical source

Avellaneda and Lee: use PCA or sector ETF regressions to remove common factors, then model idiosyncratic residuals as mean-reverting processes.

### Hypothesis

After removing market and dominant statistical factors, large idiosyncratic residual deviations partially mean-revert.

### Data

- Equities: broad liquid universe, daily or intraday bars, adjusted close, volume, sector, borrow/corporate action data.
- Crypto: top 30-200 liquid coins, 15m/1h/4h bars, volume, funding, exchange listing status.

### Pipeline

1. Build returns matrix `R` of shape `T x N`.
2. Use rolling PCA window `L_pca`.
3. Standardize returns within the PCA window.
4. Compute PCA loadings and first `K` factors.
5. Fit factor model over rolling window.
6. Compute residual returns.
7. Cumulate residuals.
8. Fit AR(1)/OU per asset.
9. Compute s-score.
10. Long low s-score assets, short high s-score assets.
11. Project weights to dollar-neutral and factor-neutral.
12. Charge turnover costs.

### Suggested starting parameters

For crypto hourly data:

- Universe: top 50 liquid coins.
- PCA window: 180 days.
- PCA update cadence: daily or every 4h depending on compute budget.
- Residual/OU window: 20-60 days.
- Signal cadence: hourly.
- Rebalance cadence: 4h or 6h.
- Entry: `|s| > 1.25` or cross-sectional top/bottom quantiles.
- Exit: `|s| < 0.25`.
- Half-life filter: e.g. 4h to 10 days.

### Required diagnostics

- Explained variance by PCA component.
- Factor loading stability.
- Residual autocorrelation.
- OU half-life distribution.
- S-score distribution.
- Raw vs projected factor exposure.
- PnL by asset.
- Turnover and cost attribution.
- Sharpe by subperiod.
- Performance during high BTC volatility regimes.

### Failure modes

- Residuals are not mean-reverting.
- PCA factors are unstable.
- The strategy shorts structural winners and longs structural losers.
- Projection removes too much signal.
- Rebalance too frequent relative to half-life.
- Costs dominate because residual signals are small.

---

## Experiment 4 — ETF / Fundamental Factor Residual Stat Arb

### Hypothesis

Explicit factors such as market, sector, size, value, momentum, volatility, liquidity, and funding explain common movement. Residuals after these factors may contain mean-reverting relative mispricing.

### Data

- Equities: market index ETF, sector ETFs, style factors, individual returns.
- Crypto: BTC, ETH, sector baskets, L1/L2/DeFi/meme categories, funding, market-cap, volume, volatility, exchange flows if available.

### Procedure

1. Define factor matrix `F_t`.
2. Regress each asset return on factors using rolling OLS or ridge.
3. Compute residual returns.
4. Cumulate residuals or model residual return directly.
5. Generate contrarian residual score.
6. Build factor-neutral portfolio.

### Required diagnostics

- Rolling R² by asset.
- Residual volatility vs raw volatility.
- Residual correlation matrix.
- Factor exposure after portfolio construction.
- Performance comparison: PCA residual vs explicit-factor residual.

### Failure modes

- Factor model is mis-specified.
- Factors are not tradeable or not known at signal time.
- Residuals contain hidden systematic risk.
- Ridge/OLS instability under collinearity.

---

## Experiment 5 — Short-Term Cross-Sectional Reversal

### Hypothesis

Very short-horizon overreaction, liquidity provision, and temporary imbalance create reversal among recent winners and losers.

### Data

- Equities: intraday or daily returns, spread, volume, volatility.
- Crypto: 5m/15m/1h returns, taker imbalance, volume, funding, spread if available.

### Features

- Last `k`-bar return.
- Volatility-adjusted return.
- Volume-adjusted return.
- Residual return after market/BTC factor.
- Liquidity filter.

### Signal

Contrarian cross-sectional score:

```text
score_i = - zscore_cross_section(residual_return_i over lookback k)
```

### Portfolio

- Long bottom recent performers.
- Short top recent performers.
- Dollar-neutral.
- BTC/market beta-neutral.
- Liquidity-weighted position caps.

### Required diagnostics

- IC by horizon.
- PnL by holding period.
- Cost sensitivity.
- Turnover.
- Performance by volatility regime.
- Performance excluding lowest-liquidity names.

### Failure modes

- Signal is bid-ask bounce.
- Spread and fees overwhelm edge.
- Momentum dominates reversal during trends.
- Liquidity filters accidentally introduce lookahead.

---

## Experiment 6 — Intermediate Momentum

### Canonical sources

Jegadeesh and Titman; Chan, Jegadeesh, and Lakonishok; Carhart; Asness, Moskowitz, and Pedersen.

### Hypothesis

Markets underreact to information over intermediate horizons. Recent winners may continue to outperform recent losers.

### Data

- Equities: daily/monthly returns, adjusted prices, delisting returns.
- Crypto: daily/4h returns, volume, market cap, exchange listings.

### Signal

Classical equity momentum:

```text
mom_i = cumulative_return_i over months 2-12, skipping most recent month
```

Crypto adaptation:

```text
mom_i = cumulative_return_i over 7-30 days, optionally skipping last 1 day or last few bars
```

### Portfolio

- Rank assets by momentum.
- Long top quantile, short bottom quantile.
- Neutralize market/BTC beta and possibly sector/category.
- Volatility scale.
- Rebalance at lower frequency than signal update.

### Required diagnostics

- Momentum decay curve by holding horizon.
- Crash risk and left-tail events.
- Exposure to market beta, volatility, liquidity, size.
- Turnover and capacity.
- Performance after neutralizing value/reversal signals.

### Failure modes

- Momentum crashes during sharp reversals.
- Signal becomes crowded.
- Low-liquidity winners dominate backtest.
- Crypto listing/survivorship bias.

---

## Experiment 7 — Value + Momentum Composite

### Canonical source

Asness, Moskowitz, and Pedersen document value and momentum premia across asset classes and emphasize their common factor structure and interaction.

### Hypothesis

Value and momentum are different but complementary relative-value signals. Combining them can improve diversification.

### Data

- Equities: book-to-market, earnings yield, profitability, investment, momentum.
- Crypto: harder; possible proxies include network activity, fee revenue, supply issuance, market-cap-to-transaction metrics, realized volatility, funding/carry, developer/activity metrics. Treat crypto value proxies as experimental.

### Signal

```text
composite_i = z(value_i) + z(momentum_i) - z(risk_penalty_i)
```

or use optimized combination based on validation IC.

### Portfolio

- Long high composite, short low composite.
- Neutralize market, sector, size, and liquidity.
- Turnover control.

### Required diagnostics

- IC of each component.
- Correlation between components.
- Incremental contribution of each component.
- Performance in growth/risk-on vs risk-off regimes.

### Failure modes

- Crypto value proxy is not economically meaningful.
- Value signal is slow and gets dominated by momentum.
- Composite overfits weights.

---

## Experiment 8 — Betting Against Beta / Low-Risk Relative Value

### Canonical source

Frazzini and Pedersen.

### Hypothesis

Leverage-constrained investors overpay for high-beta assets, causing low-beta assets to have better risk-adjusted returns.

### Data

- Rolling beta estimates to market factor.
- Volatility and correlation estimates.
- Liquidity and borrow costs.

### Signal

```text
beta_i = rolling_beta(asset_i, market)
score_i = -rank(beta_i)
```

Long low beta, short high beta, beta-scale legs to market neutrality.

### Portfolio

- Construct low-beta long leg and high-beta short leg.
- Scale each leg to equal beta contribution.
- Control leverage and funding cost.

### Required diagnostics

- Realized market beta of portfolio.
- Performance in funding stress regimes.
- Performance in sharp rebounds.
- Exposure to value, size, momentum, quality.

### Failure modes

- Beta estimates unstable.
- Low-beta leg becomes defensive crowding trade.
- Funding constraints cause forced deleveraging.
- High-beta shorts squeeze during rebounds.

---

## Experiment 9 — Formulaic Alpha Library

### Canonical source

Kakushadze's 101 Formulaic Alphas gives examples of short-horizon formulas combining ranks, correlations, returns, volume, VWAP, decay, and neutralization.

### Hypothesis

Many short-horizon equity alphas can be expressed as simple cross-sectional operators on price and volume data.

### Data

- OHLCV, VWAP if available.
- Corporate-action adjusted equities or clean crypto bars.
- Tradability filters.

### Procedure

1. Implement a small operator library: `rank`, `delay`, `delta`, `correlation`, `covariance`, `ts_rank`, `decay_linear`, `scale`, `signed_power`, `neutralize`.
2. Implement a subset of formulas.
3. Evaluate IC and PnL before optimizing.
4. Cluster alphas by correlation.
5. Combine only low-correlated, robust alphas.

### Required diagnostics

- IC mean/std/t-stat.
- Turnover.
- Alpha correlation matrix.
- Decay curve.
- Capacity by liquidity bucket.
- Stability by year/regime.

### Failure modes

- Operator leakage due to incorrect rolling windows.
- Overfitting by trying many formulas.
- Alphas are just liquidity/microcap effects.
- Costs and slippage dominate.

---

## Experiment 10 — Funding/Cash-and-Carry Statistical Arbitrage in Crypto

### Hypothesis

Perpetual funding, futures basis, and spot/perp dislocations reflect positioning pressure and may mean-revert or produce carry.

### Data

- Spot prices.
- Perp prices.
- Funding rates and predicted funding if available.
- Futures prices and expiries.
- Borrow rates if short spot.
- Fees, spread, margin requirements.

### Signals

Funding carry:

```text
score_i = expected_funding_i - borrow_cost_i - execution_cost_i
```

Basis convergence:

```text
basis_i = (future_price_i - spot_price_i) / spot_price_i
annualized_basis_i = basis_i * 365 / days_to_expiry
```

Relative funding:

```text
score_i = zscore_cross_section(funding_i) adjusted for volatility and liquidity
```

### Portfolio

- Long spot / short perp when funding is positive enough and basis/costs allow.
- Short spot / long perp only if borrow and shorting are possible.
- Cross-sectional long/short funding basket with market beta neutralization.

### Required diagnostics

- Funding PnL vs price PnL.
- Liquidation risk.
- Margin usage.
- Exchange concentration.
- Performance around volatility spikes.
- Capacity and slippage.

### Failure modes

- Funding is compensation for crash risk.
- Basis widens before converging.
- Exchange/borrow constraints prevent implementation.
- Funding rates change before trade execution.

---

## Experiment 11 — Residual Momentum vs Residual Reversal

### Hypothesis

Raw momentum/reversal may be mostly factor exposure. Residual momentum or residual reversal after factor neutralization may isolate a cleaner anomaly.

### Procedure

1. Fit factor model using market, sector, style, or PCA factors.
2. Compute residual returns.
3. Build residual momentum over lookback `L`.
4. Build residual reversal over shorter lookback `S`.
5. Compare raw vs residual signals.

### Diagnostics

- Raw signal IC vs residual signal IC.
- Factor exposure before/after.
- Performance by factor regime.
- Correlation with standard momentum.
- Incremental alpha regression.

### Failure modes

- Residualization removes real signal.
- Residual model is unstable.
- Remaining residual is noise.

---

## Experiment 12 — Alpha Combination and Ensemble Construction

### Hypothesis

A diversified alpha book can be more robust than one signal if signals are low-correlated and independently motivated.

### Data

- Signal matrix `S_{t,i,k}` for alpha `k`.
- Return outcomes.
- Cost and turnover per alpha.

### Procedure

1. Standardize each alpha cross-sectionally.
2. Compute IC and turnover.
3. Remove weak or unstable alphas.
4. Cluster by alpha correlation.
5. Combine using equal weights, IC weights, or risk-adjusted weights.
6. Penalize turnover and crowding.

### Simple combination

```text
combined_score_i = sum_k weight_k * standardized_alpha_{i,k}
```

### Diagnostics

- Alpha correlation heatmap.
- Marginal contribution to portfolio Sharpe.
- Contribution to turnover.
- Performance by regime.
- Stability of alpha weights.

### Failure modes

- Ensemble overfits validation period.
- Alphas are all variants of the same effect.
- Alpha weights chase recent performance.

---

## Experiment 13 — Crowding and Quant Meltdown Stress Test

### Canonical source

Khandani and Lo analyze the August 2007 quant deleveraging episode and the risk that market-neutral portfolios can become connected through common positions and forced liquidation.

### Hypothesis

A market-neutral stat-arb book can suffer large losses when similar books delever simultaneously, especially in high-crowding names.

### Procedure

1. Estimate common factor exposures.
2. Estimate position crowding proxies: short interest, borrow cost, liquidity, ETF ownership, open interest, funding extremes, abnormal volume.
3. Stress unwind: assume long leg down and short leg up simultaneously.
4. Simulate increased costs and reduced liquidity.
5. Simulate forced gross reduction.

### Diagnostics

- Portfolio loss under long-leg selloff / short-leg squeeze.
- Liquidity days-to-exit.
- Gross/net exposure under stress.
- Concentration by crowded names.
- Correlation spike scenarios.

### Failure modes

- Historical backtest does not contain crowding crisis.
- Borrow/funding costs jump exactly when alpha is negative.
- Vol targeting forces selling into drawdown.

---

## Experiment 14 — Robustness and Data-Snooping Audit

### Canonical sources

Lo and MacKinlay; Bailey and López de Prado; Hou, Xue, and Zhang.

### Goal

Determine whether a discovered edge is likely real or a statistical artifact.

### Audit checklist

1. Count number of tested hypotheses and parameter variants.
2. Keep a research log of failed ideas.
3. Use train/validation/test splits.
4. Use walk-forward re-training.
5. Purge overlapping labels if using ML or overlapping horizons.
6. Compute cost sensitivity.
7. Compute performance by year, volatility regime, liquidity bucket, and universe subset.
8. Compute Deflated Sharpe or multiple-testing-aware statistic.
9. Run placebo tests: shuffled labels, lagged wrong-way signals, random universe, random rebalance dates.
10. Check if performance is concentrated in microcaps/illiquid names.

### Go/no-go

Reject the strategy if:

- test performance collapses out-of-sample,
- Sharpe disappears with small cost increase,
- all PnL comes from one asset or month,
- signal only works in illiquid names,
- exposure to a known factor explains returns,
- small timing changes destroy PnL,
- after multiple-testing adjustment the result is insignificant.

---

## Experiment 15 — Crypto PCA Residual Research Plan

This is a focused plan for a crypto universe, matching a realistic medium-frequency stat-arb setup.

### Universe

- Start with top 50-100 coins by robust liquidity, not just market cap.
- Exclude stablecoins unless explicitly modeling basis/carry.
- Require minimum history, volume, and exchange reliability.
- Track delistings and symbol migrations.

### Data frequency

Start with 1h bars. Then compare 15m and 4h.

Rationale:

- 15m captures more opportunities but has more noise and costs.
- 1h is often a good first research compromise.
- 4h may improve signal stability and reduce turnover.

### Milestone 1 — Data integrity

Deliverables:

- Clean `T x N` price matrix.
- Missing data report.
- Volume/liquidity filters.
- Return distribution plots.
- Correlation heatmap.

Go/no-go:

- No lookahead filling.
- No dead assets silently dropped from the past.

### Milestone 2 — Factor structure

Deliverables:

- Rolling PCA explained variance.
- First PC loadings.
- BTC/ETH correlation with PCs.
- Sector/category clustering if labels exist.

Go/no-go:

- PCA components are interpretable enough or at least stable enough to use as statistical factors.

### Milestone 3 — Residual behavior

Deliverables:

- Residual autocorrelation by asset.
- AR(1) coefficient and half-life by asset.
- S-score distribution.
- Residual volatility vs raw volatility.

Go/no-go:

- A meaningful subset has finite, tradeable half-life and stable residual variance.

### Milestone 4 — Signal-only test

Deliverables:

- Rank IC of s-score vs future residual returns.
- Decay curve from 1h to 72h.
- Long/short quantile return without costs.
- Same with conservative costs.

Go/no-go:

- Signal direction must make sense before portfolio optimization.

### Milestone 5 — Portfolio construction

Deliverables:

- Dollar-neutral weights.
- BTC/market beta-neutral weights.
- PCA factor-neutral weights.
- Gross and net exposure plots.
- Turnover plot.

Go/no-go:

- Neutralization does not destroy all signal.
- Factor exposure after projection is near zero.

### Milestone 6 — Backtest

Deliverables:

- Quantity-based PnL.
- Transaction costs.
- Funding costs if perps.
- Equity curve.
- Drawdown.
- Sharpe, Sortino, Calmar.
- PnL attribution: price, cost, funding.

Go/no-go:

- Positive after costs with stable subperiods.

### Milestone 7 — Stress and live simulation

Deliverables:

- Slippage sensitivity.
- Fee sensitivity.
- Delayed execution test.
- Volatility regime test.
- BTC crash day behavior.
- Paper trading plan.

Go/no-go:

- Strategy survives realistic delays and moderate cost increases.

---

## Backtest Standards

Every experiment should define:

1. timestamp convention,
2. signal timestamp,
3. execution timestamp,
4. holding-period convention,
5. universe membership timing,
6. transaction-cost model,
7. borrow/funding model,
8. missing-data policy,
9. neutralization timing,
10. risk limit logic.

### Minimal backtest timing rule

```text
At time t:
  observe data up to and including t
  compute signal_t
  compute target weights_t
At time t+1:
  trade at open/next executable price
  hold position through t+1 return
  charge costs on quantity change
```

Never compute signal using close at `t` and assume fill at the same close unless the strategy explicitly uses market-on-close mechanics and the data supports that.

---

## Plots to Produce for Almost Every Experiment

1. Equity curve.
2. Drawdown curve.
3. Rolling Sharpe.
4. Monthly/weekly return heatmap.
5. Turnover over time.
6. Gross and net exposure.
7. Factor exposures over time.
8. Cost attribution.
9. Long-leg and short-leg PnL separately.
10. Signal IC decay curve.
11. Performance by volatility/liquidity regime.
12. Per-asset contribution to PnL.

---

## Failure Pattern Library

### Looks good before costs, dies after costs

Likely too high turnover or too short horizon. Increase horizon, lower rebalance frequency, add no-trade bands, improve execution model.

### Works only in small illiquid names

Likely microcap/liquidity premium or stale price effect. Add liquidity filters and realistic slippage.

### Works only in one year

Likely regime-specific. Either build explicit regime detector or reject.

### Strong raw returns, no residual returns

Signal is factor exposure, not alpha. Decide whether you want factor premium or market-neutral stat arb.

### Neutralization makes weights explode

Constraints are too strong for the universe, factors are collinear, or raw signal lies mostly in the constrained subspace. Use ridge, soft penalties, or reduce factor set.

### Half-life too long

Mean reversion is too slow relative to capital/costs. Drop or trade at lower frequency with lower turnover.

### Half-life too short

May be bid-ask bounce or microstructure noise. Need execution model and spread data.

---

## Suggested Project Structure

```text
stat_arb_project/
├── README.md
├── pyproject.toml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_data_quality.ipynb
│   ├── 02_factor_structure.ipynb
│   ├── 03_signal_research.ipynb
│   └── 04_backtest_diagnostics.ipynb
├── src/
│   └── stat_arb/
│       ├── data.py
│       ├── returns.py
│       ├── factors.py
│       ├── pca.py
│       ├── residuals.py
│       ├── signals.py
│       ├── neutralize.py
│       ├── portfolio.py
│       ├── costs.py
│       ├── backtest.py
│       ├── metrics.py
│       └── plots.py
├── tests/
│   ├── test_alignment.py
│   ├── test_neutralize.py
│   ├── test_pnl.py
│   └── test_costs.py
└── reports/
    ├── figures/
    └── experiment_logs/
```

---

## Source Registry

- Avellaneda and Lee — PCA/ETF residual statistical arbitrage: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1153505
- Gatev, Goetzmann, and Rouwenhorst — distance pairs trading: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=141615
- Jegadeesh and Titman — intermediate momentum: https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html
- Chan, Jegadeesh, and Lakonishok — momentum and underreaction: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=225438
- Fama and French — common risk factors: https://www.sciencedirect.com/science/article/abs/pii/0304405X93900235
- Fama and French — five-factor model: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2287202
- Asness, Moskowitz, and Pedersen — value and momentum across markets: https://www.aqr.com/Insights/Research/Journal-Article/Value-and-Momentum-Everywhere
- Frazzini and Pedersen — betting against beta: https://www.aqr.com/Insights/Research/Journal-Article/Betting-Against-Beta
- Kakushadze — formulaic alphas: https://arxiv.org/abs/1601.00991
- Khandani and Lo — quant meltdown/crowding: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1015987
- Lo and MacKinlay — data snooping: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=227465
- Bailey and López de Prado — Deflated Sharpe: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- Hou, Xue, and Zhang — anomaly replication: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2961979
