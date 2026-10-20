# /workflow/idea-to-hypothesis

This folder defines a reusable workflow skill for converting raw quant ideas into falsifiable, data-testable hypotheses.

## Files

```text
/workflow/idea-to-hypothesis/
├── SKILL.md
├── checklist.md
├── hypothesis_template.md
├── falsification_tests.md
├── professor_router.md
├── examples.md
├── output_schema.md
└── README.md
```

## How to Use

When you have a raw trading idea, ask the agent:

```text
Use /workflow/idea-to-hypothesis to convert this idea into a falsifiable quant hypothesis:
[insert idea]
```

The workflow should produce:

1. raw idea restatement
2. plain market translation
3. professor routing
4. market mechanism
5. observable variables
6. falsifiable hypothesis
7. null hypothesis
8. minimum viable experiment
9. backtest design
10. risk and cost assumptions
11. failure modes
12. next step
13. decision

## Design Philosophy

This workflow is adversarial but constructive.

It should not praise vague ideas.

It should force every idea through:

```text
analogy → observable → hypothesis → experiment → evidence → strategy
```

## Recommended Project Position

Place this folder at:

```text
/workflow/idea-to-hypothesis
```

Recommended neighboring folders:

```text
/workflow/hypothesis-to-backtest
/workflow/backtest-to-paper-trade
/workflow/paper-trade-to-live
/workflow/risk-review
/workflow/code-review
```

## Required Decision Labels

Every idea must end with one:

```text
REJECT
REFINE
TEST
PROTOTYPE
PAPER TRADE
DO NOT LIVE TRADE
```
