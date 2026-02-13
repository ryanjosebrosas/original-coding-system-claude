# Sub-Plan 01: Infrastructure & Documentation

> **Parent Plan**: `requests/agent-teams-plan-overview.md`
> **Sub-Plan**: 01 of 3
> **Phase**: Infrastructure & Documentation
> **Tasks**: 6
> **Estimated Context Load**: Low

---

## Scope

This sub-plan implements **the foundational infrastructure for Agent Teams** — the reference guide (centered on contract-first spawning), the skill files, WSL+tmux setup guide, and updates to existing parallel execution docs. These must exist before the `/team` command (sub-plan 02) can reference them.

**What this sub-plan delivers**:
- Comprehensive reference guide covering architecture, contract-first spawning, and comparison tables
- Agent Teams skill (SKILL.md + contract-first spawning deep dive + tmux setup guide)
- Updated parallel execution comparison in existing docs

**Prerequisites from previous sub-plans**:
- None (first sub-plan)

---

## CONTEXT FOR THIS SUB-PLAN

### Files to Read Before Implementing

- `reference/subagents-overview.md` — Why: existing parallel execution docs, will mirror structure and add Agent Teams comparison
- `reference/git-worktrees-overview.md` (lines 1-60) — Why: parallelization comparison table that needs Agent Teams row
- `.claude/skills/planning-methodology/SKILL.md` — Why: skill structure pattern to mirror for Agent Teams skill

### Files Created by Previous Sub-Plans

> N/A — first sub-plan.

---

## STEP-BY-STEP TASKS

### CREATE `.claude/skills/agent-teams/references/tmux-wsl-setup.md`

- **IMPLEMENT**: Write a WSL + tmux setup guide with these sections:
  1. **Prerequisites** — Windows 10/11, WSL2 installed, a Linux distro (Ubuntu recommended)
  2. **Install tmux** — `sudo apt update && sudo apt install tmux` inside WSL
  3. **Configure Claude Code** — Add `teammateMode` to settings.json: `"teammateMode": "tmux"`. Add env var: `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"`. Can be set globally (`~/.claude/settings.json`) or per-project (`.claude/settings.local.json`).
  4. **Verify Installation** — `tmux -V` to check version, `tmux new-session -s test` to verify it works
  5. **Running Claude Code with tmux** — Start Claude Code from within WSL terminal. Launch tmux first, then run `claude` inside tmux. Split panes appear automatically when Agent Teams spawns teammates.
  6. **Fallback: In-Process Mode** — If tmux has issues, set `"teammateMode": "in-process"` or pass `--teammate-mode in-process`. Use Shift+Up/Down to navigate teammates. Press Ctrl+T to toggle task list.
  7. **Troubleshooting** — Common issues: tmux not found (PATH issue), panes not splitting (not running inside tmux), orphaned sessions (`tmux ls` + `tmux kill-session -t <name>`). Split-pane mode NOT supported in VS Code integrated terminal, Windows Terminal, or Ghostty.
  8. **iTerm2 Alternative** (for macOS users) — Install iTerm2, enable Python API in settings
- **PATTERN**: Follow structure of `reference/git-worktrees-parallel.md` — practical guide with code blocks and troubleshooting
- **GOTCHA**: tmux has known limitations on Windows — always note WSL requirement.
- **VALIDATE**: Verify file exists and contains all 8 sections listed above

### CREATE `reference/agent-teams-overview.md`

- **IMPLEMENT**: Write the primary reference guide (~200-250 lines) with these sections:
  1. **Opening paragraph** — "Extending the PIV Loop with Coordinated Multi-Agent Implementation" — similar tone to `reference/subagents-overview.md`
  2. **What Agent Teams Are** — Multiple Claude Code instances coordinated by a lead. Each teammate has own context window. Shared task list + mailbox for inter-agent messaging. Experimental feature (note prominently).
  3. **When to Use Agent Teams vs Subagents** — Rule of thumb from Cole Medin: "Subagents for research, Agent Teams for implementation." Subagents are 2-4x more token-efficient. Agent Teams add value when agents need to coordinate on shared interfaces.
     Comparison table:
     | Approach | Communication | Coordination | File Isolation | Token Cost | Best For |
     | Subagents | One-way (to main) | Main agent manages | None | Low | Research, focused tasks |
     | Agent Teams | Two-way (mailbox) | Shared task list | Via worktrees | 2-4x higher | Coordinated implementation |
     | Worktrees + `claude -p` | None | Manual | Full (git) | Low | Independent parallel tasks |
  4. **Contract-First Spawning** (core section) — The #1 failure mode is agents building against wrong interfaces. Solution:
     - Identify the contract chain from the plan (e.g., `DB → Backend → Frontend`)
     - Spawn upstream agents first (staggered, not all parallel)
     - Lead acts as **active contract relay** — receives, verifies, forwards contracts
     - Agents publish contracts BEFORE implementing
     - Anti-pattern: telling agents to "share with each other" — lead must relay
     Include a concrete example showing the flow for a 3-agent full-stack team.
  5. **Delegate Mode** — Lead enters delegate mode (Shift+Tab). Lead never codes, only coordinates. Lead's responsibilities: identify contract chain, spawn agents in order, relay contracts, monitor progress, validate at end.
  6. **Auto-Worktree Integration** — Each implementation teammate gets a worktree. Branch naming: `team/{feature}/{teammate-name}`. Lead creates worktrees before spawning. Merge happens after validation passes.
  7. **Team Sizing** — Dynamic based on plan complexity:
     | Agents | Use Case | Example |
     | 2 | Simple split | Frontend + backend |
     | 3 | Full-stack | Frontend + backend + database |
     | 4 | Complex | + testing/DevOps |
     | 5+ | Large systems | Many independent modules |
  8. **Spawn Prompt Structure** — Each teammate prompt must include: ownership (files they own / don't touch), scope (what they build), mandatory contract communication, contract to conform to, cross-cutting concerns.
  9. **5-Phase Collaboration Flow** — Contracts (sequential) → Implementation (parallel) → Pre-completion contract verification → Polish (cross-review) → Lead end-to-end validation.
  10. **Display Modes** — In-process (default, works everywhere) vs split-pane (tmux/iTerm2). Link to: `.claude/skills/agent-teams/references/tmux-wsl-setup.md`
  11. **Configuration** — Settings: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`, `teammateMode: "auto"|"in-process"|"tmux"`. Permissions: teammates inherit lead's permissions.
  12. **Token Usage Warning** — Agent Teams uses 2-4x more tokens than single sessions. Each teammate = separate Claude instance. Use subagents for research, Agent Teams only when coordination adds real value.
  13. **Trust Progression** — Updated:
      ```
      Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
      ```
  14. **Limitations** — No session resumption, one team per session (but can create/destroy teams within session), no nested teams, split panes require tmux/iTerm2, task status can lag
  15. **Reference Files** — Link to: `/team` command, contract-first spawning guide, tmux setup guide
- **PATTERN**: Mirror structure of `reference/subagents-overview.md` — starts with "Extending the PIV Loop with...", uses tables, ends with Reference Files
- **GOTCHA**: Keep to ~200-250 lines. On-demand reference guide, not auto-loaded.
- **VALIDATE**: Verify file exists, contains "Contract-First Spawning" as a major section, and is between 180-260 lines

### CREATE `.claude/skills/agent-teams/SKILL.md`

- **IMPLEMENT**: Write the Tier 1 skill entry point (~80-120 lines) with:
  1. **Title**: "Agent Teams — Coordinated Multi-Agent Implementation"
  2. **Overview**: One paragraph — Agent Teams enable multiple Claude Code instances to work in parallel, communicate, and coordinate on shared interfaces using contract-first spawning.
  3. **Quick Start**: How to use `/team [feature-description or plan-path]`
  4. **Core Pattern: Contract-First Spawning** — Brief summary:
     - Identify contract chain from plan (DB → Backend → Frontend)
     - Spawn upstream agents first
     - Lead relays verified contracts to downstream agents
     - All agents implement against verified contracts
  5. **Team Sizing** — Brief table (2/3/4/5+ agents)
  6. **Lead Behavior** — Delegate mode (Shift+Tab). Lead never codes. Coordinates, relays, validates.
  7. **Configuration**: Settings needed (experimental flag + teammateMode)
  8. **Prerequisites**: WSL + tmux (for split-pane), or in-process mode (no setup)
  9. **References section**: Links to deep guides in `references/` subdirectory
- **PATTERN**: Mirror `.claude/skills/planning-methodology/SKILL.md`
- **GOTCHA**: Keep under 120 lines. Auto-loaded entry point — details go in reference files.
- **VALIDATE**: Verify file exists and is under 120 lines

### CREATE `.claude/skills/agent-teams/references/contract-first-spawning.md`

- **IMPLEMENT**: Write the deep dive guide (~150-200 lines) covering:
  1. **The Problem: Interface Divergence** — When agents run in parallel without coordination, they build against wrong assumptions. Example: backend builds against wrong DB schema because DB agent hasn't finished yet. Cole Medin's experience: "the backend agent almost was done with its work" before getting the correct schema.
  2. **The Solution: Contract-First Spawning** — Upstream agents publish contracts first. Lead verifies and relays. Downstream agents don't start coding until they have a verified contract.
  3. **Identifying the Contract Chain** — How to analyze a plan and determine: What depends on what? Common patterns:
     - `Database → Backend → Frontend` (most web apps)
     - `Schema → API → UI` (data-driven apps)
     - `Core library → Consumers` (library projects)
     - `Shared types → Backend + Frontend` (parallel after shared contracts)
  4. **The Lead's Role: Active Contract Relay** — Lead responsibilities:
     - Analyze the plan to identify contract chain
     - Spawn the most-upstream agent first
     - Wait for contract publication (not full completion — just the contract)
     - Verify the contract for completeness and ambiguities
     - Forward verified contract to next downstream agent
     - Continue until all agents are spawned
     Anti-pattern: "Just share your API with the frontend agent" — lead must be the relay.
  5. **Spawn Prompt Template** — Detailed template with all 5 required sections:
     - Ownership (files they own, files they don't touch)
     - Scope (what they're building)
     - Mandatory communication (publish contract BEFORE implementing)
     - Contract to conform to (the upstream contract they must respect)
     - Cross-cutting concerns (shared conventions: URL patterns, error shapes, etc.)
  6. **5-Phase Collaboration Flow** — Detailed walkthrough:
     - Phase 1: Contracts (sequential, lead-orchestrated) — each upstream agent publishes, lead verifies, relays downstream
     - Phase 2: Implementation (parallel where safe) — agents code against verified contracts
     - Phase 3: Pre-completion contract verification — lead runs contract diff to catch drift
     - Phase 4: Polish (cross-review) — agents review each other's integration points
     - Phase 5: Lead end-to-end validation — final check that everything works together
  7. **Validation Within the Team** — Two levels:
     - Agent validation: each agent validates their domain before reporting done (runs tests, checks types)
     - Lead validation: end-to-end check after all agents complete
  8. **Cross-Cutting Concerns** — How to identify and assign shared concerns. Examples: URL conventions (trailing slashes), error response shapes, streaming protocols, authentication patterns. Use a table to assign ownership.
  9. **Example: 3-Agent Full-Stack Team** — Complete walkthrough showing contract chain identification, spawn order, contract relay flow, and validation.
- **PATTERN**: Follow structure of `.claude/skills/planning-methodology/references/6-phase-process.md`
- **GOTCHA**: Include actual spawn prompt examples. This is the most practically important file — developers will reference it when using `/team`.
- **VALIDATE**: Verify file exists and contains all 9 sections

### UPDATE `reference/subagents-overview.md`

- **IMPLEMENT**: Add Agent Teams comparison to existing parallel execution docs:
  1. After the "### Parallel Execution" section (~line 38), add "### Agent Teams (Coordinated Multi-Agent Implementation)" — brief explanation: Agent Teams enable two-way communication between agents via shared task list and mailbox. Key difference from subagents: collaboration vs isolation. Rule of thumb: subagents for research, Agent Teams for implementation.
  2. Update "### Trust Progression (Complete)" to include Agent Teams:
     ```
     Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
     ```
  3. Add a pointer to `reference/agent-teams-overview.md` for the full guide
- **PATTERN**: Match existing section style — concise paragraphs with tables
- **GOTCHA**: Don't restructure the existing file — only add new content (~20-30 lines).
- **VALIDATE**: Verify the file contains "Agent Teams" text and updated trust progression

### UPDATE `reference/git-worktrees-overview.md`

- **IMPLEMENT**: Add Agent Teams integration to worktree docs:
  1. In the "### Parallelization Patterns" table, add:
     | **Agent Teams + Worktrees** | Medium | Full (code + coordination) | 3-10x | **Coordinated parallel implementation** |
  2. After the table, add a paragraph: "Agent Teams can automatically create worktrees for implementation teammates, combining coordination (shared task list, messaging) with isolation (separate file systems). See `reference/agent-teams-overview.md` and the `/team` command."
  3. In the "### When to Use Git Worktrees" list, add: "Using `/team` command for coordinated multi-agent implementation (worktrees created automatically)"
- **PATTERN**: Match existing table and list formatting
- **GOTCHA**: Don't duplicate Agent Teams content — just pointers.
- **VALIDATE**: Verify the file contains "Agent Teams" in the parallelization table

---

## VALIDATION COMMANDS

### Syntax & Structure
```bash
# Verify all new files exist
test -f ".claude/skills/agent-teams/references/tmux-wsl-setup.md" && echo "OK" || echo "MISSING"
test -f "reference/agent-teams-overview.md" && echo "OK" || echo "MISSING"
test -f ".claude/skills/agent-teams/SKILL.md" && echo "OK" || echo "MISSING"
test -f ".claude/skills/agent-teams/references/contract-first-spawning.md" && echo "OK" || echo "MISSING"
```

### Content Verification
```bash
# Verify key content in reference guide
grep -l "Contract-First" reference/agent-teams-overview.md
grep -l "Trust Progression" reference/agent-teams-overview.md

# Verify updated files contain Agent Teams
grep -l "Agent Teams" reference/subagents-overview.md
grep -l "Agent Teams" reference/git-worktrees-overview.md
```

### Cross-Reference Check
```bash
# Verify skill references directory exists
test -d ".claude/skills/agent-teams/references/" && echo "OK" || echo "MISSING"

# Verify SKILL.md links to references
grep -l "references/" .claude/skills/agent-teams/SKILL.md
```

---

## SUB-PLAN CHECKLIST

- [x] All 6 tasks completed in order
- [x] Each task validation passed
- [x] All validation commands executed successfully
- [x] No broken references to other files

---

## HANDOFF NOTES

> What the NEXT sub-plan needs to know about what was done here.

### Files Created
- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — WSL + tmux installation guide, troubleshooting, fallback to in-process mode
- `reference/agent-teams-overview.md` — Primary reference guide covering architecture, contract-first spawning, team sizing, configuration, trust progression
- `.claude/skills/agent-teams/SKILL.md` — Tier 1 skill entry point with quick start, contract-first summary, team sizing, configuration
- `.claude/skills/agent-teams/references/contract-first-spawning.md` — Deep dive on contract chain identification, spawn order, lead as contract relay, 5-phase collaboration flow, spawn prompt template

### Files Modified
- `reference/subagents-overview.md` — Added Agent Teams comparison, updated trust progression
- `reference/git-worktrees-overview.md` — Added Agent Teams row to parallelization table

### Patterns Established
- **Contract-first spawning terminology**: contract chain, active contract relay, upstream/downstream agents, staggered spawning — sub-plan 02 uses these exact terms
- **Trust progression**: `Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote` — canonical progression
- **Team sizing**: 2/3/4/5+ — referenced by `/team` command

### State for Next Sub-Plan
- Reference guide at `reference/agent-teams-overview.md` — the `/team` command will link to this
- Contract-first spawning guide at `.claude/skills/agent-teams/references/contract-first-spawning.md` — the `/team` command references spawn prompt templates from this guide
- TMUX setup guide exists — the `/team` command can reference it
