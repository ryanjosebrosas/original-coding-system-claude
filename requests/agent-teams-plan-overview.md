# Plan Overview: Agent Teams Integration with Contract-First Spawning

<!-- PLAN-SERIES -->

> **This is a decomposed plan overview.** It coordinates multiple sub-plans that together
> implement a complex feature. Each sub-plan is self-contained and executable in a fresh
> conversation. Do NOT implement from this file — use `/execute` on each sub-plan in order.
>
> **Total Sub-Plans**: 3
> **Total Estimated Tasks**: 16

---

## Feature Description

Integrate Claude Code's experimental Agent Teams feature into My Coding System as the primary multi-agent implementation layer. Creates a new `/team` command that orchestrates coordinated Claude Code instances using **contract-first spawning** — upstream agents publish interface contracts before downstream agents begin, and the lead relays and verifies contracts between teammates. Each implementation teammate gets a worktree for file isolation. Research stays with subagents (cheaper, focused). Validation is built into the team workflow (each agent self-validates + lead does end-to-end checks).

## User Story

As a developer using My Coding System, I want to orchestrate multiple Claude Code instances as a coordinated implementation team using contract-first spawning and delegate mode, so that complex features get parallel implementation with automatic interface alignment, worktree isolation, and a single `/team` command.

## Problem Statement

The current system has parallel execution approaches that don't coordinate on interfaces:
1. **Subagents** — parallel research, but results only flow back to the main agent (no inter-agent discussion)
2. **Worktrees + `claude -p`** — parallel implementation, but headless processes with no coordination — agents diverge on interfaces (e.g., backend builds against wrong DB schema)
3. **Archon tasks** — tracking, but disconnected from the parallel execution layer

Agent Teams fills the gap: agents that can message each other, share a task list, and self-coordinate — but only when guided with contract-first spawning to prevent the interface divergence problem.

## Solution Statement

- Decision 1: **Implementation-focused** — Agent Teams for coordinated implementation, subagents for research (per Cole Medin's guidance: "subagents for research, Agent Teams for implementation"). This is more token-efficient than using Agent Teams for everything.
- Decision 2: **Contract-first spawning** (core pattern) — Upstream agents spawn first, publish interface contracts (DB schema, API shapes), lead relays verified contracts to downstream agents BEFORE they start coding. Prevents the #1 failure mode: agents building against wrong interfaces.
- Decision 3: **Delegate mode** — Lead uses Shift+Tab to enter delegate mode. Never codes directly, only coordinates, relays contracts, and validates. One mode, not three invented ones.
- Decision 4: **Auto-worktree per teammate** — File conflicts eliminated by design. Each teammate gets their own worktree and branch.
- Decision 5: **Dynamic team sizing** — 2 agents for simple splits, 3 for full-stack, 4 for complex systems, 5+ for large independent modules. Determined from the plan, not fixed.
- Decision 6: **Archon summary sync** — Update Archon once at end of session (not real-time per-task sync). Agent Teams' built-in task list handles in-session coordination.
- Decision 7: **WSL + tmux** for split-pane display — Windows users need WSL. In-process mode as universal fallback.

## Feature Metadata

- **Feature Type**: New Capability
- **Estimated Complexity**: High
- **Plan Mode**: Decomposed (3 sub-plans)
- **Primary Systems Affected**: Commands (`.claude/commands/`), Reference guides (`reference/`), Skills (`.claude/skills/`), Templates (`templates/`)
- **Dependencies**: Claude Code Agent Teams (experimental), WSL, tmux

---

## CONTEXT REFERENCES

> Shared context that ALL sub-plans need. Each sub-plan also has its own
> per-phase context section. The execution agent reads BOTH this section
> and the sub-plan's context before implementing.

### Relevant Codebase Files

> IMPORTANT: The execution agent MUST read these files before implementing any sub-plan!

- `.claude/commands/parallel-e2e.md` — Why: current parallel execution command. Mirror its structure and error handling patterns.
- `.claude/commands/new-worktree.md` — Why: worktree creation logic that `/team` will embed for teammates
- `.claude/commands/end-to-end-feature.md` — Why: single-feature PIV loop pattern that `/team` extends to multi-agent
- `reference/subagents-overview.md` — Why: existing parallel execution docs that need Agent Teams comparison added
- `reference/git-worktrees-overview.md` — Why: worktree docs that need Agent Teams integration noted
- `memory.md` — Why: will be updated with Agent Teams decisions

### External Reference: Cole Medin's Agent Teams Skill

> This is the primary reference implementation. Our `/team` command adapts his patterns for our system.

**Key patterns from Cole's `build-with-agent-team` skill:**

1. **Contract-First Spawning** — The core innovation:
   - Identify the contract chain: `Database → publishes function signatures → Backend → publishes API contract → Frontend`
   - Spawn upstream agents first (staggered, not all parallel)
   - Lead acts as **active contract relay** — receives, verifies, and forwards contracts. Never tell agents to "share with each other" directly.
   - Agents publish contracts BEFORE implementing — contract must be verified before downstream agents spawn

2. **Spawn Prompt Structure** — Each teammate prompt includes:
   - **Ownership**: files they own, files they must NOT touch
   - **What they're building**: specific scope
   - **Mandatory communication**: contract publishing before implementation
   - **Contract conformity**: the verified contract they must build against
   - **Cross-cutting concerns**: shared conventions (URL patterns, error shapes, etc.)

3. **5-Phase Collaboration Flow**:
   - Phase 1: Contracts (sequential, lead-orchestrated)
   - Phase 2: Implementation (parallel where safe)
   - Phase 3: Pre-completion contract verification (lead runs contract diff)
   - Phase 4: Polish (cross-review between agents)
   - Phase 5: Lead end-to-end validation

4. **Team Sizing**:
   - 2 agents: Simple frontend/backend split
   - 3 agents: Full-stack (frontend, backend, database/infra)
   - 4 agents: Complex systems with testing, DevOps, docs
   - 5+ agents: Large systems with many independent modules

5. **Anti-Patterns** (from Cole's testing):
   - Don't spawn all agents simultaneously — upstream must publish contracts first
   - Don't tell agents to "share with each other" — lead must relay and verify
   - Don't skip contract verification — leads to interface divergence
   - Don't use Agent Teams for research — subagents are cheaper and sufficient

### Lessons from Carlini's Parallel Agent Architecture

> These lessons from running 16 autonomous Claude instances inform our design.

1. **High-quality validation as verifier** — "Claude will solve whatever problem I give it. So the task verifier must be nearly perfect." Each agent must self-validate before reporting done.
2. **Design for Claude, not humans** — Log details to files. Spawn prompts should instruct: "Write findings to files, send concise summaries via messages."
3. **File lock-based task claiming** — Agent Teams has built-in task claiming — we get this for free.
4. **Time blindness mitigation** — Include turn limits in spawn prompts: "If you've been working for more than 30 turns without progress, report blockers to the lead."
5. **Logging architecture** — Teammates write progress to `logs/team-{feature}/` directory for debugging.

### New Files to Create (All Sub-Plans)

- `reference/agent-teams-overview.md` — Reference guide for Agent Teams integration — Sub-plan: 01
- `.claude/skills/agent-teams/SKILL.md` — Agent Teams skill entry point — Sub-plan: 01
- `.claude/skills/agent-teams/references/contract-first-spawning.md` — Contract-first spawning deep dive — Sub-plan: 01
- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — WSL + tmux setup guide — Sub-plan: 01
- `.claude/commands/team.md` — The `/team` slash command — Sub-plan: 02
- `templates/TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for contract-first pattern — Sub-plan: 02

### Related Memories (from memory.md)

- Memory: Plan decomposition for complex features — Relevance: this feature uses decomposed plans
- Memory: Modular CLAUDE.md with on-demand loading — Relevance: Agent Teams docs follow same pattern
- Memory: Adopted 3-tier skills architecture — Relevance: Agent Teams skill follows SKILL.md → references/ pattern

### Patterns to Follow

**Command Structure** (from `.claude/commands/parallel-e2e.md`):
```markdown
---
description: Command description
argument-hint: [arguments]
allowed-tools: Tool1, Tool2, ...
---

# Command Title

**Feature Description**: $ARGUMENTS

## Step N: Step Name

{step details}

---
```
- Why: all commands follow this frontmatter + stepped structure
- Gotcha: `allowed-tools` must include all tools the command uses

**Reference Guide Structure** (from `reference/subagents-overview.md`):
- Self-contained, on-demand loaded
- Organized with tables, code blocks, clear headings
- Ends with Reference Files section

**Skill 3-Tier Structure** (from `.claude/skills/planning-methodology/`):
```
.claude/skills/{name}/
  SKILL.md          — Tier 1: overview (<120 lines)
  references/
    {detail}.md     — Tier 3: deep guides (on-demand)
```

---

## PLAN INDEX

| # | Phase | Sub-Plan File | Tasks | Context Load |
|---|-------|---------------|-------|--------------|
| 01 | Infrastructure & Documentation | `requests/agent-teams-plan-01-infrastructure.md` | 6 | Low |
| 02 | /team Command & Templates | `requests/agent-teams-plan-02-team-command.md` | 5 | Medium |
| 03 | Integration & System Updates | `requests/agent-teams-plan-03-integration.md` | 5 | Low |

> Each sub-plan targets 5-6 tasks. Context load estimates help decide instance assignment.

---

## EXECUTION ROUTING

### Instance Assignment

| Sub-Plan | Instance | Model | Notes |
|----------|----------|-------|-------|
| 01 | claude1 | Sonnet | Primary execution instance |
| 02 | claude2 | Sonnet | Secondary — heaviest sub-plan |
| 03 | claude1 | Sonnet | Back to primary |

### Execution Instructions

**Manual execution** (recommended):
```bash
# Sub-plan 1: Infrastructure
claude --model sonnet
> /execute requests/agent-teams-plan-01-infrastructure.md

# Sub-plan 2: /team Command (heaviest)
claude --model sonnet
> /execute requests/agent-teams-plan-02-team-command.md

# Sub-plan 3: Integration
claude --model sonnet
> /execute requests/agent-teams-plan-03-integration.md
```

**Between sub-plans**:
- Each sub-plan runs in a fresh conversation (context reset)
- Read HANDOFF NOTES from completed sub-plan before starting the next
- If a sub-plan fails, fix and re-run it before proceeding

---

## ACCEPTANCE CRITERIA

- [x] `/team [feature]` command exists and follows system command patterns
- [x] Contract-first spawning documented as the core orchestration pattern
- [x] Delegate mode documented (lead never codes, only coordinates)
- [x] Auto-worktree creation integrated into implementation phase
- [x] Dynamic team sizing guidance (2-5 agents based on plan complexity)
- [x] WSL + tmux setup guide exists with step-by-step instructions
- [x] Reference guide `reference/agent-teams-overview.md` covers full architecture
- [x] Agent Teams skill follows 3-tier pattern (SKILL.md + references/)
- [x] Existing docs updated: `reference/subagents-overview.md`, `reference/git-worktrees-overview.md`
- [x] Spawn prompt templates follow contract-first pattern with ownership boundaries
- [x] `memory.md` updated with Agent Teams decisions
- [x] Trust progression updated to include Agent Teams tier
- [x] Settings configuration documented (experimental flag, teammateMode)

---

## COMPLETION CHECKLIST

- [x] Sub-plan 01 (Infrastructure & Documentation) — complete
- [x] Sub-plan 02 (/team Command & Templates) — complete
- [x] Sub-plan 03 (Integration & System Updates) — complete
- [x] All acceptance criteria met
- [x] Feature-wide manual validation passed
- [x] Ready for `/commit`

---

## NOTES

### Key Design Decisions
- **Contract-first over PIV-phased control** — The original plan invented Coordinator/Delegate/Synthesizer modes that don't map to real Agent Teams features. Contract-first spawning (from Cole Medin's tested approach) solves the actual problem: interface divergence between parallel agents.
- **Implementation-only teams** — Agent Teams for research wastes tokens. Subagents are 2-4x cheaper for research tasks and provide sufficient output. Agent Teams' value is coordination during implementation.
- **Archon summary sync, not real-time** — Real-time Archon sync adds fragility and complexity. Agent Teams' built-in task list handles in-session coordination. Archon gets updated once at the end for cross-session persistence.

### Risks
- **Agent Teams is experimental** — API may change. Mitigation: document current API, note experimental status, design for easy updates
- **Windows + WSL + tmux complexity** — Mitigation: detailed setup guide with troubleshooting, in-process mode as fallback
- **Contract-first requires plan analysis** — Lead must identify the contract chain from the plan. Mitigation: clear heuristics in the command (DB → Backend → Frontend pattern)

### Confidence Score: 8/10
- **Strengths**: contract-first pattern is battle-tested by Cole Medin, simpler architecture than original plan, strong existing patterns to follow
- **Uncertainties**: Agent Teams experimental status; contract chain identification may be tricky for non-standard architectures
- **Mitigations**: spawn prompt templates cover common patterns; in-process mode fallback; team sizing guidance reduces guesswork
