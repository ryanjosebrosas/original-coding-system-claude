---
description: Technical code review for quality and bugs
---

Perform technical code review on recently changed files.

## Review Philosophy

- Simplicity is the ultimate sophistication — every line should justify its existence
- Code is read far more often than it's written — optimize for readability
- The best code is often the code you don't write
- Elegance emerges from clarity of intent and economy of expression

## Review Mode Selection

**If custom review agents exist** in `.claude/agents/`:
- Use **Parallel Review** (4 specialized agents, 40-50% faster)
- Agents: code-review-type-safety, code-review-security, code-review-architecture, code-review-performance

**If no custom agents exist**:
- Use **Standard Review** (single-agent sequential review)

Check for agents:
```bash
ls .claude/agents/code-review-*.md 2>/dev/null | wc -l
```

---

## PARALLEL REVIEW MODE (Preferred)

Launch four Task agents simultaneously for comprehensive review:

### Agent 1: Type Safety Review → @code-review-type-safety

Focus: Type annotations, type checking, proper typing
Returns: Type safety findings with severity levels

### Agent 2: Security Review → @code-review-security

Focus: Vulnerabilities, exposed secrets, injection attacks, auth issues
Returns: Security findings with attack vectors and impact

### Agent 3: Architecture Review → @code-review-architecture

Focus: Pattern compliance, layering, DRY/YAGNI, conventions
Returns: Architecture findings with pattern violations

### Agent 4: Performance Review → @code-review-performance

Focus: N+1 queries, algorithm efficiency, memory issues
Returns: Performance findings with complexity analysis

**Execution**: All four agents run in parallel. Each reviews ALL changed files from their specialized perspective.

**After agents complete**:
1. Wait for all four agents to return results
2. Combine findings into unified report
3. Remove duplicate findings (same issue caught by multiple agents)
4. Sort by severity: Critical → Major → Minor
5. Save to `requests/code-reviews/[feature-name]-review.md`

## Archon Integration (Optional)

**If code review is part of a PIV Loop with Archon task management:**

After review report generation, update the code review task status:
- Find code review task: `find_tasks(query="code review", filter_by="status", filter_value="doing")`
- Mark complete: `manage_task("update", task_id="{task_id}", status="done")`

This is OPTIONAL — code review can be run standalone without Archon.

---

## STANDARD REVIEW MODE (Fallback)

Use when custom agents don't exist.

### Step 1: Gather Context

Read codebase context to understand standards:
- @CLAUDE.md — Read project rules and conventions
- README files at project root

### Step 2: Examine Changes

```bash
git status
git diff HEAD
git diff --stat HEAD
git ls-files --others --exclude-standard
```

Read each changed file in its entirety (not just the diff) for full context.

### Step 3: Analyze Each File

Check for:

1. **Logic Errors**
   - Off-by-one errors, incorrect conditionals, missing error handling, race conditions

2. **Security Issues**
   - SQL injection, XSS, insecure data handling, exposed secrets

3. **Performance Problems**
   - N+1 queries, inefficient algorithms, memory leaks, unnecessary computations

4. **Code Quality**
   - DRY violations, overly complex functions, poor naming, missing type hints

5. **Adherence to Standards**
   - Conventions from CLAUDE.md, linting/typing standards, logging/testing patterns

### Step 4: Verify Issues

- Run specific tests for issues found
- Confirm type errors are legitimate
- Validate security concerns with context

---

## Output Format (Both Modes)

Save to: `requests/code-reviews/[feature-name]-review.md`

### Review Summary

- **Mode**: Parallel / Standard
- **Files Modified**: X
- **Files Added**: X
- **Files Deleted**: X
- **Total Findings**: X (Critical: Y, Major: Z, Minor: W)

### Findings by Severity

**For each issue:**

```yaml
severity: critical|major|minor
category: Type Safety|Security|Architecture|Performance|Logic|Quality
file: path/to/file:line
issue: [one-line description]
detail: [explanation of why this is a problem]
suggestion: [how to fix it]
```

### Security Alerts

If any CRITICAL security issues found, list them separately at top of report with:
- Attack vector
- Potential impact
- Immediate remediation steps

### Summary Assessment

- Overall: [Pass / Needs minor fixes / Needs revision / BLOCKED - critical issues]
- Recommended action: [Commit as-is / Fix minor issues / Major rework needed]

If no issues found: "Code review passed. No technical issues detected."

---

## Important

- Be specific (line numbers, not vague complaints)
- Focus on real bugs, not style preferences
- Suggest fixes, don't just complain
- Flag security issues as CRITICAL
- In parallel mode, avoid duplicate findings across agents
