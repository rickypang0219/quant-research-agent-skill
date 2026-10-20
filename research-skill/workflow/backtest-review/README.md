# /workflow/backtest-review

This workflow is used to review whether a backtest is believable.

It focuses on:

- PnL formula correctness
- position timing
- fill realism
- fees and slippage
- funding and borrow
- turnover
- Sharpe ratio quality
- validation and forward testing
- robustness
- execution realism
- paper/live readiness

## Files

```text
/workflow/backtest-review
  SKILL.md
  formulas.md
  experiments.md
  checklists.md
  metrics.md
  red_flags.md
  code_review.md
  report_template.md
```

## Recommended Usage

Use this workflow after a strategy has produced a promising backtest.

The main question is:

```text
Is this alpha real, or is it an artifact of bad accounting, overfitting, or unrealistic execution?
```

## Relationship to /workflow/backtest

- `/workflow/backtest` builds and runs backtests.
- `/workflow/backtest-review` attacks and validates backtests.

A strategy should not move to paper trading until it survives `/workflow/backtest-review`.
