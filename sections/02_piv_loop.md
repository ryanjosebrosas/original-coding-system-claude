```
PLAN → IMPLEMENT → VALIDATE → (iterate)
```

### Granularity Principle

Always do **smaller iterations**. Multiple small PIV loops, never try to implement everything at once. Each loop picks ONE feature slice and builds it completely before moving on.

### Planning (Layer 1 + Layer 2)

**Layer 1 — Project Planning** (done once, updated rarely):
- **PRD** (Product Requirements Document) — defines **what** to build (MVP scope, features, architecture, success criteria). Use template: `templates/PRD-TEMPLATE.md`
- **CLAUDE.md** (Global Rules) — defines **how** to build (tech stack, conventions, patterns)
- **On-demand context** — reference guides, external docs, tool designs (in `reference/`)
- PRD feeds into everything: it helps define your rules and on-demand context

**Layer 2 — Task Planning** (done for every feature):
1. **Vibe Planning** — casual, unstructured conversation
   - Explore ideas, ask questions, research codebase
   - Reference the PRD to choose the next logical feature
   - No structure needed, just get on the same page
   - See examples: `templates/VIBE-PLANNING-GUIDE.md`
2. **Structured Plan** — turn conversation into a markdown document
   - Use template: `templates/STRUCTURED-PLAN-TEMPLATE.md`
   - Save to: `requests/{feature}-plan.md`
   - Apply the 4 pillars of Context Engineering

**Do NOT** take your PRD and use it as a structured plan. Break it into granular Layer 2 plans — one per PIV loop.

**Model recommendation**: Use Opus for `/planning` sessions (`claude --model opus`) and Sonnet for everything else (`claude` default). Planning is the highest-leverage phase — Opus's reasoning quality directly impacts plan quality. See `reference/multi-model-strategy.md` for configuration.

**Billing**: Claude Code works with MAX subscription ($100-200/month, recommended) or API billing (pay-per-token). With MAX, all models share a usage pool. Ensure `ANTHROPIC_API_KEY` is NOT set in your environment to use subscription billing. See `reference/multi-model-strategy.md` for details.

### Implementation
- Start a **new conversation** (fresh context)
- Feed ONLY the structured plan
- Use command: `/execute requests/{feature}-plan.md`
- Or use prompt: `templates/IMPLEMENTATION-PROMPT.md` (for non-Claude Code tools)
- Trust but verify: watch loosely, don't micromanage
- **Remote execution (optional)**: The PIV Loop can also run remotely via GitHub Actions. Create a GitHub Issue, comment `@claude-fix` or `@claude-create`, and the full loop runs in CI. See `sections/10_github_integration.md` for setup.

### Validation
- **AI validates**: unit tests, integration tests, linting
- **Human validates**: code review (git diffs), questions, manual testing
- Use checklist: `templates/VALIDATION-PROMPT.md`
- Small issues: one-off fix prompts
- Major issues: revert to git save point, tweak plan, retry

#### Enhanced Validation Workflow (optional)

For thorough validation, chain these commands after implementation:

```
/execute [plan] → /execution-report → /code-review → /code-review-fix → /commit
```

- **`/execution-report`** — Run in the SAME context as `/execute`, BEFORE commit. Captures what happened while the AI has full memory of the implementation.
- **`/code-review`** — Technical quality check on changed files. Finds bugs, security issues, performance problems.
- **`/code-review-fix`** — Takes the code review output and fixes issues one by one.
- **`/system-review [plan] [report]`** — Run AFTER commit when you want to evolve the system. Compares plan vs implementation to find process bugs (not code bugs). High leverage but not needed every loop.

### Leveraging Save States

Since every plan and implementation gets committed, you have save points at every stage:
- **Bad plan?** Go back to the commit before the plan, evolve the command, retry
- **Bad implementation?** Go back to the plan commit (`git stash` or `git checkout .`), tweak the plan, retry with `/execute`
- **After evolving the system** (fixing a command/template), you can retry from any save point to see if the fix works

---

**For deeper context**: See `reference/system-foundations.md` for:
- Why the PIV Loop exists (the system gap)
- How to measure your improvement (baseline assessment)
- Course architecture and trust progression
- Understanding AI strengths and limitations

**For PIV Loop in practice**: See `reference/piv-loop-practice.md` for:
- Layer 1 vs Layer 2 planning (CLAUDE.md vs feature plans)
- Vibe planning → structured planning workflow
- The 4 Pillars of Context Engineering in action
- Implementation with fresh context strategies
- Systematic validation (5-level pyramid)
- Git save points for confident iteration

**For global rules optimization**: See `reference/global-rules-optimization.md` for:
- Two-Question Framework (constant vs task-specific, auto-load vs on-demand)
- Version 1 vs Version 2 CLAUDE.md organization (@sections)
- Strategic context loading to avoid token bloat
- 10 recommended sections for comprehensive coverage
