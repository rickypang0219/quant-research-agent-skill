# Andrew W. Lo Skill Examples

Practical examples for applying Andrew W. Lo-style thinking to strategy research, risk management, Adaptive Markets diagnosis, AI in finance, and market-sense training.

---

## Example 1 — Adaptive Markets diagnosis for a crypto funding-rate strategy

### Observation

A coin has very positive perpetual funding for several days, strong spot momentum, rising open interest, and increasing social attention.

### Naive interpretation

“Funding is high, so short the perp.”

### Lo-style interpretation

High funding is not automatically a short signal. It is an ecological state variable. It may indicate:

1. genuine information diffusion,
2. retail trend chasing,
3. leveraged long crowding,
4. basis arbitrage demand,
5. exchange-specific margin constraints,
6. structural shortage of short capital,
7. or a coming liquidation cascade.

### Adaptive diagnosis

```markdown
Environment:
- Market: crypto perpetual swaps
- Horizon: 1h to multi-day
- Friction: funding, taker fees, spread, depth, liquidation rules

Agent populations:
- Retail momentum longs
- Market makers
- Funding arbitrage desks
- Directional funds
- Liquidation engine participants

Dominant heuristic:
- Extrapolate recent price trend
- Chase breakout
- Use high funding as confirmation of bullish demand

Potential maladaptation:
- Crowd assumes trend continues; leverage grows; liquidation convexity rises

Evidence to collect:
- Open interest percentile
- Funding percentile
- Long/short taker imbalance
- Spot-perp basis
- Liquidation heatmap
- Order-book depth
- Cross-exchange spread
- BTC beta
```

### Testable strategy hypotheses

1. **Continuation hypothesis:** High funding plus rising spot volume predicts continuation when liquidity remains strong.
2. **Reversal hypothesis:** Extreme funding plus falling order-book depth predicts downside liquidation risk.
3. **No-trade hypothesis:** Funding is high because shorting demand is structurally constrained; shorting is negative carry and dangerous.

### Feature set

```text
funding_z = zscore(funding_rate, 90d)
oi_z = zscore(open_interest, 90d)
spot_volume_z = zscore(spot_volume, 90d)
depth_z = zscore(orderbook_depth_1pct, 90d)
taker_buy_ratio = taker_buy_volume / total_taker_volume
basis = perp_mid / spot_mid - 1
liq_pressure = estimated_liquidations / rolling_volume
btc_beta = rolling_beta(asset_return, btc_return)
```

### Decision logic

```text
If funding_z is high and oi_z is high and depth_z is falling:
    treat as crowded-long fragility
    do not blindly short
    wait for trigger: price breaks short-term support or taker flow flips

If funding_z is high and spot_volume_z is high and depth_z stable:
    continuation more likely
    avoid contrarian short

If funding_z high but basis arbitrage spread > cost and borrow/short capacity exists:
    consider market-neutral basis trade, not directional short
```

### Risk rule

Never size the trade using average depth. Size it using stressed depth after volatility doubles and depth halves.

---

## Example 2 — Quant meltdown template for market-neutral crypto baskets

### Setup

You run a cross-sectional stat-arb strategy:

- Long cheap coins based on residual z-score.
- Short expensive coins.
- Dollar-neutral and beta-neutral to BTC.
- Rebalance every 4 hours.

### Hidden risk

Many other desks may use similar factors. If volatility spikes and leverage is cut, everyone sells the same longs and covers the same shorts.

### Lo-style risk memo

```markdown
## Crowded Unwind Risk

Strategy:
- Cross-sectional mean reversion across top 50 crypto assets

Apparent hedge:
- Dollar neutral
- BTC beta neutral

Hidden exposure:
- Long illiquid high-beta alts
- Short liquid large caps
- Short volatility through convergence assumption
- Long liquidity premium
- Exposed to synchronized deleveraging

Crowding indicators:
- Same factor return sharply negative across universe
- Long-leg underperforms short-leg despite BTC hedge
- Cross-sectional correlation rises
- Funding and open interest unwind together
- Bid depth collapses in long-leg names

Stress action:
- Reduce gross exposure
- Increase liquidity score threshold
- Cap long-leg concentration
- Add factor crowding penalty
- Temporarily widen entry threshold
- Freeze new positions during liquidation cascades
```

### Risk dashboard metrics

```text
gross_exposure
net_exposure
BTC_beta
ETH_beta
PC1_exposure
long_leg_avg_spread
short_leg_avg_spread
long_leg_depth_1pct
short_leg_depth_1pct
factor_return_today
crowding_score
liquidation_proxy
funding_pressure
```

---

## Example 3 — Adaptive regime classifier for strategy gating

### Purpose

Instead of assuming one strategy works in all states, classify market ecology and gate strategy exposure.

### Regime variables

```text
vol_z                # realized volatility percentile/z-score
corr_z               # average pairwise correlation percentile
spread_z             # average spread percentile
depth_z              # order-book depth percentile
funding_abs_z        # absolute funding extremity
oi_z                 # open interest percentile
trend_strength       # medium-horizon momentum strength
liquidation_z        # liquidation pressure percentile
```

### Simple rule-based classifier

```python
from dataclasses import dataclass

@dataclass
class Regime:
    name: str
    risk_multiplier: float
    allowed_styles: list[str]


def classify_regime(vol_z, corr_z, spread_z, depth_z, funding_abs_z, oi_z, trend_strength, liquidation_z):
    """
    Rule-based Adaptive Markets regime classifier.
    Replace thresholds with walk-forward calibrated values.
    """
    if vol_z > 2 and corr_z > 1.5 and depth_z < -1 and liquidation_z > 1.5:
        return Regime(
            name="crisis_liquidation",
            risk_multiplier=0.25,
            allowed_styles=["liquidity_provision_only", "risk_reduction"]
        )

    if funding_abs_z > 2 and oi_z > 1.5 and trend_strength > 1:
        return Regime(
            name="crowded_trend",
            risk_multiplier=0.50,
            allowed_styles=["trend_following_with_trailing_stop", "basis_arbitrage"]
        )

    if vol_z < 0.5 and corr_z < 0.5 and spread_z < 0.5 and depth_z > 0:
        return Regime(
            name="normal_liquid",
            risk_multiplier=1.00,
            allowed_styles=["mean_reversion", "cross_sectional_stat_arb", "market_making"]
        )

    if vol_z > 1 and trend_strength > 1 and corr_z > 1:
        return Regime(
            name="macro_beta_dominant",
            risk_multiplier=0.60,
            allowed_styles=["trend_following", "reduced_cross_sectional"]
        )

    return Regime(
        name="uncertain_transition",
        risk_multiplier=0.50,
        allowed_styles=["small_size", "research_only"]
    )
```

### Usage

```text
position_size = base_position_size * regime.risk_multiplier
only trade if strategy_style in regime.allowed_styles
```

---

## Example 4 — Market-sense drill: who is forced to trade?

### Scenario

BTC falls 8% in one hour. Altcoins fall 15–25%. Perp funding flips negative. Spreads widen. Stablecoin basis becomes noisy.

### Drill questions

1. Who is forced to sell?
2. Who is forced to buy?
3. Which collateral is being liquidated?
4. Which exchanges have the most open interest?
5. Is this information shock, leverage shock, or liquidity shock?
6. Are correlations rising because fundamentals changed or because balance sheets are constrained?
7. Is your strategy long liquidity or short liquidity?
8. What should you stop doing immediately?
9. What trade becomes attractive only after forced selling is exhausted?

### Possible answer

```markdown
Forced sellers:
- Leveraged longs near liquidation thresholds
- Funds reducing gross exposure
- Market makers reducing inventory
- Traders with altcoin collateral

Forced buyers:
- Short perps taking profit
- Liquidation arbitrageurs
- Basis traders closing shorts if funding flips too negative

Mechanism:
- Initial BTC shock triggers margin stress
- Alt collateral falls faster
- Liquidations create market sells
- Market makers widen spreads
- Correlations rise
- Cross-sectional signals fail because common deleveraging dominates idiosyncratic value

Action:
- Disable mean-reversion entries until liquidation pressure normalizes
- Reduce gross exposure
- Trade only most liquid instruments
- Track funding, OI, depth, and liquidation flow for stabilization
```

---

## Example 5 — AI financial research copilot architecture

### Goal

Build an AI system to help research financial markets without hallucinating or making unverified trading claims.

### Architecture

```text
User question
  -> Intent classifier
  -> Source retrieval
      - papers
      - exchange docs
      - filings
      - news
      - internal backtest docs
  -> Calculation tools
      - returns
      - risk metrics
      - portfolio accounting
      - transaction cost model
  -> LLM reasoning layer
  -> Verification layer
      - source citations
      - numerical checks
      - consistency checks
      - hallucination checks
  -> Human approval
  -> Research memo
```

### Guardrails

```markdown
- The model must cite every factual market claim.
- The model must not calculate PnL without using the accounting tool.
- The model must separate hypothesis from evidence.
- The model must show cost assumptions.
- The model must label regulatory/tax/legal uncertainty.
- The model must not issue live-trading instructions without human approval.
```

### Lo-style principle

AI is powerful for financial advice and analysis, but high-stakes decisions require domain-specific modules, fiduciary framing, bias checks, explainability, and accountability.

---

## Example 6 — Research memo template for a new strategy

```markdown
# Strategy Research Memo

## 1. Observation
What market behavior did we observe?

## 2. Adaptive mechanism
Why might this behavior exist?
Which agents create it?
Which constraints make it persistent?

## 3. Hypothesis
State the tradable hypothesis in one sentence.

## 4. Data
Required data:
- prices
- volume
- order book
- funding
- open interest
- liquidations
- news/text/on-chain if relevant

## 5. Signal construction
Formula:
Feature transformations:
Normalization:
Lag assumptions:

## 6. Backtest
Universe:
Frequency:
Rebalance:
Execution price:
Costs:
Slippage:
Position sizing:
Risk limits:

## 7. Results
Gross return:
Net return:
Sharpe:
Max drawdown:
Turnover:
Capacity:
Hit rate:
Tail loss:

## 8. Robustness
Subperiods:
Regimes:
Parameter sensitivity:
Alternative universes:
Walk-forward:
Out-of-sample:

## 9. Risk
Hidden beta:
Liquidity:
Crowding:
Leverage:
Operational:
Model:
AI/data risk:

## 10. Decision
Reject / research more / paper trade / trade small / scale

## 11. Monitoring
What tells us the ecology has changed?
What kills the strategy?
```

---

## Example 7 — Lo-style stop-loss analysis

### Naive question

“Should I use a stop-loss?”

### Better question

“Under what serial correlation, regime switching, transaction cost, and behavioral constraint does a stop-loss improve expected utility or reduce ruin risk?”

### Practical test

```text
For each asset/strategy:
1. Estimate return autocorrelation by regime.
2. Estimate gap risk and transaction cost.
3. Test stop thresholds across walk-forward windows.
4. Compare:
   - buy/hold or strategy baseline
   - fixed stop
   - volatility-scaled stop
   - regime-conditioned stop
   - drawdown de-risking
5. Evaluate not just Sharpe, but max drawdown, recovery time, turnover, and cost drag.
```

### Interpretation

A tight stop-loss may reduce downside but destroy returns through excessive trading costs. A regime-aware stop may help if losses cluster and transaction costs are manageable.

---

## Example 8 — Crisis narrative table

Use this when everyone has a strong opinion after a crash.

```markdown
| Narrative | Evidence For | Evidence Against | Data Needed | Trading/Risk Implication |
|---|---|---|---|---|
| Macro shock | BTC and equities fell together | Some crypto-specific names fell more | SPX, rates, DXY, BTC beta | Reduce macro beta |
| Leverage unwind | OI collapsed, liquidations spiked | Funding was not extreme before event | OI, liquidation, funding | Reduce leverage/crowding |
| Liquidity shock | Depth collapsed, spreads widened | Volume remained high | L2 order book, slippage | Trade smaller, widen bands |
| Exchange-specific issue | One venue led move | Other venues followed quickly | Cross-exchange prices | Monitor venue risk |
| Information event | News preceded move | Price moved before news | Timestamped news/feed | Improve event detection |
```

Lesson: Do not choose one narrative because it is emotionally satisfying. Convert narratives into measurable claims.

---

## Example 9 — Daily market-sense journal

```markdown
# Daily Market Ecology Journal

Date:

## Market state
- BTC trend:
- Volatility:
- Correlation:
- Funding:
- Open interest:
- Liquidity/depth:
- Dominant narrative:

## Agent behavior
- Who is making money?
- Who is losing money?
- Who is forced to trade?
- What heuristic is dominant?

## Strategy implications
- Best style today:
- Worst style today:
- Signals to trust less:
- Signals to trust more:

## Risk
- Main tail risk:
- Crowded trade:
- Liquidity concern:
- Kill-switch trigger:

## Learning
- What surprised me?
- What did I misread?
- What changed in market ecology?
```

---

## Example 10 — One-week training plan for market sense

### Day 1: Market efficiency map

Pick one crypto pair and estimate signal decay for momentum, mean reversion, funding, and order-flow imbalance.

### Day 2: Agent map

List every major participant and infer their constraints.

### Day 3: Liquidity stress

Replay a high-volatility day. Measure spread, depth, slippage, and liquidation flow.

### Day 4: Crowding

Build a simple crowded-trade proxy using funding, open interest, price trend, and social/news attention.

### Day 5: Risk dashboard

Build gross/net exposure, beta, liquidity, factor, and tail-risk metrics for one toy portfolio.

### Day 6: Crisis narrative

Choose one market crash and build a multi-narrative table.

### Day 7: Strategy memo

Write a one-page research memo using the template in Example 6.

---

# Final rule

Every strategy idea must answer:

> What adaptive behavior creates this opportunity, what risk am I being paid to bear, who can force me out, and how will I know the ecology has changed?

