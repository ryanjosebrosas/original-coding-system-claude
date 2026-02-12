---
description: Fix issues found in code review
argument-hint: [review-path-or-description] [scope]
---

I ran a code review and found these issues:

Code review (file path or description of issues): $1

Scope (optional — narrow focus to specific issues): $2

Please fix these issues one by one. If $1 is a file path, read the entire file first to understand all issues.

For each fix:
1. Explain what was wrong
2. Show the fix
3. Create and run relevant tests to verify

After all fixes, run the project's validation suite (linting, type checking, tests) to finalize.

## Notes

- You may choose NOT to fix issues that are already documented as acceptable, out of scope for MVP, or not actually problems. Explain your reasoning.
- If the review is very long with 20+ issues, focus on high/critical severity first. Use the scope parameter ($2) to narrow focus.
