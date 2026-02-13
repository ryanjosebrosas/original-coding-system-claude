# Worktree Workflow — Detailed Reference

> This reference is loaded on-demand during skill execution (Tier 3).

---

## Setup Phase

### Single Mode (`/new-worktree feature/search`)

Sequential steps for one worktree:

1. **Create worktree**: `git worktree add worktrees/{branch} -b {branch}`
2. **Navigate**: `cd worktrees/{branch}`
3. **Sync dependencies**: Run project-specific command (e.g., `uv sync`, `npm install`, `pip install`)
4. **Start server in background**: Launch on dedicated port (`8124`)
5. **Health check**: Verify the environment works (`curl -f http://localhost:8124/health`)
6. **Kill server**: Always clean up background processes
7. **Return to main repo**: `cd ../..`

### Parallel Mode (`/new-worktree branch1 branch2 ... branchN`)

When 2+ branches are provided (max 10):

1. **Parse arguments** into branch list with port allocation
2. **Launch N Task agents** simultaneously (`subagent_type="Bash"`, `model: haiku`)
3. **Each agent independently** creates its worktree, syncs dependencies, runs health check
4. **Port allocation**: Branch at index `i` gets port `8124 + i`
5. **Combine results** from all agents into summary table

| Index | Branch | Port | Path |
|-------|--------|------|------|
| 0 | feature/search | 8124 | worktrees/feature-search |
| 1 | feature/export | 8125 | worktrees/feature-export |

**If any agent fails**: Others continue independently. Report which failed, offer retry for individual worktrees.

### Project-Specific Customization

These commands are templates. Customize for your project:

| What | Example (Python) | Example (Node.js) | Example (Go) |
|------|-------------------|--------------------|----|
| Dependencies | `uv sync` | `npm install` | `go mod download` |
| Server | `uvicorn app.main:app` | `npm run dev` | `go run .` |
| Health check | `/health` | `/api/health` | `/healthz` |
| Base port | 8124 | 3000 | 8080 |

---

## Execution Phase

After worktrees are set up, open separate terminals for each:

**Terminal 1:**
```bash
cd worktrees/feature-search
claude
/execute requests/search-plan.md
```

**Terminal 2:**
```bash
cd worktrees/feature-export
claude
/execute requests/export-plan.md
```

**Key details:**
- Each worktree has its own CLAUDE.md, commands, and full context
- Agents are completely independent — they don't know about each other
- Plans must be placed inside the worktree directory before launching Claude Code
- Each agent commits to its own branch within the worktree

### Monitoring Progress

- Watch terminal output for each agent
- Use a terminal splitter (tmux, Ghostty split) for side-by-side monitoring
- Each agent will run validation commands from the plan before committing

---

## Merge Phase (`/merge-worktrees`)

### The 9-Step Gated Process

**Step 1: Verify Preconditions**
- Confirm running from main repository root (not inside `worktrees/`)
- Verify all branches exist: `git rev-parse --verify {branch}`
- Store current branch: `CURRENT_BRANCH=$(git branch --show-current)`
- Minimum 2 branches, maximum 10

**Step 2: Create Integration Branch**
```bash
git checkout -b integration-{first_branch}-to-{last_branch}
```
Testing happens on this temporary branch. Main branch stays clean.

**Step 3: Sequential Merge with Validation**

For each branch (in order provided):
```bash
git merge {branch_name} --no-ff -m "merge: integrate {branch_name}"
```
Then run tests immediately. If tests fail, stop and provide rollback instructions.

**Step 4: Full Validation Suite**

After all branches merged, run comprehensive validation:
- Test suite (e.g., `pytest -v`, `npm test`)
- Type checking (e.g., `mypy`, `tsc --noEmit`)
- Additional checks as needed (linting, security scans)

ALL validation must pass before continuing.

**Step 5: Merge to Original Branch**
```bash
git checkout $CURRENT_BRANCH
git merge integration-{first}-to-{last} --no-ff -m "merge: integrate features"
```

**Step 6: Cleanup Integration Branch**
```bash
git branch -d integration-{first}-to-{last}
```
Uses `-d` (safe delete) — Git prevents deletion if unmerged commits exist.

**Step 7: Worktree Cleanup (User Choice)**

Ask user: "Remove all worktrees and delete feature branches?"
- **Yes**: `git worktree remove worktrees/{branch}` + `git branch -d {branch}` for each
- **No**: Provide manual cleanup instructions

### Rollback Instructions (On Any Failure)

```bash
git checkout $CURRENT_BRANCH
git branch -D integration-{first}-to-{last}
```

This deletes the temporary branch, leaving your main branch untouched.

### Why `--no-ff` (No Fast-Forward)?

- Preserves feature branch history in the Git graph
- Makes it clear which commits belong to which feature
- Enables easier rollback (revert the merge commit)

### Why Test After Each Merge?

- Catches issues early (fail fast)
- If branch 3 breaks tests, no point merging branches 4-5
- Narrows down which feature caused the problem

---

## Cleanup Protocol

**Always use `git worktree remove`** — never manually delete worktree directories. Manual deletion leaves stale references in `.git/worktrees/` that cause errors.

Proper sequence:
1. `git worktree remove worktrees/{name}`
2. `git branch -d {branch}`
3. Verify: `git worktree list` should show only the main working tree
