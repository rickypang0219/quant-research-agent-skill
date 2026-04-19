---
name: research-to-production-handoff
description: Use to convert notebook or research code into production-ready quant modules, configs, tests, data contracts, monitoring, deployment plans, and ownership handoff.
---

# Research to Production Handoff Workflow

## Purpose

Move a strategy from notebook logic to maintainable, testable, deployable code without changing its behavior silently.

## Required Artifacts

- research report;
- frozen config;
- data contract;
- feature definitions;
- signal definitions;
- PnL/accounting formula;
- risk limits;
- tests;
- monitoring metrics;
- runbook;
- rollback plan.

## Handoff Questions

- What exact code path produced the research result?
- What assumptions must production preserve?
- What data is required at decision time?
- What happens when data is missing?
- What risk checks can block orders?
- What metrics prove live behavior matches research?

## Output Standard

1. Research artifact inventory
2. Production module map
3. Data contracts
4. Config schema
5. Tests
6. Monitoring
7. Deployment plan
8. Handoff verdict

