### The 5-Level Validation Pyramid

Each level gates the next. Don't proceed to the next level if the current one fails.

```
        Level 5: Human Review
              (Alignment with intent)
                    |
        Level 4: Integration Tests
              (System behavior)
                    |
        Level 3: Unit Tests
              (Isolated logic)
                    |
        Level 2: Type Safety
              (Type checking)
                    |
        Level 1: Syntax & Style
              (Linting, formatting)
```

**Level 1 — Syntax & Style**: Linting and formatting. Catch obvious errors fast. Run automatically after file writes.

**Level 2 — Type Safety**: Static type checking. Catch type errors before runtime. Run before running tests.

**Level 3 — Unit Tests**: Test isolated functions and classes. Verify logic correctness. AI writes tests alongside implementation.
- Common pitfall: AI mocking tests to pass. Require real test coverage, reject mocks without justification.

**Level 4 — Integration Tests**: Test system interactions. Verify components work together. Use fixtures, mock external services only.

**Level 5 — Human Review**: Strategic alignment check. Does it match the plan? Are patterns followed? Is the approach sound? AI handles levels 1-4; humans judge intent alignment.

### Validation as Feedback

When validation fails, it reveals missing context in the plan, unclear requirements, patterns to document, or commands to improve.

**Don't just fix the bug. Fix the system that allowed the bug.** When you see the same validation failures repeatedly, that's a signal to improve your system — not just your code. Use `/system-review` for this.

### Validation Commands

Beyond embedded validation in plans, these commands provide on-demand validation:
- `/code-review` — Technical code review on changed files (run before commit)
- `/code-review-fix [review] [scope]` — Fix issues from code review
- `/execution-report` — Generate implementation report (run in same context as execute)
- `/system-review [plan] [report]` — Divergence analysis for process improvement

See section 09 for full command descriptions.
