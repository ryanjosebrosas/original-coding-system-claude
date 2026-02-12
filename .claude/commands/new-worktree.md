---
description: Create git worktrees with optional parallel setup
argument-hint: [branch1] [branch2] ... [branchN] (1-10 branches)
allowed-tools: Bash(git:*), Bash(cd:*), Bash(uv:*), Bash(curl:*), Bash(sleep:*), Bash(kill:*), Task, Read
---

# New Worktree

Quick worktree setup with health check verification. Supports parallel creation with up to 10 agents.

## Parameters

- **Branches**: $ARGUMENTS (1-10 branch names, space-separated)
- Examples:
  - Single: `/new-worktree feature/search`
  - Two: `/new-worktree feature/search feature/export`
  - Many: `/new-worktree feature/search feature/export feature/analytics feature/notifications`

## Logic

1. Parse $ARGUMENTS into a list of branch names
2. Count branches (N)
3. **If N = 1**: Create single worktree sequentially (Single Worktree Mode)
4. **If N >= 2 (max 10)**: Spawn N agents in parallel using Task tool (Parallel Worktrees Mode)
   - Each agent sets up their own worktree independently
   - Port allocation: branch at index i gets port `8124 + i` (0-based)
   - Combine results from all agents
5. **If N > 10**: Error — "Maximum 10 parallel worktrees supported (subagent limit)"

## Steps

### Single Worktree Mode (when 1 branch provided)

Execute these steps sequentially:

#### Step 1: Create Worktree

```bash
git worktree add worktrees/{branch} -b {branch}
```

#### Step 2: Navigate to Worktree

```bash
cd worktrees/{branch}
```

#### Step 3: Sync Dependencies

```bash
uv sync
```

**Note**: This uses `uv` as an example. Users customize this for their project:
- Node.js: `npm install` or `yarn install`
- Python: `pip install -r requirements.txt`
- Other: Project-specific dependency command

#### Step 4: Start Server in Background

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8124 &
SERVER_PID=$!
```

**Note**: Replace with your project's server command. Port 8124 is dedicated for the single worktree.

#### Step 5: Wait for Server to Be Ready

```bash
sleep 3
```

#### Step 6: Test Health Endpoint

```bash
curl -f http://localhost:8124/health || echo "Health check failed"
```

**Note**: Replace `/health` with your project's health endpoint. This verifies the worktree environment works.

#### Step 7: Kill Server

```bash
kill $SERVER_PID
```

**Critical**: Always kill background processes before completing. Prevents port conflicts.

#### Step 8: Return to Main Repository

```bash
cd ../..
```

#### Step 9: Report Success

Output:
```
✓ Worktree initialized
  Path: worktrees/{branch-name}
  Branch: {branch}

✓ Dependencies synced (uv sync)
✓ Health check passed (http://localhost:8124/health)
✓ Server stopped

Ready for development!

Next steps:
  cd worktrees/{branch-name}
  claude
  /execute .agents/plans/{feature}-plan.md
```

---

### Parallel Worktrees Mode (when 2+ branches provided)

Launch N Task agents simultaneously (max 10 concurrent).

#### Step 1: Parse Arguments and Allocate Ports

Parse $ARGUMENTS into a list of branches. For each branch at index i (0-based):
- Branch name: `branches[i]`
- Dedicated port: `8124 + i`
- Worktree path: `worktrees/<branch-name>`

Port allocation table (example with 4 branches):
| Index | Branch | Port |
|-------|--------|------|
| 0 | feature/search | 8124 |
| 1 | feature/export | 8125 |
| 2 | feature/analytics | 8126 |
| 3 | feature/notifications | 8127 |

#### Step 2: Launch Parallel Agents

For EACH branch, launch a Task agent with `subagent_type="Bash"` and `model: haiku`:

**Prompt template for Agent i:**
```
Set up worktree for branch: {branch_name}

Execute these steps in a SINGLE bash invocation:

1. Create worktree:
   git worktree add worktrees/{branch_name} -b {branch_name}

2. Navigate and sync:
   cd worktrees/{branch_name}
   uv sync

3. Start server in background:
   uv run uvicorn app.main:app --host 0.0.0.0 --port {8124 + i} &
   SERVER_PID=$!

4. Wait and test:
   sleep 3
   HEALTH_RESULT=$(curl -f http://localhost:{8124 + i}/health 2>&1 || echo "FAILED")

5. Kill server:
   kill $SERVER_PID 2>/dev/null || true

6. Return to main repo:
   cd ../..

Report (structured format):
- Worktree path: worktrees/{branch_name}
- Branch name: {branch_name}
- Port: {8124 + i}
- Dependencies: SYNCED
- Health check: [PASS/FAIL with details]
- Server: STOPPED

IMPORTANT: Execute ALL steps in ONE bash command using && and semicolons. Do not split across multiple bash calls.
```

**Execution**: Launch ALL agents in a single message (parallel Task tool calls). Each agent runs independently.

#### Step 3: Combine Results

After all agents complete, combine their outputs:

```
✓ N worktrees initialized in parallel

[For each agent, report:]
Agent {i+1} ({branch_name}):
  Path: worktrees/{branch_name}
  Branch: {branch_name}
  ✓ Dependencies synced
  ✓ Health check passed (port {8124 + i})
  ✓ Server stopped

All worktrees ready for parallel development!

⚠ CONFLICT PREVENTION REMINDER:
Each worktree is fully isolated. If features share registration points
(routes, configs), handle those during merge — NOT during implementation.

Next steps (run in separate terminals):

[For each worktree:]
Terminal {i+1}:
  cd worktrees/{branch_name}
  claude
  /execute .agents/plans/{feature}-plan.md
```

---

## Notes

**Project-Agnostic Template**: This command uses `uv` and `uvicorn` as examples. Users must customize for their project:
- Dependency sync: `uv sync` → `npm install`, `pip install`, `bundle install`, etc.
- Server start: `uvicorn` → `npm run dev`, `rails s`, `go run`, etc.
- Health endpoint: `/health` → your project's health check URL
- Port allocation: base port 8124 → your project's port convention

**Port Allocation Strategy**:
- Formula: Port = 8124 + index (0-based)
- Worktree 1: 8124, Worktree 2: 8125, ..., Worktree N: 8124 + (N-1)
- Supports up to 10 worktrees (ports 8124-8133)
- Predictable, simple, no conflicts between parallel worktrees
- Users can customize the base port for their environment

**Background Process Management**:
- Always capture `SERVER_PID=$!` immediately after starting server
- Always kill the server before completing (`kill $SERVER_PID`)
- Prevents zombie processes and port conflicts

**Bash Variable Scope**:
- Variables don't persist across separate Bash tool calls
- Solution: Execute all steps in ONE bash command (use `&&` and `;`)
- Agents use this pattern to maintain `SERVER_PID` and `HEALTH_RESULT`

**Health Check Purpose**:
- Verifies worktree environment is correctly configured
- Tests dependency sync worked (imports resolve)
- Catches environment issues early (missing config, port conflicts)
- Not a comprehensive test — just a smoke test

**Conflict Prevention (Parallel Agents)**:
- Each Task agent operates ONLY on its assigned worktree directory — no cross-worktree access
- Setup agents are inherently isolated: Agent i creates and configures `worktrees/{branch_i}` only
- Port allocation prevents network conflicts between parallel health checks
- If any agent fails, others continue independently — partial success is acceptable

**When Parallel Mode Fails**:
- If one agent fails, the others may still succeed
- Report shows which worktree(s) failed and why
- User can retry failed worktree individually (single mode)
- Partial success is acceptable — fix issues and continue
