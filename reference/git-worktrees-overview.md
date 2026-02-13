### Extending the PIV Loop with Parallel Implementation

Git worktrees enable parallel feature development by providing isolated working directories for each branch. Unlike subagents (which provide context isolation), worktrees provide **code isolation** — completely separate file systems where multiple coding agents can work simultaneously without conflicts.

### What Git Worktrees Are

- Isolated working directories for different branches in the same repository
- Each worktree has its own `.git` file pointing to the main repository
- Multiple Claude Code instances can run simultaneously, each in its own worktree
- Full isolation: no risk of one agent's changes affecting another's work
- Lives in `worktrees/` directory (convention from the worktrees guide)

Git worktrees are built into Git — not a third-party tool. They enable the same workflow as cloning a repo multiple times, but without duplicating the entire Git history.

### Parallelization Patterns

| Approach | Setup Complexity | Isolation | Speed Gain | Use Case |
|----------|------------------|-----------|------------|----------|
| **Subagents** | Low | Context only | 2-5x | Research, analysis, code review |
| **Multiple terminals** | Low | None | 2x | Quick parallel tasks on same branch |
| **Git worktrees** | Medium | Full (code-level) | 2-10x | **Feature implementation** |
| **Agent Teams + Worktrees** | Medium | Full (code + coordination) | 3-10x | **Coordinated parallel implementation** |
| **Containers/Cloud** | High | Complete | Unlimited | Large-scale parallel work, CI/CD |

**Key difference**: Subagents (see `reference/subagents-deep-dive.md`) parallelize **research and analysis**. Worktrees (see `reference/git-worktrees-parallel.md`) parallelize **implementation and code changes**. Agent Teams can automatically create worktrees for implementation teammates, combining coordination (shared task list, messaging) with isolation (separate file systems). See `reference/agent-teams-overview.md` and the `/team` command.

### When to Use Git Worktrees

**Use worktrees when:**
- Implementing multiple features simultaneously
- Features are isolated (vertical slice architecture)
- You want to maximize agent utilization
- Each feature takes 30+ minutes to implement
- Features touch different parts of the codebase
- Using `/team` command for coordinated multi-agent implementation (worktrees created automatically)

**Don't use worktrees when:**
- Quick bug fixes (same branch is fine)
- Features aren't isolated (high merge conflict risk)
- Single-feature focus (no parallelization needed)
- Testing/debugging existing code (use same branch)

**The architecture requirement**: Parallel implementation works best with **vertical slice architecture** — features isolated into independent modules. One agent works on `features/search/`, another on `features/export/` — minimal risk of conflicts.

### Worktree Workflow

#### 1. Setup Worktrees

Use `/new-worktree` command:

```bash
# Single worktree
/new-worktree feature/search

# Two parallel worktrees
/new-worktree feature/search feature/export

# Multiple parallel worktrees (up to 10)
/new-worktree feature/search feature/export feature/analytics feature/notifications
```

This creates:
- One worktree per branch in `worktrees/` directory
- Each with synced dependencies and verified health
- Dedicated ports: 8124, 8125, 8126, ... (formula: 8124 + index)

#### 2. Execute in Parallel

Open separate terminals for each worktree:

**Terminal 1:**
```bash
cd worktrees/feature-search
claude
/execute .agents/plans/search-feature-plan.md
```

**Terminal 2:**
```bash
cd worktrees/feature-export
claude
/execute .agents/plans/export-feature-plan.md
```

Both agents work simultaneously without conflicts.

#### 3. Merge Back

Use `/merge-worktrees` command from main repository:

```bash
# Merge 2 branches
/merge-worktrees feature/search feature/export

# Merge N branches (up to 10)
/merge-worktrees feature/search feature/export feature/analytics feature/notifications
```

This:
1. Creates temporary integration branch
2. For each branch: merges with `--no-ff`, then runs tests (fail fast)
3. Runs full validation suite after all merges (tests + type checks)
4. Merges to original branch only if ALL validation passes
5. Cleans up integration branch
6. Asks user about worktree cleanup (via AskUserQuestion)

**Safety**: If any step fails, the workflow provides rollback instructions and stops. Your main branch stays clean.

### Best Practices

**Dependency Management:**
- Each worktree has independent dependencies (`node_modules/`, `venv/`, `.uv/`)
- Run `uv sync` (or `npm install`, `pip install`) in each worktree
- Keep dependency versions aligned across worktrees

**Port Allocation:**
- Formula: Port = 8124 + index (0-based)
- Worktree 1: 8124, Worktree 2: 8125, ..., Worktree N: 8124 + (N-1)
- Supports up to 10 worktrees (ports 8124-8133)
- Document port assignments in your project

**Cleanup:**
- Remove worktrees after merging: `git worktree remove worktrees/branch-name`
- Delete merged branches: `git branch -d feature/branch-name`
- Never manually delete worktree directories (use `git worktree remove`)

**Commit Hygiene:**
- Keep commits separate per feature for easy review
- Test features in isolation before merging
- Use `--no-ff` (no fast-forward) to preserve feature branch history

**Project-Specific Customization:**
- The `/new-worktree` and `/merge-worktrees` commands are templates
- Customize dependency commands (`uv` → `npm`, `pip`, etc.)
- Customize validation commands (`pytest` → `jest`, `vitest`, etc.)
- Customize port allocation for your services

### Conflict Prevention (Parallel Agent Safety)

Git worktrees provide **code isolation** — agents in different worktrees cannot see or modify each other's files. However, conflicts can still emerge at merge time. These patterns prevent and manage conflicts.

**The Scope Boundary Principle:**
Each parallel agent should have a clear, non-overlapping scope:
- Agent 1 OWNS `features/search/` — can create and modify files here
- Agent 2 OWNS `features/export/` — can create and modify files here
- NEITHER agent modifies shared files (routes, configs, registries) during implementation

This works naturally with vertical slice architecture. When planning parallel features, verify each feature's plan only touches files within its own slice. If two plans modify the same file — don't parallelize those features.

**Shared File Strategy (Registration Points):**
When multiple features need to add entries to a shared file (e.g., adding routes to `routes/index.ts`, registering tools in `main.py`):
- During implementation: agents do NOT modify the shared file
- During merge: the merge step handles registration conflicts
- Typical conflict: two features both add a line to the same file — Git auto-merges if additions are in different locations; manual resolution needed if at the same line
- Best practice: design registration points to be append-friendly (each feature adds at the end, reducing positional conflicts)

**Research Agent Deduplication:**
When running parallel research agents (e.g., in `/planning`), partition work by scope:
- Codebase agents: each assigned to different directories or file patterns
- External agents: each assigned to different documentation sources or topics
- Prevents duplicate findings and wasted context window from redundant results

**Detecting Overlap Before Parallelizing:**
Before creating parallel worktrees, verify feature isolation:
1. Review each feature's plan — list all files that will be created or modified
2. Check for intersection — if two plans modify the same files, they overlap
3. Overlapping features should be implemented sequentially, not in parallel
4. Exception: shared registration points (routes, configs) are expected and handled at merge time

### Command Summary

**`/new-worktree [branch1] [branch2] ... [branchN]`**
- Create 1-10 worktrees with dependency sync and health check
- Single mode: Sequential setup for one worktree
- Parallel mode: Launch N agents via Task tool (when 2+ branches provided, max 10)
- Each agent sets up worktree independently with dedicated port (8124 + index)

**`/merge-worktrees [branch1] [branch2] ... [branchN]`**
- Safely merge 2-10 feature branches with validation gates
- Creates temporary integration branch for testing
- Merges sequentially: merge branch → test → merge next → test → ... → final validation
- Only updates main branch after ALL validation passes
- Provides rollback instructions on failure

**`/parallel-e2e [feature A | feature B | ...]`**
- Full PIV Loop for 2-10 features in parallel
- Chains: prime → plan all (sequential) → create worktrees → execute via `claude -p` (parallel) → merge → commit → PR
- Requires: `claude` CLI with `-p` support, `jq`, proven `/end-to-end-feature` + `/new-worktree` + `/merge-worktrees`

Full specifications: See the worktree command files in `.claude/commands/`

### Trust Progression (Complete)

```
Manual → Commands → Chained → Subagents → Worktrees → Parallel Chained → Remote
  ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑
```

**Before using worktrees**: Your `/execute` command works reliably on single features. You've run 5+ features sequentially with consistent results. Your validation strategy catches issues before commit.

**When to parallelize**: You have established patterns (documented standards, vertical slices, reusable plans). You trust validation automation. You can verify manually for critical paths.

Don't skip stages. Parallel implementation amplifies both good patterns and bad ones.

### Worktrees vs Remote System

Two approaches to parallel implementation:

- **Git Worktrees** — Local parallel execution. Multiple terminals on your machine. Full control, immediate feedback, works offline.
- **Remote Agentic System** (see `reference/remote-agentic-system.md`) — Cloud parallel execution. GitHub Issues trigger agents remotely. Scales to 10+ simultaneous agents, always available, platform-agnostic.

**Choosing between them:**
- **Local worktrees**: Development phase, iterative work, need immediate feedback
- **Remote system**: Production workflows, high parallelization (5+ features), team collaboration

Both use the same PIV Loop methodology. Both require vertical slice architecture. Worktrees are simpler to start; remote scales further.

### Reference Files

- `reference/git-worktrees-parallel.md` — Deep-dive guide: parallelization patterns, vertical slices, industry direction
- `.claude/commands/new-worktree.md` — Worktree creation command
- `.claude/commands/merge-worktrees.md` — Merge validation command
- Load when: setting up parallel implementation, customizing worktree commands, troubleshooting merge conflicts
