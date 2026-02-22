---
description: Orchestrate a multi-agent swarm for complex, parallelizable tasks
argument-hint: "[task-description]"
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "Task"]
---

# Swarm

## Input

Task description: $ARGUMENTS

If no description is provided, ask the user: "What complex task would you like to swarm? Describe the epic goal (e.g., 'Add user authentication with login, logout, and session management', 'Refactor the API layer to use a new database schema')."

## Step 1: Analyze the Task

Understand what the user wants to achieve:
- What is the end state?
- Approximately how many files will need modification?
- Can the work be parallelized?
- Are there clear subsystem boundaries (frontend/backend/tests/database)?

**If the task is simple (1-2 files)**, recommend: "This task might not need a full swarm. Would you like me to implement it directly, or would you prefer to use the swarm workflow anyway?"

## Step 2: Load Project Context

Read project conventions:
- `QWEN.md` — core project rules
- `CLAUDE.md` — additional conventions (if exists)
- Relevant existing code for pattern matching

## Step 3: Decompose into Subtasks

Break the epic into 2-5 focused subtasks:

**Guidelines:**
- Each subtask should modify 1-4 specific files
- Avoid overlapping file assignments
- Identify dependencies (what must be done sequentially)
- Group related changes together

**Example decomposition for "Add user authentication":**

| Subtask | Files | Type | Dependencies |
|---------|-------|------|--------------|
| 1. Database schema | `src/db/schema.ts`, `migrations/001_auth.ts` | Data | none |
| 2. Auth API | `src/auth/login.ts`, `src/auth/logout.ts`, `src/auth/session.ts` | Backend | subtask 1 |
| 3. Auth UI | `src/components/LoginForm.tsx`, `src/components/SessionProvider.tsx` | Frontend | subtask 2 |
| 4. Integration tests | `tests/auth.test.ts`, `tests/e2e/auth-flow.test.ts` | Testing | subtasks 2-3 |

## Step 4: Create Swarm Plan Document

Create a plan document at `requests/swarm-[task-name]-plan.md`:

```markdown
# Swarm Plan: [Task Name]

## Epic Goal
[What this swarm achieves]

## Subtasks

### 1. [Subtask Title]
- **Files**: [file1.ts, file2.ts]
- **Worker**: swarm-worker
- **Dependencies**: [none | subtask X]
- **Description**: [What to implement]

### 2. [Subtask Title]
...

## Shared Context
[What all workers need to know about the project and epic]

## Execution Order
1. Subtask 1 (no dependencies)
2. Subtask 2 (depends on 1)
3. Subtask 3-4 (parallel, depend on 2)

## Success Criteria
- [ ] All subtasks completed and reviewed
- [ ] Tests passing
- [ ] No integration conflicts
- [ ] Code follows project conventions
```

## Step 5: Spawn Workers

### For Independent Subtasks (Parallel)

Spawn multiple workers in a single message:

```
I'm spawning workers for parallel subtasks:

**Worker 1** (Subtask 1: Database schema):
[Detailed prompt with files, requirements, context]

**Worker 2** (Subtask 2: Auth API):
[Detailed prompt with files, requirements, context]
```

### For Dependent Subtasks (Sequential)

Wait for each worker to complete before spawning the next:

```
Worker 1 has completed. Reviewing output...
[Review findings]

Now spawning Worker 2 with the context from Worker 1's changes...
```

## Step 6: Review Worker Output

For each completed worker:

1. **Check completeness**: Did they modify all assigned files?
2. **Check quality**: Does the code follow project conventions?
3. **Check tests**: Are tests added and passing?
4. **Check conflicts**: Would this conflict with other workers' changes?

**If issues found**: Request revision with specific feedback.

**If passed**: Mark subtask as complete and proceed.

## Step 7: Integration Review

Once all workers complete:

1. Verify all subtasks are marked as passed
2. Check for integration issues between components
3. Run full test suite if applicable
4. Identify any gaps or follow-up work needed

## Step 8: Final Report

Provide a comprehensive summary:

```markdown
## Swarm Completion Report

**Epic**: [Task Name]
**Status**: ✅ All passed / ⚠️ Some revisions needed

### Subtask Summary
| # | Title | Status | Files Modified |
|---|-------|--------|----------------|
| 1 | Database schema | ✅ Passed | 2 files |
| 2 | Auth API | ✅ Passed | 3 files |
| 3 | Auth UI | ✅ Passed | 2 files |
| 4 | Integration tests | ✅ Passed | 2 files |

### Integration Notes
[Any issues or considerations when combining the changes]

### Recommended Next Steps
1. Review the changes in each file
2. Run the full test suite
3. Commit the changes: `/commit`
4. Create PR: `/create-pr`
```

## Important Rules

- **Delegate, don't implement**: You are a coordinator — workers do the implementation
- **Clear boundaries**: Each worker owns specific files; no overlaps
- **Sequential for dependencies**: Don't parallelize dependent work
- **Thorough review**: Never approve substandard work
- **File reservations**: Remind workers to reserve files before editing
- **Context sharing**: Ensure workers know about related subtasks

## Model Selection

- **Coordinator**: Sonnet (balanced reasoning for planning and review)
- **Workers**: Sonnet for implementation, Haiku for simple/testing tasks

---

**After completion**, ask the user: "Would you like me to help you review the changes, run tests, or prepare a commit?"
