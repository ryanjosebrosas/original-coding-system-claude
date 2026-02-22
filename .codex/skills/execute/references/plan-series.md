# Plan Series Execution

## Detection

File contains marker: `<!-- PLAN-SERIES -->`

## Sub-Plan Structure

```
## PLAN INDEX

1. [Sub-plan 1](requests/feature-part1-plan.md)
2. [Sub-plan 2](requests/feature-part2-plan.md)
```

## Execution

1. Read overview for shared context
2. Execute sub-plans in order
3. Read HANDOFF NOTES between sub-plans
4. Stop if any sub-plan fails
5. Generate series report
