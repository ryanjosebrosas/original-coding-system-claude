# Parallel Workflow — Full 8-Stage Pipeline

> This reference is loaded on-demand during skill execution (Tier 3).

---

## Stage 1: Prime — Load Codebase Context

Build comprehensive understanding of the project:

1. Analyze project structure (files, directories)
2. Read core documentation (CLAUDE.md, README)
3. Identify key files (entry points, configs, schemas)
4. Understand current state (branch, recent commits)
5. Read memory.md for cross-session context (if exists)
6. Search Archon RAG for relevant documentation (if available)

Provide a brief summary before proceeding to planning.

---

## Stage 2: Plan All Features (Sequential)

For each feature (1 to N), create a comprehensive implementation plan:

1. Run the full `/planning` methodology (6 phases)
2. Save plan to `requests/{feature-name}-plan.md`
3. **After each plan (except the first)**: Run overlap detection

### Overlap Detection (Critical)

Compare file targets across all plans created so far:
- Read "New Files to Create" and task TARGET files from each plan
- If two plans modify the same file beyond registration points: **STOP**
- Present options to the user:
  - Remove the overlapping feature
  - Redesign for better isolation
  - Implement overlapping features sequentially

**Why sequential planning?** Overlap detection requires knowing previous plans. Parallel planning risks two plans modifying the same files without detection.

---

## Stage 3: Commit Plans (Git Save Point)

```bash
git add requests/{feature-1}-plan.md requests/{feature-2}-plan.md ...
git commit -m "plan: parallel plans for {feature-1}, {feature-2}, ..."
```

This creates a save point. If execution fails, revert with `git checkout .` or `git stash`.

---

## Stage 4: Create Worktrees (Parallel)

For each feature at index `i` (0-based):
- Branch: `feature/{kebab-name}`
- Path: `worktrees/{kebab-name}`
- Port: `8124 + i`

Launch N Task agents in parallel, each creating their worktree independently:
1. `git worktree add worktrees/{name} -b feature/{name}`
2. Navigate in and sync dependencies
3. Return to main repo

After all agents complete, verify all worktrees are READY.

**If any fail**: Report which failed, offer retry or continue with successful ones.

---

## Stage 5: Execute in Parallel (claude -p)

This is the core parallelization step.

### 5a. Copy Plans to Worktrees

```bash
mkdir -p worktrees/{name}/requests/
cp requests/{feature}-plan.md worktrees/{name}/requests/
```

### 5b. Launch Background Processes

For each feature, launch a headless `claude -p` process:

```bash
(cd worktrees/{name} && claude -p \
  --dangerously-skip-permissions \
  --output-format json \
  --max-turns 50 \
  "Read the plan at requests/{feature}-plan.md and execute ALL tasks..." \
  > logs/{name}.json 2>&1) &
PID_{i}=$!
```

### 5c. Wait for Completion

```bash
wait $PID_0 $PID_1 $PID_2 ...
```

### 5d. Check Results

Parse each log file for status, turns, cost, and duration. Report per-feature results table.

### Headless Mode Differences (`claude -p`)

- No interactive prompts — agent must be self-sufficient
- MCP servers may not be available — main conversation handles all MCP integration
- `--dangerously-skip-permissions` bypasses tool approval (required for unattended execution)
- `--max-turns 50` prevents infinite loops
- Output is JSON format for programmatic parsing

---

## Stage 6: Merge All Features (Sequential)

Embed `/merge-worktrees` logic:

### 6a. Verify Preconditions
- Running from repo root (not inside `worktrees/`)
- All successful feature branches have commits

### 6b. Create Integration Branch
```bash
git checkout -b integration-{first}-to-{last}
```

### 6c. Sequential Merge with Testing

For each successful feature:
```bash
git merge feature/{name} --no-ff -m "merge: integrate {feature}"
```
Run tests after each merge. Stop on conflict or test failure.

### 6d. Full Validation Suite

After all branches merged:
- Run test suite
- Run type checking
- Run any additional project validation

### 6e. Merge to Original Branch

```bash
git checkout $CURRENT_BRANCH
git merge integration-{first}-to-{last} --no-ff
```

### 6f. Cleanup
```bash
git branch -d integration-{first}-to-{last}
```

---

## Stage 7: Commit

Create a conventional commit for all merged features:

```
feat: parallel implementation of {feature-1}, {feature-2}, ...

Implemented N features in parallel using git worktrees + claude -p:
- {feature-1}: {brief description}
- {feature-2}: {brief description}
```

Update memory.md with lessons learned (if it exists).

---

## Stage 8: Create Pull Request

Push and create PR using `gh`:

```bash
git push -u origin $CURRENT_BRANCH
gh pr create --title "feat: parallel implementation of ..." --body "..."
```

Include in PR body:
- Summary of features implemented
- Links to plan files
- Test plan with validation results

---

## Feature Input Format

Features are provided as pipe-separated descriptions:

```
/parallel-e2e search functionality | CSV export | email notifications
```

Each is converted to:
- **Kebab-case name**: `search-functionality`
- **Branch**: `feature/search-functionality`
- **Plan path**: `requests/search-functionality-plan.md`

---

## Resource Considerations

- Each `claude -p` process runs independently with significant RAM/CPU usage
- N processes = N times API costs
- Local machines typically support 2-3 parallel agents
- Cloud resources scale to 10+ agents
- Monitor system resources when running 5+ parallel processes
- Platform requirement: Unix-like systems (macOS/Linux/WSL) for background process management
