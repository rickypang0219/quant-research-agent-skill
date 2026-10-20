# Feynman Lens Examples

## Example 1 - PCA Stat Arb

Fancy version:

```text
We project returns onto a latent factor subspace and trade residual dislocations.
```

Plain version:

```text
Many coins move together because the whole market moves. We first remove the common market movement. What remains is the coin-specific wiggle. The bet is that an unusually large wiggle may shrink back.
```

Toy example:

- BTC and ETH usually move together.
- BTC rises 1%.
- ETH rises 5%.
- If the common factor explains only 1%, ETH has a +4% residual move.
- The strategy asks whether that residual tends to reverse after costs.

Falsifier:

```text
Residuals do not mean-revert out-of-sample after fees and slippage.
```

## Example 2 - Market Impact

Plain version:

```text
If you demand liquidity now, you push through the book. The price moves because the cheap liquidity gets used first and the remaining liquidity is more expensive.
```

Toy example:

- Best ask: 1 BTC at 100.
- Next ask: 2 BTC at 101.
- You buy 2 BTC.
- Average fill is above 100.

Equation meaning:

```text
impact = extra price paid because your order consumed available liquidity
```

Failure:

```text
If the backtest fills the whole order at mid, it is pretending the order book is infinitely deep.
```

## Example 3 - Volatility Targeting

Plain version:

```text
When the road is slippery, drive slower. Volatility targeting reduces position size when price movement becomes larger.
```

Toy example:

- Same signal strength.
- Normal volatility: trade $100.
- Volatility doubles: trade $50.

Question:

```text
Does reducing size lower drawdowns enough to justify the extra turnover?
```

## Example 4 - Martingale

Plain version:

```text
A martingale is a fair game under a chosen information set: given what you know now, the expected next value is the current value.
```

Quant warning:

```text
Risk-neutral martingale pricing does not mean the asset has no real-world expected return. It means discounted prices are fair under the pricing measure.
```

## Example 5 - Cargo-Cult Backtest

Looks scientific:

- many charts;
- high Sharpe;
- optimized parameters;
- advanced model;
- no data audit;
- no transaction costs;
- no forward test;
- no experiment ledger.

Verdict:

```text
This has the appearance of quant research but not the substance. First audit data, timing, costs, baselines, and out-of-sample behavior.
```

