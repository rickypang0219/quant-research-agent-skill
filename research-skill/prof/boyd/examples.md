# Boyd Lens Examples

## Example 1 - Long/Short Portfolio Optimization

Decision variable:

```text
w_i = portfolio weight in asset i
```

Objective:

```text
maximize alpha' w - lambda * w' Sigma w - cost_rate' |w - w_prev|
```

Constraints:

```text
sum_i w_i = 0
sum_i |w_i| <= gross_limit
B' w = 0
|w_i| <= single_name_cap
turnover <= turnover_cap
```

Checks:

- Is `Sigma` positive semidefinite?
- Are factor exposures point-in-time?
- Which constraints bind?
- Does the solution survive alpha/covariance perturbation?

## Example 2 - Infeasible Neutrality

If beta neutrality, sector neutrality, gross cap, and single-name caps make the problem infeasible, do not loosen constraints silently.

Report:

```text
The signal cannot be expressed under the requested risk constraints. Either expand the universe, relax neutrality, or reject the trade.
```

## Example 3 - Turnover-Aware Rebalance

Instead of replacing the portfolio every bar, solve:

```text
minimize -alpha' w + gamma * risk(w) + eta * ||w - w_prev||_1
```

This makes turnover a first-class design variable.

