# Statistical Arbitrage Formulas

This file contains formulas for statistical arbitrage research. It emphasizes explicit dimensions, neutralization, residual modeling, PnL, costs, and validation.

## 0. Notation

| Symbol | Meaning | Shape |
|---|---|---|
| `t = 1,...,T` | time index | scalar |
| `i = 1,...,N` | asset index | scalar |
| `P_{t,i}` | price of asset `i` at time `t` | scalar |
| `r_{t,i}` | return of asset `i` at time `t` | scalar |
| `r_t` | cross-section of returns at time `t` | `N x 1` |
| `R` | return matrix | `T x N` |
| `F_t` | factor returns at time `t` | `K x 1` |
| `B` | factor exposure matrix | `N x K` |
| `w_t` | portfolio weights / dollar weights | `N x 1` |
| `C` | constraint matrix | `N x M` |
| `q_t` | asset quantities | `N x 1` |
| `V_{t,i}` | target notional position in asset `i` | scalar |
| `s_{t,i}` | score or s-score | scalar |

Use column vectors by default. A portfolio return is usually `w_t^T r_{t+1}` if `w_t` is fixed at the close of `t` and earns the next-period return.

---

## 1. Returns

### Simple return

```math
r_{t,i} = \frac{P_{t,i}}{P_{t-1,i}} - 1
```

### Log return

```math
x_{t,i} = \log P_{t,i} - \log P_{t-1,i}
```

For high-frequency crypto and stat-arb factor work, log returns are usually easier for additive modeling, but PnL should be computed from quantities and price changes.

### Excess return

```math
r^e_{t,i} = r_{t,i} - r^f_t
```

In crypto, the equivalent may involve funding, borrow, stablecoin yield, or no explicit risk-free term depending on the venue and strategy.

---

## 2. Cross-Sectional Normalization

At each time `t`, for signal `x_{t,i}`:

### Cross-sectional mean and standard deviation

```math
\bar{x}_t = \frac{1}{N_t}\sum_{i \in \mathcal{U}_t} x_{t,i}
```

```math
\sigma_{x,t} = \sqrt{\frac{1}{N_t-1}\sum_{i \in \mathcal{U}_t}(x_{t,i}-\bar{x}_t)^2}
```

### Cross-sectional z-score

```math
z_{t,i} = \frac{x_{t,i} - \bar{x}_t}{\sigma_{x,t}}
```

### Winsorized z-score

```math
z^{clip}_{t,i} = \max(-z_{max}, \min(z_{t,i}, z_{max}))
```

### Rank transform

```math
u_{t,i} = \frac{\operatorname{rank}_t(x_{t,i}) - 0.5}{N_t}
```

```math
s_{t,i} = 2\nu_{t,i} - 1 \in (-1,1)
```

Ranking is often more robust than raw z-scores when distributions are heavy-tailed or unstable.

---

## 3. Time-Series Normalization

For each asset `i`, using a rolling window `L`:

```math
\mu_{t,i}^{(L)} = \frac{1}{L}\sum_{u=t-L+1}^{t} x_{u,i}
```

```math
\sigma_{t,i}^{(L)} = \sqrt{\frac{1}{L-1}\sum_{u=t-L+1}^{t}(x_{u,i}-\mu_{t,i}^{(L)})^2}
```

```math
z_{t,i}^{TS} = \frac{x_{t,i}-\mu_{t,i}^{(L)}}{\sigma_{t,i}^{(L)}}
```

Use time-series z-scores for asset-specific deviations. Use cross-sectional z-scores for relative ranking across assets at the same time.

---

## 4. Pairs Trading: Distance Method

Based on the Gatev-Goetzmann-Rouwenhorst style idea.

### Normalize price paths over formation window

For asset `i`:

```math
\tilde{P}_{t,i} = \frac{P_{t,i}}{P_{t_0,i}}
```

or use z-scored cumulative return paths:

```math
X_{t,i} = \frac{\log P_{t,i} - \log P_{t_0,i} - \mu_i}{\sigma_i}
```

### Pair distance

```math
D_{ij} = \sum_{t \in \mathcal{F}} (X_{t,i} - X_{t,j})^2
```

Choose pairs with small `D_{ij}` during the formation window.

### Spread

```math
S_t = X_{t,i} - X_{t,j}
```

### Trading rule

Open when:

```math
|S_t - \bar{S}| > k\sigma_S
```

Close when:

```math
S_t \rightarrow \bar{S}
```

Hard stop when:

```math
|S_t - \bar{S}| > k_{stop}\sigma_S
```

Caution: distance closeness is not the same as cointegration. A pair can be close historically and still not have a stable restoring relationship.

---

## 5. Pairs Trading: Regression Hedge Ratio

For log prices `y_t = log P_{t,A}` and `x_t = log P_{t,B}`:

```math
y_t = \alpha + \beta x_t + \epsilon_t
```

The spread is:

```math
S_t = y_t - \hat{\alpha} - \hat{\beta}x_t
```

A dollar-neutral approximation can be different from a beta-hedged spread. If one unit of `A` is long, hedge with `\hat{\beta}` units of `B` in log-price regression terms, but practical sizing must convert this to dollar exposure and exchange constraints.

---

## 6. Cointegration Spread

A vector of log prices `p_t in R^N` is cointegrated if there exists a nonzero vector `\beta` such that:

```math
S_t = \beta^T p_t
```

is stationary even though the individual log price series are non-stationary.

### Error correction model intuition

```math
\Delta p_t = \alpha \beta^T p_{t-1} + \sum_{l=1}^{q}\Gamma_l \Delta p_{t-l} + \epsilon_t
```

`\beta^T p_{t-1}` is the disequilibrium term. `\alpha` measures how assets adjust back toward the long-run relation.

Caution: cointegration can be unstable across regimes; rolling tests and out-of-sample decay are mandatory.

---

## 7. Factor Model

### Time-series factor model for asset `i`

```math
r_{t,i} = \alpha_i + \beta_i^T F_t + \epsilon_{t,i}
```

where `F_t` is `K x 1`.

OLS estimates:

```math
\hat{\beta}_i = (F^T F)^{-1}F^T r_i
```

where `F` is `T x K`, `r_i` is `T x 1`.

### Matrix form

```math
R = \mathbf{1}\alpha^T + F B^T + E
```

where:

- `R`: `T x N`,
- `F`: `T x K`,
- `B`: `N x K`,
- `E`: `T x N`.

### Residual return

```math
\hat{\epsilon}_{t,i} = r_{t,i} - \hat{\alpha}_i - \hat{\beta}_i^T F_t
```

The residual is the candidate mean-reverting object in residual stat arb.

---

## 8. PCA Factor Model

Given standardized return window `Y` of shape `L x N`:

```math
Y_{u,i} = \frac{R_{u,i} - \bar{R}_i}{\sigma_i}
```

Correlation matrix:

```math
\Sigma = \frac{1}{L-1}Y^T Y
```

Eigen-decomposition:

```math
\Sigma = V\Lambda V^T
```

Choose first `K` eigenvectors `V_K`. A common PCA factor return estimate is:

```math
F_t = V_K^T r_t
```

or, if using standardized returns:

```math
F_t = V_K^T y_t
```

where `y_t` is standardized by the same rolling means and volatilities used in fitting PCA.

### Explained variance ratio

```math
EVR_K = \frac{\sum_{k=1}^{K}\lambda_k}{\sum_{j=1}^{N}\lambda_j}
```

Choose `K` by a fixed count, explained variance threshold, cross-validation, or stability. Do not choose `K` by maximizing backtest Sharpe without multiple-testing correction.

---

## 9. Residual Price / Cumulative Residual

If residual returns are `\epsilon_{t,i}`, define cumulative residual:

```math
X_{t,i} = \sum_{u=t_0}^{t}\epsilon_{u,i}
```

Some Avellaneda-Lee-style implementations fit mean-reversion on cumulative residuals rather than raw residual returns.

---

## 10. AR(1) / OU Model for Residuals

### AR(1)

```math
X_{t+1} = a + bX_t + \eta_{t+1}
```

Mean:

```math
m = \frac{a}{1-b}
```

Innovation variance:

```math
\sigma_\eta^2 = \operatorname{Var}(\eta_t)
```

Equilibrium variance:

```math
\sigma_{eq}^2 = \frac{\sigma_\eta^2}{1-b^2}
```

S-score:

```math
s_t = \frac{X_t - m}{\sigma_{eq}}
```

Mean reversion speed under OU mapping with bar interval `\Delta t`:

```math
b = e^{-\kappa \Delta t}
```

```math
\kappa = -\frac{\log b}{\Delta t}
```

Half-life:

```math
h_{1/2} = \frac{\log 2}{\kappa}
```

If `b <= 0` or `b >= 1`, the OU interpretation is unstable or invalid for simple mean reversion.

---

## 11. Signal Rules for Residual Mean Reversion

For residual score `s_{t,i}`:

### Contrarian entry

```math
\text{long if } s_{t,i} < -s_{entry}
```

```math
\text{short if } s_{t,i} > s_{entry}
```

### Exit

```math
\text{exit if } |s_{t,i}| < s_{exit}
```

### Hard stop

```math
\text{stop if } |s_{t,i}| > s_{stop}
```

### Half-life filter

Trade only if:

```math
h_{min} \le h_{1/2,i} \le h_{max}
```

Rationale: too fast may be microstructure noise; too slow may not revert inside the holding period.

---

## 12. Cross-Sectional Long/Short Portfolio from Scores

Given score vector `s_t` where higher means more attractive:

### Demean

```math
\tilde{s}_t = s_t - \bar{s}_t\mathbf{1}
```

### Volatility scaling

```math
u_{t,i} = \frac{\tilde{s}_{t,i}}{\hat{\sigma}_{t,i}}
```

### Raw weights

```math
w^{raw}_{t,i} = \frac{\nu_{t,i}}{\sum_j |\nu_{t,j}|}
```

This gives unit gross exposure:

```math
\sum_i |w^{raw}_{t,i}| = 1
```

and approximately dollar-neutral if the signal is demeaned.

---

## 13. Dollar Neutrality

Dollar-neutral constraint:

```math
\mathbf{1}^T w = 0
```

Project raw weights onto the dollar-neutral hyperplane:

```math
w^{DN} = w^{raw} - \frac{\mathbf{1}^T w^{raw}}{\mathbf{1}^T\mathbf{1}}\mathbf{1}
```

Renormalize gross:

```math
w = \frac{G \cdot w^{DN}}{\sum_i |w^{DN}_i|}
```

where `G` is target gross exposure.

---

## 14. Factor Neutrality

Given exposure matrix `B` of shape `N x K`, factor neutrality means:

```math
B^T w = 0
```

Dollar plus factor constraints:

```math
C^T w = 0
```

where:

```math
C = [\mathbf{1}, B]
```

and `C` is `N x (K+1)`.

### Euclidean projection

Find closest neutral weights:

```math
\min_w \|w - w^{raw}\|_2^2 \quad \text{s.t.}\quad C^T w = 0
```

Solution:

```math
w^{proj} = w^{raw} - C(C^T C)^{-1}C^T w^{raw}
```

For numerical stability, use pseudo-inverse or ridge:

```math
w^{proj} = w^{raw} - C(C^T C + \lambda I)^{-1}C^T w^{raw}
```

Then renormalize gross.

### Weighted projection

If assets have different risks, use diagonal risk matrix `D`:

```math
\min_w (w-w^{raw})^T D (w-w^{raw}) \quad \text{s.t.}\quad C^T w = 0
```

Solution:

```math
w = w^{raw} - D^{-1}C(C^T D^{-1}C)^{-1}C^T w^{raw}
```

---

## 15. Constrained Optimization Portfolio

A practical portfolio can be formed as:

```math
\max_w \quad \mu^T w - \lambda_r w^T\Sigma w - \lambda_t\|w - w_{prev}\|_1
```

subject to:

```math
\mathbf{1}^T w = 0
```

```math
B^T w = 0
```

```math
\sum_i |w_i| \le G
```

```math
|w_i| \le w_{max,i}
```

```math
\sum_{i \in sector\;g} w_i = 0 \quad \text{optional}
```

where:

- `\mu` is expected return forecast,
- `\Sigma` is covariance matrix,
- `\lambda_r` controls risk aversion,
- `\lambda_t` controls turnover penalty,
- `G` is gross exposure limit.

---

## 16. Sign-Preserving Soft Neutralization

Hard sign preservation can be infeasible. A soft version:

```math
\min_w \quad \|w - w^{raw}\|_2^2 + \lambda_c\|C^T w\|_2^2 + \lambda_s\sum_i \max(0, -\operatorname{sign}(w^{raw}_i)w_i)^2
```

subject to:

```math
\sum_i |w_i| \le G
```

and box constraints. This penalizes factor exposure and sign flips without making the problem infeasible.

---

## 17. PnL with Quantities and Transaction Costs

For asset `i`:

Target notional:

```math
V_{t,i} = AUM_t \cdot w_{t,i}
```

Target quantity:

```math
q^{target}_{t,i} = \frac{V_{t,i}}{P_{t,i}}
```

Delta quantity:

```math
\Delta q_{t,i} = q^{target}_{t,i} - q_{t-1,i}
```

Price-change PnL:

```math
PnL^{price}_{t+1,i} = q_{t,i}(P_{t+1,i} - P_{t,i})
```

Transaction cost:

```math
TC_{t,i} = |\Delta q_{t,i}|P_{t,i}c_i
```

where `c_i` is proportional cost, e.g. taker fee + slippage.

Total PnL:

```math
PnL_{t+1} = \sum_i q_{t,i}(P_{t+1,i}-P_{t,i}) - \sum_i |\Delta q_{t,i}|P_{t,i}c_i - Borrow_t - Funding_t
```

This is safer than using `w_t * returns` when positions, prices, costs, and contract specifications matter.

---

## 18. Turnover

One-way turnover:

```math
TO_t = \frac{1}{2}\sum_i |w_{t,i} - w_{t-1,i}|
```

or notional turnover:

```math
TO^{notional}_t = \sum_i |\Delta q_{t,i}|P_{t,i}
```

Annualized turnover depends on rebalance frequency.

---

## 19. Risk Metrics

### Mean return

```math
\bar{r} = \frac{1}{T}\sum_{t=1}^{T} r_t
```

### Volatility

```math
\hat{\sigma} = \sqrt{\frac{1}{T-1}\sum_{t=1}^{T}(r_t-\bar{r})^2}
```

### Annualized Sharpe

```math
SR = \frac{\bar{r}}{\hat{\sigma}}\sqrt{A}
```

where `A` is periods per year, e.g. `365` for daily crypto, `252` for daily equities.

### Max drawdown

```math
DD_t = \frac{Equity_t}{\max_{u\le t}Equity_u} - 1
```

```math
MDD = \min_t DD_t
```

### Hit rate

```math
HR = \frac{\#\{t: PnL_t > 0\}}{T}
```

Hit rate is not enough. A low-hit strategy can work with large winners; a high-hit strategy can fail with fat-tail losses.

---

## 20. Information Coefficient

For forecast `s_{t,i}` and future return `r_{t+1,i}`:

```math
IC_t = \operatorname{corr}_i(s_{t,i}, r_{t+1,i})
```

Rank IC:

```math
RankIC_t = \operatorname{corr}_i(\operatorname{rank}(s_{t,i}), \operatorname{rank}(r_{t+1,i}))
```

Average IC:

```math
\overline{IC} = \frac{1}{T}\sum_t IC_t
```

IC information ratio:

```math
IR_{IC} = \frac{\overline{IC}}{\operatorname{std}(IC_t)}\sqrt{A}
```

---

## 21. Autocorrelation-Adjusted Sharpe

If returns are autocorrelated, naive annualized Sharpe can be inflated.

Let `\rho_k` be autocorrelation at lag `k`. An approximate adjustment over horizon `q`:

```math
SR(q) \approx \frac{q\bar{r}}{\sqrt{q\sigma^2 + 2\sigma^2\sum_{k=1}^{q-1}(q-k)\rho_k}}
```

Use Newey-West or block bootstrap for more reliable inference.

---

## 22. Probabilistic and Deflated Sharpe Intuition

### Probabilistic Sharpe Ratio intuition

For benchmark Sharpe `SR^*`, estimate:

```math
PSR = P(\widehat{SR} > SR^*)
```

adjusting for sample length and non-normality.

### Deflated Sharpe Ratio intuition

Deflated Sharpe asks whether the observed Sharpe is still significant after accounting for:

- multiple trials,
- non-normal returns,
- selection bias,
- short sample length.

Use it when many strategy variants or parameters were tried.

---

## 23. Multiple Testing

If testing `M` independent hypotheses with significance `\alpha`, Bonferroni threshold:

```math
p_i < \frac{\alpha}{M}
```

For correlated strategies, this is conservative but useful as a warning. In practice, also use:

- walk-forward testing,
- combinatorial purged cross-validation,
- White's Reality Check / SPA-style procedures,
- Deflated Sharpe,
- holdout sets untouched by research iteration.

---

## 24. Capacity and Market Impact

Simple linear cost model:

```math
Cost(Q) = c_0 |Q| + c_1 Q^2
```

Square-root market impact model:

```math
I(Q) = Y\sigma \sqrt{\frac{|Q|}{ADV}}
```

Expected net alpha per asset:

```math
NetAlpha_i(Q) = Forecast_i \cdot Q - Cost_i(Q)
```

Capacity is where marginal expected alpha equals marginal cost/risk:

```math
\frac{d}{dQ}Forecast_i Q = \frac{d}{dQ}Cost_i(Q)
```

---

## 25. Volatility Targeting

Given raw portfolio return volatility estimate `\hat{\sigma}_t` and target volatility `\sigma^*`:

```math
L_t = \min\left(L_{max}, \frac{\sigma^*}{\hat{\sigma}_t}\right)
```

Scaled weights:

```math
w^{scaled}_t = L_t w_t
```

Vol targeting reduces exposure in high vol regimes but can force deleveraging during crowded selloffs.

---

## 26. Crypto-Specific Terms

### Funding PnL for perpetuals

If position notional is `V_{t,i}` and funding rate per interval is `f_{t,i}`:

```math
FundingPnL_{t,i} = - V_{t,i} f_{t,i}
```

Sign conventions differ by venue. Always check whether longs pay shorts or shorts pay longs.

### Basis

```math
Basis_t = \frac{F_t - S_t}{S_t}
```

Annualized basis:

```math
Basis^{ann}_t = \frac{F_t - S_t}{S_t}\cdot\frac{365}{DTE}
```

### Spot-perp carry signal

```math
CarrySignal_{t,i} = FundingRate_{t,i} - BorrowCost_{t,i} - ExpectedBasisDecay_{t,i}
```

---

## 27. Diagnostics Checklist

For every formula implementation, verify:

1. no future data used in rolling means, PCA, regressions, vol estimates, or ranks;
2. rebalance timing is explicit: signal at `t`, trade at `t+1` open/close, earn return `t+1`;
3. weights sum to intended net and gross exposure;
4. factor exposures after projection are near zero;
5. quantities match exchange tick/lot/min-notional rules;
6. costs are charged on turnover, not position;
7. delisted/missing assets are handled conservatively;
8. performance is stable by subperiod and not concentrated in one regime.
