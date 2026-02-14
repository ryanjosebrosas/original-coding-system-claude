# Validation Report

> Standard output format for PIV Loop validation results.
> Run validation using `templates/VALIDATION-PROMPT.md` before filling this report.
> AI fills Levels 1-4 automatically. Humans complete Level 5.
>
> **Core Principle**: Validate in order — don't run integration tests
> if linting fails. Fix issues at each level before proceeding.

---

## Report Header

- **Feature**: {feature name}
- **Date**: {YYYY-MM-DD}
- **Validator**: {AI / Human / Both}
- **Plan Reference**: `requests/{feature}-plan.md`

---

## Results

```
Validation Results
-------------------------------------------------------------------
{PASSED|FAILED} {linting_tool}:     {PASSED (0 issues) | FAILED (N issues)}
{PASSED|FAILED} {formatter}:        {PASSED | FAILED}
{PASSED|FAILED} {type_checker}:     {PASSED | FAILED (N errors)}
{PASSED|FAILED} Unit Tests:         {PASSED (N tests, Xs) | FAILED}
{PASSED|FAILED} Integration Tests:  {PASSED | FAILED}
-------------------------------------------------------------------
Status: {ALL CHECKS PASSED | VALIDATION FAILED}
```

### Level 1: Syntax & Style

| Tool | Command | Result |
|------|---------|--------|
| {linting_tool} | `{lint command}` | {PASSED / FAILED (N issues)} |
| {formatter} | `{format check command}` | {PASSED / FAILED} |

### Level 2: Type Safety

| Tool | Command | Result |
|------|---------|--------|
| {type_checker} | `{type check command}` | {PASSED / FAILED (N errors)} |

### Level 3: Unit Tests

| Metric | Value |
|--------|-------|
| Tests run | {count} |
| Tests passed | {count} |
| Time | {seconds} |
| Command | `{test command}` |

### Level 4: Integration Tests

| Metric | Value |
|--------|-------|
| Tests run | {count} |
| Tests passed | {count} |
| Time | {seconds} |
| Command | `{test command}` |

### Level 5: Human Review

| Check | Result | Notes |
|-------|--------|-------|
| Code review (git diffs) | {PASSED / FAILED} | {notes} |
| Manual testing (UI, workflows) | {PASSED / FAILED} | {notes} |
| Alignment with intent | {PASSED / FAILED} | {notes} |
| Edge cases not covered by tests | {PASSED / FAILED} | {notes} |

---

## Issues Found

> Group by category. Use `file:line` format.

### {Category} ({count})

- `{file:line}` — {issue description}

---

## AI vs Human Validation Checklist

**AI handles (Levels 1-4):**
- [ ] Linting (syntax, style)
- [ ] Type checking (type safety)
- [ ] Unit tests (isolated logic)
- [ ] Integration tests (system behavior)

**Humans handle (Level 5):**
- [ ] Code review (patterns, design)
- [ ] Manual testing (real usage)
- [ ] Alignment with intent (does it solve the right problem?)
- [ ] Edge cases not covered by automated tests

---

## Status

**{ALL CHECKS PASSED | VALIDATION FAILED}**

{If failed: list blocking issues and recommended next steps}

---

> **Reference**: See `reference/validation-strategy.md` for the 5-level validation pyramid and `reference/piv-loop-practice.md` Section "Validation Report Format" for examples.
