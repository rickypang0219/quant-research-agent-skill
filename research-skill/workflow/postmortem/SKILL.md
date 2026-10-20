---
name: postmortem
description: Use after losses, bad fills, outages, data failures, risk breaches, unexpected exposure, backtest/live divergence, or production incidents to produce a rigorous incident review and prevention plan.
---

# Postmortem Workflow

## Purpose

Convert failures into system improvements. Do not search for comforting narratives. Identify what happened, why controls failed, and what tests or limits prevent recurrence.

## Required Sections

1. Timeline
2. Expected behavior
3. Actual behavior
4. Financial impact
5. Root cause
6. Contributing factors
7. Detection gap
8. Control gap
9. Fixes
10. Tests added
11. Owner and deadline

## Incident Classes

- data outage;
- stale signal;
- bad fill;
- rejected/canceled order;
- position mismatch;
- risk-limit failure;
- exchange/API failure;
- model drift;
- unexpected drawdown;
- deployment/config mistake.

