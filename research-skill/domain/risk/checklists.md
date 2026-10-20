# Risk Checklists

## Research Risk Checklist

- [ ] Universe known at each historical timestamp.
- [ ] Gross, net, beta, sector/factor exposures computed.
- [ ] Leverage and margin rules match instrument.
- [ ] Funding, borrow, and financing included.
- [ ] Costs and slippage stressed.
- [ ] Volatility target does not use future volatility.
- [ ] Turnover and capacity estimated.
- [ ] Drawdown and drawdown duration measured.
- [ ] Tail metrics reported: VaR/ES or empirical quantiles.
- [ ] Performance sliced by regime and liquidity.

## Live Risk Checklist

- [ ] Pre-trade limits implemented.
- [ ] Post-trade positions reconciled.
- [ ] Exchange balances reconciled.
- [ ] Stale data guard implemented.
- [ ] Max order size and max order rate enforced.
- [ ] Per-symbol notional cap enforced.
- [ ] Gross/net exposure cap enforced.
- [ ] Max daily loss and max drawdown kill switch enforced.
- [ ] Liquidation-distance monitor for futures/perps.
- [ ] Funding/basis monitor for carry strategies.
- [ ] Alerting and incident log in place.
- [ ] Manual and automatic kill switch tested.

## Promotion Gate

No paper/live promotion unless:

- risk limits are expressed as config, not hard-coded guesses;
- at least one unit test verifies each core limit;
- simulated breach behavior is tested;
- live state reconciliation has a failure path;
- the user can explain the largest plausible loss scenario.

