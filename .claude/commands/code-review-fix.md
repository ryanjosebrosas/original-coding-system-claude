---
description: "I ran a code review and found these issues:"
argument-hint: [review-path-or-description] [scope]
---

# Fix Issues from Code Review

## Input

- **Review source** ($1): File path to a code review report, OR inline description of issues
- **Scope** ($2, optional): Filter for specific severity (`critical`, `major`, `minor`, `critical+major`) or file path pattern (e.g., `src/auth/`)

Review input: $ARGUMENTS

## Step 1: Load the Review

**If $1 is a file path** (e.g., `requests/code-reviews/feature-review.md`):
- Read the entire review file
- Parse findings by the standard review output format (severity/category/file/issue/detail/suggestion)

**If $1 is an inline description**:
- Treat the description as a single issue or set of issues
- Infer severity if not specified (default to major)

**If no input provided**:
- Check `requests/code-reviews/` for the most recent review file
- If none found, ask the user what issues to fix

## Step 2: Categorize and Prioritize

Parse all findings and group by severity:

1. **CRITICAL** — Security vulnerabilities, data loss risks, crashes, authentication bypasses
2. **MAJOR** — Logic errors, missing validation, performance problems, incorrect behavior
3. **MINOR** — Style issues, naming inconsistencies, documentation gaps, code smell

**Apply scope filter** (if $2 provided):
- `critical` → only fix critical issues
- `critical+major` → fix critical and major issues, skip minor
- `major` → only fix major issues
- File path pattern (e.g., `src/auth/`) → only fix issues in matching files
- If no scope: fix all issues, starting with critical

**Report the triage**:
```
Found X issues: Y critical, Z major, W minor
Scope: [all | filtered to ...]
Fixing in order: critical → major → minor
```

## Step 3: Apply the Selectivity Principle

Before fixing each issue, evaluate whether it SHOULD be fixed. You may choose **NOT to fix** issues that are:

- Already documented as acceptable in CLAUDE.md or project conventions
- Out of scope for the current feature/MVP
- Would require architectural changes beyond a targeted fix
- Style preferences rather than actual bugs
- False positives from the review (the code is actually correct)

**For each skipped issue**: Explain the reasoning clearly. Never silently skip.

**Bias check**: Default to fixing. Only skip when there's a genuine reason — not because it's inconvenient. When in doubt, fix it.

## Step 4: Fix Issues (One at a Time)

For EACH issue being fixed, follow this process:

### a. Understand Context
- Read the **entire affected file** (not just the flagged line)
- Understand the surrounding code, function purpose, and call sites
- Check if the issue is part of a larger pattern that needs consistent fixing

### b. Explain the Problem
- State what's wrong and WHY it's a problem
- Reference the review finding (severity, category, file:line)

### c. Apply the Fix
- Make the **minimal change** needed to resolve the issue
- Do NOT refactor surrounding code, add features, or "improve" unrelated areas
- If the fix requires changes in multiple files (e.g., type change propagation), fix all affected files
- Preserve existing code style and patterns

### d. Verify the Fix
- If the task has a validation command (from the plan's VALIDATE field), run it
- Check that the fix doesn't introduce new issues (type errors, import errors)
- If a test exists for the affected code, run it

## Step 5: Post-Fix Validation

After ALL fixes are applied, run the project's validation suite in pyramid order:

1. **Linting** — run project linter if configured
2. **Type checking** — run type checker if configured
3. **Tests** — run the project's test suite

If any validation fails:
- Fix the regression
- Re-run validation
- Only proceed when all checks pass

If no project validation tools are configured, note this in the output.

## Step 6: Output Summary

### Fix Summary

| Severity | Found | Fixed | Skipped |
|----------|-------|-------|---------|
| Critical | X | X | X |
| Major | X | X | X |
| Minor | X | X | X |
| **Total** | **X** | **X** | **X** |

### Issues Fixed
For each fixed issue:
- **[severity]** `file:line` — issue description → fix applied

### Issues Skipped
For each skipped issue:
- **[severity]** `file:line` — issue description → reason for skipping

### Validation Results
- Linting: pass/fail/not configured
- Type checking: pass/fail/not configured
- Tests: pass/fail/not configured

### Recommended Next Steps
- If all critical+major fixed and validation passes → ready for `/commit`
- If issues remain → suggest running `/code-review-fix` again with narrower scope
- If architectural issues were skipped → suggest creating a follow-up task

## Archon Integration (Optional)

**If this fix is part of a PIV Loop with Archon task management:**
- Find task: `find_tasks(query="code review fix", filter_by="status", filter_value="doing")`
- Mark complete: `manage_task("update", task_id="{task_id}", status="done")`

This is OPTIONAL — code-review-fix can be run standalone without Archon.

## Important Rules

- **Severity order is mandatory** — always fix critical before major before minor
- **Selectivity over completeness** — a thoughtful skip is better than a harmful fix
- **Minimal changes** — fix the issue, nothing more. This is surgery, not renovation
- **Explain everything** — every fix and every skip gets a clear explanation
- **Never auto-fix all** — evaluate each issue individually, even when scope is "all"
