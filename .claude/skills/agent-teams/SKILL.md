---
name: agent-teams
description: "Coordinated multi-agent implementation using Claude Code Agent Teams with contract-first spawning. Use when orchestrating multiple Claude Code instances for parallel implementation that requires interface coordination. Provides contract-first spawning methodology, team sizing, spawn prompt templates, and WSL+tmux setup."
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Write", "Edit", "Task", "AskUserQuestion"]
---

# Agent Teams — Coordinated Multi-Agent Implementation

Agent Teams enable multiple Claude Code instances to work in parallel, communicate via a shared task list and mailbox, and coordinate on shared interfaces using **contract-first spawning**. The lead agent orchestrates without coding — it identifies the contract chain, spawns agents in dependency order, and relays verified contracts between teammates.

## When This Skill Applies

- User wants to implement a feature using multiple coordinated agents
- A plan requires parallel implementation with shared interfaces (DB → API → frontend)
- User invokes `/team [feature]` command
- User asks about Agent Teams setup, configuration, or patterns

## Quick Start

1. Create a plan first: `/planning [feature-description]`
2. Run: `/team requests/{feature}-plan.md`
3. The lead analyzes the plan, identifies the contract chain, creates worktrees, and spawns agents

## Core Pattern: Contract-First Spawning

The #1 failure mode of parallel agents is **interface divergence** — agents building against wrong assumptions. Contract-first spawning prevents this:

1. **Identify contract chain** from the plan (e.g., `Database → Backend → Frontend`)
2. **Spawn upstream agent first** — instructs it to publish its contract (schema, types, function signatures) before implementing
3. **Lead verifies contract** — checks completeness, catches ambiguities
4. **Lead relays verified contract** to next downstream agent's spawn prompt
5. Repeat until all agents are spawned with verified contracts

Anti-pattern: telling agents to "share with each other." The lead must relay and verify all contracts.

## Team Sizing

| Agents | Use Case | Example |
|--------|----------|---------|
| 2 | Simple split | Frontend + backend |
| 3 | Full-stack | Frontend + backend + database |
| 4 | Complex system | + testing or DevOps |
| 5+ | Large systems | Many independent modules |

Determine from the plan's structure, not fixed upfront.

## Lead Behavior

- Enter **delegate mode** (Shift+Tab) — lead never codes directly
- Responsibilities: identify contract chain, spawn agents in order, relay contracts, monitor progress, validate at end
- If an agent diverges from its contract: intervene immediately

## Configuration

**Required** (in `~/.claude/settings.json` or `.claude/settings.local.json`):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "auto"
}
```

`teammateMode`: `"auto"` (detect), `"tmux"` (split panes in WSL), `"in-process"` (no setup), `"iterm2"` (macOS)

## Prerequisites

- **Split-pane mode**: WSL + tmux (see setup guide below)
- **In-process mode**: No additional setup (works everywhere)
- **Cost awareness**: Agent Teams uses 2-4x more tokens than single sessions

## Detailed References (Tier 3 — Load When Actively Using Agent Teams)

For contract-first spawning deep dive (contract chain identification, spawn order, 5-phase flow):
@references/contract-first-spawning.md

For WSL + tmux installation, troubleshooting, and fallback options:
@references/tmux-wsl-setup.md

## Related

- `/team [feature or plan-path]` — The command that orchestrates Agent Teams
- `reference/agent-teams-overview.md` — Full reference guide with architecture details
- `templates/TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for all agent types
- `reference/subagents-overview.md` — Comparison: subagents vs Agent Teams
