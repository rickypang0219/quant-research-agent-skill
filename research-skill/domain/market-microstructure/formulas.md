# Market Microstructure Formulas

This file is a formula map for limit order book research, market making, execution, and microstructure-aware backtesting.

## 0. Notation

Let time be indexed by event time `n` or clock time `t`.

At the best bid/ask:

- Best bid price: `b_t`
- Best ask price: `a_t`
- Best bid size: `B_t`
- Best ask size: `A_t`
- Mid-price: `m_t = (a_t + b_t) / 2`
- Spread: `s_t = a_t - b_t`
- Half-spread: `h_t = s_t / 2`
- Trade price: `p_i`
- Trade sign: `epsilon_i = +1` for buyer-initiated trade, `-1` for seller-initiated trade
- Signed trade size: `x_i = epsilon_i q_i`
- Tick size: `tau`

For Binance trade data:

```text
isBuyerMaker = true  => buyer was passive maker => seller was aggressor => epsilon = -1
isBuyerMaker = false => buyer was aggressor      => epsilon = +1
```

## 1. Core price and liquidity quantities

### Mid-price

```math
m_t = \frac{a_t + b_t}{2}
```

Mid-price is a convention, not necessarily fair value. It ignores queue imbalance, toxicity, and venue-specific flow.

### Spread

```math
s_t = a_t - b_t, \qquad h_t = \frac{s_t}{2}
```

In tick units:

```math
s^{tick}_t = \frac{a_t - b_t}{\tau}
```

### Depth at top of book

```math
D^{top}_t = A_t + B_t
```

Average best-depth:

```math
D_t = \frac{A_t + B_t}{2}
```

### Multi-level depth

For `L` levels:

```math
D^{bid}_{t,L} = \sum_{\ell=1}^{L} B_{t,\ell},
\qquad
D^{ask}_{t,L} = \sum_{\ell=1}^{L} A_{t,\ell}
```

## 2. Order book imbalance and microprice

### Top-level order book imbalance

```math
I_t = \frac{B_t - A_t}{B_t + A_t}
```

Interpretation:

- `I_t > 0`: more displayed size on bid than ask; upward short-horizon pressure is plausible.
- `I_t < 0`: more displayed size on ask than bid; downward short-horizon pressure is plausible.

### Microprice

A common microprice is:

```math
\mu_t = \frac{a_t B_t + b_t A_t}{A_t + B_t}
```

Equivalent skew form:

```math
\mu_t - m_t = \frac{s_t}{2}\frac{B_t - A_t}{A_t + B_t}
= h_t I_t
```

If bid depth is large relative to ask depth, the microprice moves toward the ask because the ask queue is easier to deplete.

### Multi-level weighted microprice

Let level weights be `w_l`, often decaying with distance from touch:

```math
\mu^{(L)}_t
= \frac{a_t \sum_{\ell=1}^{L} w_\ell B_{t,\ell}
       + b_t \sum_{\ell=1}^{L} w_\ell A_{t,\ell}}
       {\sum_{\ell=1}^{L} w_\ell (A_{t,\ell}+B_{t,\ell})}
```

Use this only after testing whether deeper levels improve out-of-sample prediction.

## 3. Order flow imbalance

### Event-level OFI

Let `P^B_n, q^B_n` be best bid price/size after event `n`, and `P^A_n, q^A_n` be best ask price/size after event `n`.

```math
e_n =
\mathbf{1}_{P^B_n \ge P^B_{n-1}} q^B_n
- \mathbf{1}_{P^B_n \le P^B_{n-1}} q^B_{n-1}
- \mathbf{1}_{P^A_n \le P^A_{n-1}} q^A_n
+ \mathbf{1}_{P^A_n \ge P^A_{n-1}} q^A_{n-1}
```

This captures the signed change in supply/demand at the best quotes.

### Bucketed OFI

For interval or event bucket `k`:

```math
OFI_k = \sum_{n \in k} e_n
```

### Cont-Kukanov-Stoikov impact regression

```math
\Delta m_k = \alpha_k + \beta_k OFI_k + \varepsilon_k
```

Empirical microstructure result:

```math
\beta_k \propto \frac{1}{D_k}
```

where `D_k` is average market depth. Depth, not just volume, controls impact.

### Normalized OFI

```math
NOFI_k = \frac{OFI_k}{D_k}
```

Use normalized OFI when comparing assets with different price levels and depths.

## 4. Trade-sign and order-flow features

### Signed volume

```math
SV_k = \sum_{i \in k} \epsilon_i q_i
```

### Signed notional

```math
SN_k = \sum_{i \in k} \epsilon_i q_i p_i
```

### Taker buy ratio

```math
TBR_k = \frac{\sum_{i\in k} \mathbf{1}_{\epsilon_i=+1} q_i}
{\sum_{i\in k} q_i}
```

### Taker imbalance

```math
TI_k = \frac{V^B_k - V^S_k}{V^B_k + V^S_k}
```

where `V^B` is buyer-initiated volume and `V^S` is seller-initiated volume.

### Trade-sign autocorrelation

```math
\rho(\ell) = Corr(\epsilon_i, \epsilon_{i-\ell})
```

Positive trade-sign autocorrelation is common because large hidden orders are split over time.

## 5. Effective spread, realized spread, and adverse selection

Let trade `i` occur at price `p_i`, sign `epsilon_i`, and prevailing mid `m_i`.

### Effective spread

```math
ES_i = 2\epsilon_i(p_i - m_i)
```

Half-spread version:

```math
EHS_i = \epsilon_i(p_i - m_i)
```

### Realized spread after horizon `h`

```math
RS_i(h) = 2\epsilon_i(p_i - m_{i+h})
```

### Price impact / adverse-selection component

```math
PI_i(h) = 2\epsilon_i(m_{i+h} - m_i)
```

Relationship:

```math
ES_i = RS_i(h) + PI_i(h)
```

Interpretation:

- Effective spread is what the liquidity taker pays immediately.
- Realized spread is what the liquidity provider keeps after the price moves.
- Price impact/adverse selection is the amount lost because the quote was picked off by informed or directional flow.

## 6. Roll spread estimator

If observed price changes have negative first-order autocovariance due to bid-ask bounce:

```math
Cov(\Delta p_t, \Delta p_{t-1}) < 0
```

then the Roll effective spread estimate is:

```math
S_{Roll} = 2\sqrt{-Cov(\Delta p_t, \Delta p_{t-1})}
```

Use only as a rough low-frequency proxy. It can fail when serial covariance is positive because of trends, inventory effects, or stale prices.

## 7. Kyle lambda and price impact

### Linear Kyle impact

```math
\Delta p_t = \lambda x_t + \varepsilon_t
```

where `x_t` is signed order flow.

OLS estimate:

```math
\hat{\lambda} = \frac{Cov(\Delta p_t, x_t)}{Var(x_t)}
```

High `lambda` means low liquidity: a unit of signed flow moves price more.

### Amihud illiquidity

```math
ILLIQ = \frac{1}{N}\sum_{t=1}^{N}\frac{|r_t|}{DollarVolume_t}
```

Useful for low-frequency liquidity screening, not a replacement for order-book impact.

### Square-root market impact law

Empirical meta-order impact is often modeled as:

```math
E[\Delta p] \approx Y\sigma \left(\frac{Q}{V}\right)^\delta,
\qquad \delta \approx \frac{1}{2}
```

where:

- `Q` = meta-order size,
- `V` = market volume over the execution horizon,
- `sigma` = volatility over the horizon,
- `Y` = asset/venue/regime coefficient.

This is an empirical regularity, not a universal law.

## 8. Market making: Avellaneda-Stoikov baseline

Assume mid-price:

```math
dS_t = \sigma dW_t
```

Market maker has inventory `q`, risk aversion `gamma`, terminal horizon `T`, and order-arrival intensity:

```math
\lambda(\delta) = A e^{-k\delta}
```

where `delta` is quote distance from mid.

### Reservation price

```math
r(s,q,t) = s - q\gamma\sigma^2(T-t)
```

Interpretation:

- Long inventory `q > 0`: reservation price below mid; quote more aggressively to sell.
- Short inventory `q < 0`: reservation price above mid; quote more aggressively to buy.

### Approximate total spread

```math
\delta^a + \delta^b
= \gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\left(1+\frac{\gamma}{k}\right)
```

### Quotes

```math
p^b_t = r_t - \frac{\delta^a_t + \delta^b_t}{2}
```

```math
p^a_t = r_t + \frac{\delta^a_t + \delta^b_t}{2}
```

Practical extensions:

```math
r^{practical}_t = m_t + \alpha_t - q_t\Gamma_t - fee\_skew_t - latency\_skew_t
```

where:

- `alpha_t` is short-horizon fair-value prediction,
- `Gamma_t` is inventory penalty per unit,
- `fee_skew_t` accounts for maker/taker economics,
- `latency_skew_t` accounts for stale-quote risk.

## 9. Fill probability and quote distance

Empirical fill model:

```math
P(fill \le \Delta t \mid \delta, Q^{ahead}, state)
= 1 - \exp(-\lambda(\delta, Q^{ahead}, state)\Delta t)
```

A simple parametric model:

```math
\lambda(\delta) = A e^{-k\delta}
```

A more realistic model includes:

```math
\lambda = f(\delta, Q^{ahead}, OFI, spread, volatility, trade\ intensity, cancel\ intensity)
```

## 10. Queue depletion model

Let `Q^b_t` and `Q^a_t` be best bid/ask queue sizes. A price move occurs when one side depletes:

```math
\tau_b = \inf\{t: Q^b_t = 0\},
\qquad
\tau_a = \inf\{t: Q^a_t = 0\}
```

```math
P(\Delta m > 0) = P(\tau_a < \tau_b)
```

Estimate this probability empirically using current queue sizes, recent market orders, cancellations, and limit-order arrivals.

## 11. Hawkes process for order arrivals

For event type `i`:

```math
\lambda_i(t)
= \mu_i + \sum_j \int_{0}^{t} \phi_{ij}(t-s)dN_j(s)
```

Use cases:

- market orders excite more market orders,
- cancellations cluster,
- buy and sell flows self-excite or cross-excite,
- intensity changes before volatility bursts.

## 12. VPIN / flow toxicity

Divide trades into equal-volume buckets of size `Vbar`. Let `V^B_j` and `V^S_j` be buy/sell volume in bucket `j`.

```math
VPIN_n = \frac{1}{n\bar{V}}\sum_{j=1}^{n}|V^B_j - V^S_j|
```

Interpretation: high VPIN means order flow is imbalanced in volume time, potentially increasing adverse-selection risk for liquidity providers.

Use with caution:

- trade classification errors matter,
- bucket size affects stability,
- toxicity is not the same as alpha,
- use only out-of-sample forward tests.

## 13. PIN model

Classical probability of informed trading:

```math
PIN = \frac{\alpha \mu}{\alpha \mu + \epsilon_b + \epsilon_s}
```

where:

- `alpha` = probability of an information event,
- `mu` = informed trade arrival rate,
- `epsilon_b`, `epsilon_s` = uninformed buy/sell arrival rates.

PIN is more structural but harder to estimate robustly at high frequency.

## 14. Hasbrouck trade informativeness

A simplified VAR representation:

```math
z_t = A_1 z_{t-1} + \cdots + A_p z_{t-p} + u_t
```

where `z_t` may include quote revisions and signed trades.

Trade information effect is the long-run impulse response of efficient price to a trade innovation:

```math
Impact = \sum_{h=0}^{\infty} \frac{\partial E[\Delta m_{t+h}]}{\partial u^{trade}_t}
```

Practical test: estimate whether trade shocks permanently move quotes or only temporarily bounce prices.

## 15. Cross-market price discovery

For the same asset traded on multiple venues, define price vector `p_t` and use a VECM:

```math
\Delta p_t = \alpha\beta^\top p_{t-1} + \sum_{i=1}^{k}\Gamma_i \Delta p_{t-i} + \varepsilon_t
```

Questions:

- Which venue incorporates information first?
- Does Binance lead Coinbase for BTC?
- Does futures lead spot?
- Does perp lead spot during high funding/liquidation events?

## 16. Almgren-Chriss execution model

Let total shares to liquidate be `X`, over `N` periods. Inventory path is `x_k`, trading rate is:

```math
v_k = \frac{x_{k-1}-x_k}{\tau}
```

Price dynamics with permanent impact:

```math
S_k = S_{k-1} + \sigma\sqrt{\tau}\xi_k - \tau g(v_k)
```

Execution price with temporary impact:

```math
\tilde{S}_k = S_{k-1} - h(v_k)
```

Objective:

```math
\min_{x_0,\ldots,x_N}
E[C] + \lambda Var(C)
```

where `C` is implementation shortfall. Larger `lambda` trades faster to reduce volatility risk but pays more impact.

## 17. Implementation shortfall

For a buy program:

```math
IS = \sum_{k} q_k p_k - Q p_0
```

For a sell program:

```math
IS = Qp_0 - \sum_k q_k p_k
```

Include fees:

```math
IS^{net} = IS + \sum_k fee_k |q_k|p_k
```

## 18. Discrete P&L with inventory and transaction costs

Let `Q_t` be asset quantity held after trading at time `t`, and `P_t` be close/mid/mark price.

Price-change P&L:

```math
PnL^{price}_t = Q_{t-1}(P_t - P_{t-1})
```

Transaction cost:

```math
TC_t = |Q_t - Q_{t-1}|P_t fee\_rate
```

Net P&L:

```math
PnL_t = Q_{t-1}(P_t - P_{t-1}) - |Q_t-Q_{t-1}|P_t fee\_rate
```

For USD target position `V_t`:

```math
Q^{target}_t = \frac{V_t}{P_t}
```

This formula is useful for crypto portfolio/stat-arb backtests when positions are specified in USDT notional.

## 19. Market-making P&L decomposition

For passive fills at bid/ask:

```math
PnL = SpreadCapture - AdverseSelection - InventoryRisk - Fees - LatencyLoss
```

A useful empirical approximation per fill `i`:

```math
SpreadCapture_i = \epsilon_i(p_i - m_i)
```

```math
AdverseSelection_i(h) = \epsilon_i(m_{i+h} - m_i)
```

```math
RealizedHalfSpread_i(h) = \epsilon_i(p_i - m_{i+h})
```

Positive realized half-spread means the passive order kept money after subsequent price movement.

## 20. Crypto perp additions

### Funding-adjusted expected return

For a perp position:

```math
r^{net}_{t,t+1} = r^{price}_{t,t+1} + r^{funding}_{t,t+1} - r^{fees}_{t,t+1}
```

### Basis

```math
Basis_t = \frac{P^{perp}_t - P^{spot}_t}{P^{spot}_t}
```

### Annualized funding approximation

If funding rate per interval is `f` and there are `K` funding intervals per year:

```math
FundingAPR \approx K f
```

### Liquidation-flow proxy

If liquidation feed exists:

```math
LiqImbalance_k = \frac{LiqBuyNotional_k - LiqSellNotional_k}{LiqBuyNotional_k + LiqSellNotional_k}
```

If no historical liquidation feed exists, do not pretend it is backtestable. Use it only for live monitoring or forward paper trading.

## 21. Feature normalization

Use dimensionless features when comparing assets:

```math
SpreadBps_t = 10^4\frac{a_t-b_t}{m_t}
```

```math
DepthBps_{L,t} = \frac{\sum_{\ell=1}^{L} notional_{\ell,t}}{ADV_t}
```

```math
ReturnVolScaled_t = \frac{r_t}{\hat{\sigma}_t}
```

```math
OFIScaled_t = \frac{OFI_t}{D_t}
```

## 22. Minimum viable microstructure feature vector

For a crypto medium-frequency strategy, start with:

```text
spread_bps
log_depth_bid_L1, log_depth_ask_L1
imbalance_L1
imbalance_L5
microprice_minus_mid_bps
OFI_1s, OFI_5s, OFI_30s
signed_volume_1s, signed_volume_5s, signed_volume_30s
taker_buy_ratio_1m
realized_vol_1m, realized_vol_5m
cancel_rate if event data exists
funding_rate and basis for perps
```

Then test whether each feature survives lagging, fees, and walk-forward validation.
