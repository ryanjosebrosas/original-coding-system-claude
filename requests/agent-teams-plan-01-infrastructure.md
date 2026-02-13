# Sub-Plan 01: Infrastructure & Documentation

> **Parent Plan**: `requests/agent-teams-plan-overview.md`
> **Sub-Plan**: 01 of 3
> **Phase**: Infrastructure & Documentation
> **Tasks**: 6
> **Estimated Context Load**: Low

---

## Scope

This sub-plan implements **the foundational infrastructure for Agent Teams** — settings configuration, WSL+tmux setup guide, and the primary reference guide. These must exist before the `/team` command (sub-plan 02) can reference them.

**What this sub-plan delivers**:
- Agent Teams experimental flag enabled in settings documentation
- WSL + tmux installation and configuration guide
- Comprehensive reference guide covering architecture, PIV-phased control, and comparison tables
- Updated parallel execution comparison tables

**Prerequisites from previous sub-plans**:
- None (first sub-plan)

---

## CONTEXT FOR THIS SUB-PLAN

> Only the files and docs relevant to THIS sub-plan's tasks. For shared context
> (patterns, documentation, memories), see the overview's CONTEXT REFERENCES section.

### Files to Read Before Implementing

- `reference/subagents-overview.md` — Why: existing parallel execution docs, will mirror structure and add Agent Teams comparison
- `reference/git-worktrees-overview.md` (lines 1-60) — Why: parallelization comparison table that needs Agent Teams row
- `reference/multi-model-strategy.md` — Why: model routing guidance that applies to Agent Teams (teammate model selection)
- `.claude/skills/planning-methodology/SKILL.md` — Why: skill structure pattern to mirror for Agent Teams skill

### Files Created by Previous Sub-Plans

> N/A — first sub-plan.

---

## STEP-BY-STEP TASKS

> Execute every task in order, top to bottom. Each task is atomic and independently testable.

### CREATE `.claude/skills/agent-teams/references/tmux-wsl-setup.md`

- **IMPLEMENT**: Write a comprehensive WSL + tmux setup guide with these sections:
  1. **Prerequisites** — Windows 10/11, WSL2 installed, a Linux distro (Ubuntu recommended)
  2. **Install tmux** — `sudo apt update && sudo apt install tmux` inside WSL
  3. **Configure Claude Code** — Add `teammateMode` to settings.json: `"teammateMode": "tmux"`. Add env var: `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"`
  4. **Verify Installation** — `tmux -V` to check version, `tmux new-session -s test` to verify it works
  5. **Running Claude Code with tmux** — Start Claude Code from within WSL terminal. Launch tmux first, then run `claude` inside tmux. Split panes appear automatically when Agent Teams spawn teammates.
  6. **Fallback: In-Process Mode** — If tmux has issues, set `"teammateMode": "in-process"` or pass `--teammate-mode in-process`. Use Shift+Up/Down to navigate teammates.
  7. **Troubleshooting** — Common issues: tmux not found (PATH issue), panes not splitting (not running inside tmux), orphaned sessions (`tmux ls` + `tmux kill-session -t <name>`)
  8. **iTerm2 Alternative** (for macOS users) — Install `it2` CLI, enable Python API in iTerm2 settings
- **PATTERN**: Follow structure of `reference/git-worktrees-parallel.md` — practical guide with code blocks and troubleshooting
- **IMPORTS**: N/A (markdown file)
- **GOTCHA**: tmux has known limitations on Windows — always note WSL requirement. Split-pane mode is NOT supported in VS Code integrated terminal, Windows Terminal, or Ghostty.
- **VALIDATE**: Verify file exists and contains all 8 sections listed above

### CREATE `reference/agent-teams-overview.md`

- **IMPLEMENT**: Write the primary reference guide (~200-250 lines) with these sections:
  1. **Opening paragraph** — "Extending the PIV Loop with Coordinated Multi-Agent Teams" — similar tone to `reference/subagents-overview.md` and `reference/git-worktrees-overview.md`
  2. **What Agent Teams Are** — Multiple Claude Code instances coordinated by a lead. Each teammate has own context window. Shared task list + mailbox for inter-agent messaging. Experimental feature (note prominently).
  3. **Agent Teams vs Subagents vs Worktrees** — Comparison table:
     | Approach | Context | Communication | Coordination | File Isolation | Best For |
     | Subagents | Own window, reports back | One-way (to main) | Main agent manages | None | Focused tasks |
     | Agent Teams | Own window, independent | Two-way (mailbox) | Shared task list | Via worktrees | Collaborative work |
     | Worktrees | Separate terminal | None | Manual | Full (git) | Parallel implementation |
  4. **PIV-Phased Control Model** — The core architecture:
     - **PLANNING phase**: Lead = Coordinator. Spawns research teammates. They explore codebase, external docs, competing approaches. Debate findings via mailbox. Lead synthesizes into structured plan.
     - **IMPLEMENTATION phase**: Lead = Delegate-only (Shift+Tab for delegate mode). Spawns implementation teammates, each with auto-worktree. Lead assigns tasks from Archon, coordinates only. Teammates self-claim unblocked tasks.
     - **VALIDATION phase**: Lead = Synthesizer. Spawns review teammates (security, performance, architecture, test coverage). Each reviewer checks all implementation work. Lead synthesizes findings into validation report.
  5. **Auto-Worktree Integration** — Each implementation teammate gets a worktree automatically. Branch naming: `team/{feature}/{teammate-name}`. Lead creates worktrees before spawning, includes worktree path in spawn prompt. Merge happens after validation passes.
  6. **Archon Task Sync** — Archon is the source of truth. Flow: Lead pulls tasks from Archon at start → creates Agent Teams task list → teammates claim and work → lead syncs status back to Archon at end. Agent Teams task list is ephemeral (session-scoped), Archon persists.
  7. **Display Modes** — In-process (default, works everywhere) vs split-pane (tmux/iTerm2, requires setup). Link to setup guide: `.claude/skills/agent-teams/references/tmux-wsl-setup.md`
  8. **Configuration** — Settings needed: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`, `teammateMode: "auto"|"in-process"|"tmux"`. Permissions: teammates inherit lead's permissions.
  9. **Token Usage Warning** — Agent Teams uses significantly more tokens than single sessions. Each teammate = separate Claude instance. Use for complex work where parallel exploration adds value. For routine tasks, single session + subagents is more cost-effective.
  10. **Trust Progression** — Updated progression:
      ```
      Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
        ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑
      ```
      Agent Teams sits above Worktrees because it combines coordination + isolation.
  11. **Hooks for Quality Gates** — TeammateIdle: runs when teammate goes idle, exit code 2 sends feedback. TaskCompleted: runs when task marked complete, exit code 2 prevents completion.
  12. **Limitations** — No session resumption, task status can lag, one team per session, no nested teams, lead is fixed, split panes require tmux/iTerm2
  13. **Reference Files** — Link to: `/team` command, tmux setup guide, PIV-phased control deep dive
- **PATTERN**: Mirror structure of `reference/subagents-overview.md` — starts with "Extending the PIV Loop with...", uses tables, ends with Reference Files section
- **IMPORTS**: N/A (markdown file)
- **GOTCHA**: Keep to ~200-250 lines. This is an on-demand reference guide, not auto-loaded. Be comprehensive but concise.
- **VALIDATE**: Verify file exists, contains all 13 sections, and is between 180-260 lines

### CREATE `.claude/skills/agent-teams/SKILL.md`

- **IMPLEMENT**: Write the Tier 1 skill entry point (~80-120 lines) with:
  1. **Title**: "Agent Teams — Coordinated Multi-Agent Development"
  2. **Overview**: One paragraph explaining what Agent Teams brings to the system
  3. **Quick Start**: How to use `/team [feature]` — the simplest invocation
  4. **PIV Phases Summary** — Brief table showing Lead Mode per phase:
     | Phase | Lead Mode | Teammates | Key Action |
     | Planning | Coordinator | Research agents | Explore & debate |
     | Implementation | Delegate-only | Coding agents + worktrees | Build in parallel |
     | Validation | Synthesizer | Review agents | Check & report |
  5. **Configuration**: Settings needed (experimental flag + teammateMode)
  6. **Prerequisites**: WSL + tmux (for split-pane), or in-process mode (no setup)
  7. **References section**: Links to deep guides in `references/` subdirectory
- **PATTERN**: Mirror `.claude/skills/planning-methodology/SKILL.md` — Tier 1 overview, concise, links to Tier 3 references
- **IMPORTS**: N/A (markdown file)
- **GOTCHA**: Keep under 120 lines. This is the auto-loaded entry point — save details for reference files.
- **VALIDATE**: Verify file exists and is under 120 lines

### CREATE `.claude/skills/agent-teams/references/piv-phased-control.md`

- **IMPLEMENT**: Write the deep dive guide (~150-200 lines) covering:
  1. **The Three Modes** — Detailed explanation of Coordinator, Delegate-only, and Synthesizer modes with specific behaviors and prompts for each
  2. **Planning Phase Deep Dive** — How to structure research teams. Example: spawn 4 teammates (codebase researcher, external docs researcher, architecture analyst, devil's advocate). Spawn prompt templates for each role. How findings flow: teammates message each other → debate → lead synthesizes.
  3. **Implementation Phase Deep Dive** — Delegate mode activation (Shift+Tab). Auto-worktree setup per teammate. Task assignment from Archon. Self-claim mechanics for unblocked tasks. Plan approval requirement: "Require plan approval before they make any changes." Lead reviews teammate plans before they implement.
  4. **Validation Phase Deep Dive** — Review team structure (mirrors existing `/code-review` parallel mode: security, performance, architecture, test coverage). Each reviewer checks ALL implementation work. Lead synthesizes findings into validation report format (use `templates/VALIDATION-REPORT-TEMPLATE.md`).
  5. **Phase Transitions** — How the lead transitions between phases. Clean shutdown of research team before spawning implementation team. Worktree creation between planning and implementation. Worktree merge between implementation and validation.
  6. **Controlling the Lead** — Prompts to keep the lead on track: "Wait for teammates to finish", "Only coordinate, don't implement", "Synthesize findings into a report"
  7. **Archon Sync Points** — When to sync with Archon: start of session (pull tasks), task assignment (update status to "doing"), task completion (update to "review"/"done"), end of session (final sync)
- **PATTERN**: Follow structure of `.claude/skills/planning-methodology/references/6-phase-process.md` — detailed process guide
- **IMPORTS**: N/A (markdown file)
- **GOTCHA**: This is the most conceptually dense file. Use clear examples and prompts throughout. Include actual natural language prompts the user would give to the lead.
- **VALIDATE**: Verify file exists and contains all 7 sections

### UPDATE `reference/subagents-overview.md`

- **IMPLEMENT**: Add Agent Teams to the existing parallel execution documentation:
  1. After the "### Parallel Execution" section (~line 38), add a new subsection "### Agent Teams (Multi-Agent Coordination)" that briefly explains Agent Teams as the next tier above subagents. Include a comparison paragraph: "While subagents report back to the main agent only, Agent Teams teammates can message each other directly, share a task list, and self-coordinate."
  2. Update the "### Trust Progression (Complete)" section to include Agent Teams:
     ```
     Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
     ```
  3. Add a row to the "Agents vs Skills vs Commands" table (if applicable) or add a note pointing to `reference/agent-teams-overview.md` for the full comparison
- **PATTERN**: Match existing section style in the file — concise paragraphs with tables
- **IMPORTS**: N/A
- **GOTCHA**: Don't restructure the existing file — only add new content. Keep additions to ~20-30 lines.
- **VALIDATE**: Verify the file contains "Agent Teams" text and updated trust progression

### UPDATE `reference/git-worktrees-overview.md`

- **IMPLEMENT**: Add Agent Teams integration to the worktree documentation:
  1. In the "### Parallelization Patterns" table (~line 17), add a new row:
     | **Agent Teams + Worktrees** | Medium | Full (code + coordination) | 3-10x | **Coordinated parallel implementation** |
  2. After the table, add a paragraph: "Agent Teams can automatically create worktrees for implementation teammates, combining coordination (shared task list, messaging) with isolation (separate file systems). See `reference/agent-teams-overview.md` and the `/team` command."
  3. In the "### When to Use Git Worktrees" section, add to the "Use worktrees when" list: "Using `/team` command for coordinated multi-agent implementation (worktrees created automatically)"
- **PATTERN**: Match existing table and list formatting
- **IMPORTS**: N/A
- **GOTCHA**: Don't duplicate Agent Teams content here — just add pointers. The full documentation lives in `reference/agent-teams-overview.md`.
- **VALIDATE**: Verify the file contains "Agent Teams" in the parallelization table

---

## VALIDATION COMMANDS

### Syntax & Structure
```bash
# Verify all new files exist
test -f ".claude/skills/agent-teams/references/tmux-wsl-setup.md" && echo "OK" || echo "MISSING"
test -f "reference/agent-teams-overview.md" && echo "OK" || echo "MISSING"
test -f ".claude/skills/agent-teams/SKILL.md" && echo "OK" || echo "MISSING"
test -f ".claude/skills/agent-teams/references/piv-phased-control.md" && echo "OK" || echo "MISSING"
```

### Content Verification
```bash
# Verify key content in reference guide
grep -l "PIV-Phased Control" reference/agent-teams-overview.md
grep -l "Trust Progression" reference/agent-teams-overview.md
grep -l "Archon" reference/agent-teams-overview.md

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

- [ ] All 6 tasks completed in order
- [ ] Each task validation passed
- [ ] All validation commands executed successfully
- [ ] No broken references to other files

---

## HANDOFF NOTES

> What the NEXT sub-plan needs to know about what was done here.

### Files Created
- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — WSL + tmux installation guide, troubleshooting, fallback to in-process mode
- `reference/agent-teams-overview.md` — Primary reference guide covering architecture, PIV-phased control, comparison tables, configuration, trust progression
- `.claude/skills/agent-teams/SKILL.md` — Tier 1 skill entry point with quick start, phase summary, configuration
- `.claude/skills/agent-teams/references/piv-phased-control.md` — Deep dive on Coordinator/Delegate/Synthesizer modes with example prompts

### Files Modified
- `reference/subagents-overview.md` — Added Agent Teams subsection, updated trust progression
- `reference/git-worktrees-overview.md` — Added Agent Teams row to parallelization table, added integration paragraph

### Patterns Established
- **PIV-phased control terminology**: Coordinator (planning), Delegate-only (implementation), Synthesizer (validation) — sub-plan 02 uses these exact terms in the command
- **Trust progression**: `Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote` — this is now the canonical progression

### State for Next Sub-Plan
- Reference guide at `reference/agent-teams-overview.md` — the `/team` command in sub-plan 02 will link to this for detailed documentation
- PIV-phased control guide at `.claude/skills/agent-teams/references/piv-phased-control.md` — the `/team` command references specific prompts from this guide
- TMUX setup guide exists — the `/team` command can reference it for setup instructions
