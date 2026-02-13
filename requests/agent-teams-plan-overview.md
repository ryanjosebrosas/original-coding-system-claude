# Plan Overview: Agent Teams Integration with PIV-Phased Control & TMUX

<!-- PLAN-SERIES -->

> **This is a decomposed plan overview.** It coordinates multiple sub-plans that together
> implement a complex feature. Each sub-plan is self-contained and executable in a fresh
> conversation. Do NOT implement from this file — use `/execute` on each sub-plan in order.
>
> **Total Sub-Plans**: 3
> **Total Estimated Tasks**: 19

---

## Feature Description

Integrate Claude Code's experimental Agent Teams feature into My Coding System as the primary multi-agent orchestration layer. This creates a new `/team` command that runs a full PIV Loop using coordinated Agent Teams — with PIV-phased control (Coordinator mode for planning, Delegate-only mode for implementation, Synthesizer mode for validation). Implementation teammates automatically get worktrees for file isolation, and all task management flows through Archon as the source of truth. TMUX split-pane display is enabled via WSL for visibility.

## User Story

As a developer using My Coding System, I want to orchestrate multiple Claude Code instances as a coordinated team with PIV-phased control, so that complex features get parallel research, parallel implementation (with worktree isolation), and parallel review — all managed through a single `/team` command.

## Problem Statement

The current system has three parallel execution approaches that don't communicate with each other:
1. **Subagents** — parallel research, but results only flow back to the main agent (no inter-agent discussion)
2. **Worktrees + `claude -p`** — parallel implementation, but headless processes with no coordination
3. **Archon tasks** — tracking, but disconnected from the parallel execution layer

Agent Teams fills the gap: agents that can message each other, share a task list, self-coordinate, and debate findings — while still leveraging worktrees for file isolation and Archon for task tracking.

## Solution Statement

- Decision 1: **Full integration** (not additive tier) — because Agent Teams supersedes headless `claude -p` processes with a richer coordination model. Subagents remain for quick, focused tasks within a single session.
- Decision 2: **New `/team` command** (not modifying existing commands) — because existing commands stay stable while `/team` wraps the orchestration layer. Users opt in explicitly.
- Decision 3: **PIV-phased control** — because different PIV phases need different lead behaviors. Planning = coordinator (guide research). Implementation = delegate-only (never code, only assign). Validation = synthesizer (aggregate reviews).
- Decision 4: **Auto-worktree per implementation teammate** — because file conflicts are eliminated by design. Each teammate gets their own worktree and branch.
- Decision 5: **Archon is source of truth** — because the Agent Teams built-in task list is ephemeral (session-scoped). Archon persists across sessions and provides RAG search.
- Decision 6: **WSL + tmux** for split-pane display — because Windows doesn't support tmux natively, and split panes give visibility into all teammates simultaneously.

## Feature Metadata

- **Feature Type**: New Capability
- **Estimated Complexity**: High
- **Plan Mode**: Decomposed (3 sub-plans)
- **Primary Systems Affected**: Commands (`.claude/commands/`), Reference guides (`reference/`), Settings, Skills (`.claude/skills/`), Templates (`templates/`)
- **Dependencies**: Claude Code Agent Teams (experimental), WSL, tmux, Archon MCP

---

## CONTEXT REFERENCES

> Shared context that ALL sub-plans need. Each sub-plan also has its own
> per-phase context section. The execution agent reads BOTH this section
> and the sub-plan's context before implementing.

### Relevant Codebase Files

> IMPORTANT: The execution agent MUST read these files before implementing any sub-plan!

- `.claude/commands/parallel-e2e.md` — Why: current parallel execution command that Agent Teams evolves beyond. Mirror its structure and error handling patterns.
- `.claude/commands/new-worktree.md` — Why: worktree creation logic that `/team` will embed for implementation teammates
- `.claude/commands/end-to-end-feature.md` — Why: single-feature PIV loop pattern that `/team` extends to multi-agent
- `reference/subagents-overview.md` — Why: existing parallel execution documentation that needs Agent Teams added
- `reference/git-worktrees-overview.md` — Why: worktree documentation that needs Agent Teams integration noted
- `memory.md` — Why: will be updated with Agent Teams decisions

### New Files to Create (All Sub-Plans)

- `reference/agent-teams-overview.md` — Reference guide for Agent Teams integration — Sub-plan: 01
- `.claude/commands/team.md` — The `/team` slash command — Sub-plan: 02
- `templates/TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for each PIV phase — Sub-plan: 02
- `.claude/skills/agent-teams/SKILL.md` — Agent Teams skill entry point — Sub-plan: 03
- `.claude/skills/agent-teams/references/piv-phased-control.md` — PIV-phased control deep dive — Sub-plan: 03
- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — WSL + tmux setup guide — Sub-plan: 01

### Related Memories (from memory.md)

- Memory: Plan decomposition for complex features — Relevance: this feature uses decomposed plans, confirming the pattern works
- Memory: Modular CLAUDE.md with on-demand loading — Relevance: Agent Teams docs follow same pattern (overview auto-loaded, reference on-demand)
- Memory: Adopted 3-tier skills architecture — Relevance: Agent Teams skill follows SKILL.md → references/ pattern

### Relevant Documentation

- [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams)
  - Specific sections: All — architecture, display modes, permissions, task list, hooks
  - Why: primary source for Agent Teams capabilities and configuration
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
  - Specific section: TeammateIdle, TaskCompleted
  - Why: quality gate enforcement for teammates
- [Building a C Compiler with Parallel Claude Agents](https://www.anthropic.com/engineering/building-c-compiler)
  - Nicholas Carlini ran 16 parallel Claude instances autonomously building a 100K-line C compiler
  - Why: battle-tested patterns for multi-agent coordination at scale

### Lessons from Carlini's Parallel Agent Architecture

> These lessons from running 16 autonomous Claude instances inform our Agent Teams design.

1. **Extremely high-quality tests as the verifier** — "Claude will solve whatever problem I give it. So the task verifier must be nearly perfect, otherwise Claude solves the wrong problem." Our `/team` command must enforce validation gates (TaskCompleted hooks) to prevent teammates from marking tasks done incorrectly.

2. **Design for Claude, not humans** — Minimize context window pollution. Log details to files agents can grep. Pre-compute aggregate stats. Our spawn prompts should tell teammates to write findings to files, not return massive inline results.

3. **Specialized agent roles** — Beyond core development, Carlini used dedicated agents for: code deduplication, performance optimization, code quality review, documentation. Our PIV-phased approach mirrors this: research specialists, implementation specialists, review specialists.

4. **File lock-based task claiming** — Agents claim work via lock files to prevent duplicates. Agent Teams has built-in task claiming with file locking — we get this for free.

5. **Time blindness mitigation** — Claude "can't tell time and will happily spend hours running tests." Include `--fast` flags and test sampling. Our `/team` command should set `--max-turns` limits on teammates and include time-awareness prompts.

6. **Logging architecture** — Agents need comprehensive logs to self-orient in fresh contexts. Our teammates should write progress to `logs/team-{feature}/` directory for debugging and lead visibility.

7. **Progress documentation** — Frequently updated README/progress docs help agents orient. Our Archon task sync serves this purpose — teammates can query Archon for current project state.

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
- Why this pattern: all commands follow this frontmatter + stepped structure
- Common gotchas: `allowed-tools` must include all tools the command uses; missing tools causes permission prompts

**Reference Guide Structure** (from `reference/subagents-overview.md`):
```markdown
### Section Title

Content organized with tables, code blocks, and clear headings.
Ends with ### Reference Files section pointing to deeper guides.
```
- Why this pattern: reference guides are on-demand loaded, so they must be self-contained
- Common gotchas: don't auto-load reference guides — they're pulled by commands when needed

**Skill 3-Tier Structure** (from `.claude/skills/planning-methodology/`):
```
.claude/skills/{name}/
  SKILL.md          — Tier 1: overview (auto-loaded when skill invoked)
  references/
    {detail}.md     — Tier 3: deep guides (loaded on-demand)
```
- Why this pattern: progressive disclosure minimizes token usage
- Common gotchas: SKILL.md should be concise (<200 lines), deep content goes in references/

---

## PLAN INDEX

| # | Phase | Sub-Plan File | Tasks | Context Load |
|---|-------|---------------|-------|--------------|
| 01 | Infrastructure & Documentation | `requests/agent-teams-plan-01-infrastructure.md` | 6 | Low |
| 02 | /team Command & Templates | `requests/agent-teams-plan-02-team-command.md` | 7 | Medium |
| 03 | Integration & System Updates | `requests/agent-teams-plan-03-integration.md` | 6 | Low |

> Each sub-plan targets 5-8 tasks and 150-250 lines. Context load estimates
> help decide instance assignment (Low = minimal codebase reads, Medium = several files).

---

## EXECUTION ROUTING

### Instance Assignment

| Sub-Plan | Instance | Model | Notes |
|----------|----------|-------|-------|
| 01 | claude1 | Sonnet | Primary execution instance |
| 02 | claude2 | Sonnet | Secondary — heaviest sub-plan |
| 03 | claude1 | Sonnet | Back to primary |

### Fallback Chain

```
Primary:   claude1 (Sonnet) — main execution instance
Secondary: claude2 (Sonnet) — if primary hits rate limit
Fallback:  claude3 (Sonnet) — last resort
```

### Execution Instructions

**Manual execution** (recommended for this feature):
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

- [ ] `/team [feature]` command exists and follows system command patterns
- [ ] PIV-phased control documented: Coordinator → Delegate → Synthesizer
- [ ] Auto-worktree creation integrated into implementation phase
- [ ] Archon task sync documented and integrated into `/team` flow
- [ ] WSL + tmux setup guide exists with step-by-step instructions
- [ ] Reference guide `reference/agent-teams-overview.md` covers full architecture
- [ ] Agent Teams skill follows 3-tier pattern (SKILL.md + references/)
- [ ] Existing docs updated: `reference/subagents-overview.md`, `reference/git-worktrees-overview.md`
- [ ] Spawn prompt templates exist for all 3 PIV phases
- [ ] `memory.md` updated with Agent Teams decisions
- [ ] Trust progression updated to include Agent Teams tier
- [ ] Settings configuration documented (experimental flag, teammateMode)

---

## COMPLETION CHECKLIST

- [ ] Sub-plan 01 (Infrastructure & Documentation) — complete
- [ ] Sub-plan 02 (/team Command & Templates) — complete
- [ ] Sub-plan 03 (Integration & System Updates) — complete
- [ ] All acceptance criteria met
- [ ] Feature-wide manual validation passed
- [ ] Ready for `/commit`

---

## NOTES

### Key Design Decisions
- **Decomposed into 3 sub-plans** because the feature spans infrastructure (settings, TMUX), a new command (the core deliverable), and integration (Archon, hooks, system updates) — three distinct concerns
- **Sub-plan 02 is the heaviest** because the `/team` command is the centerpiece and needs the most careful design — it orchestrates all three PIV phases with different lead modes
- **WSL + tmux in sub-plan 01** (not 02) because it's infrastructure that must exist before the command can reference it

### Risks
- **Agent Teams is experimental** — API may change. Mitigation: document current API, note experimental status prominently, design for easy updates
- **Windows + WSL + tmux complexity** — multiple layers of indirection. Mitigation: detailed setup guide with troubleshooting, in-process mode as fallback
- **Archon sync is conceptual** — Agent Teams doesn't have native Archon integration. Mitigation: the `/team` command handles sync logic (pull tasks at start, push status at end), not a deep integration

### Confidence Score: 8/10
- **Strengths**: clear architecture from vibe planning, well-defined PIV phases, strong existing patterns to follow (commands, skills, reference guides)
- **Uncertainties**: Agent Teams experimental status may introduce breaking changes; WSL+tmux on Windows may have edge cases; Archon sync is manual (command-level, not automatic)
- **Mitigations**: in-process mode fallback for tmux issues; Archon sync is a clearly defined step in the command; all docs note experimental status
