# Sub-Plan 03: Integration & System Updates

> **Parent Plan**: `requests/agent-teams-plan-overview.md`
> **Sub-Plan**: 03 of 3
> **Phase**: Integration & System Updates
> **Tasks**: 6
> **Estimated Context Load**: Low

---

## Scope

This sub-plan implements **system-wide integration** — updating existing documentation to reflect Agent Teams, adding file structure entries, updating memory, and ensuring all cross-references are correct.

**What this sub-plan delivers**:
- Updated file structure documentation
- Updated memory.md with Agent Teams decisions
- Updated CLAUDE.md if needed (on-demand guide entry)
- Cross-reference validation across all new and modified files
- Archon project/task setup for tracking this feature

**Prerequisites from previous sub-plans**:
- Sub-plan 01: All infrastructure files created (reference guide, skill, tmux guide, PIV control guide)
- Sub-plan 02: `/team` command and spawn prompt templates created
- Sub-plan 01: `reference/subagents-overview.md` and `reference/git-worktrees-overview.md` updated

---

## CONTEXT FOR THIS SUB-PLAN

### Files to Read Before Implementing

- `reference/file-structure.md` — Why: must add all new files from sub-plans 01 and 02
- `memory.md` — Why: must add Agent Teams decisions and session notes
- `CLAUDE.md` — Why: check if on-demand guides table needs Agent Teams entry
- `reference/command-design-overview.md` — Why: check if command registry needs `/team` entry

### Files Created by Previous Sub-Plans

- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — Created in sub-plan 01: WSL + tmux guide
- `reference/agent-teams-overview.md` — Created in sub-plan 01: primary reference guide
- `.claude/skills/agent-teams/SKILL.md` — Created in sub-plan 01: skill entry point
- `.claude/skills/agent-teams/references/piv-phased-control.md` — Created in sub-plan 01: PIV-phased control guide
- `.claude/commands/team.md` — Created in sub-plan 02: the /team command
- `templates/TEAM-SPAWN-PROMPTS.md` — Created in sub-plan 02: spawn prompt templates

---

## STEP-BY-STEP TASKS

### UPDATE `reference/file-structure.md`

- **IMPLEMENT**: Add all new files created in sub-plans 01 and 02 to the file structure documentation. Add entries in the appropriate sections:
  1. Under `.claude/commands/`:
     - `team.md` — Agent Teams orchestration: full PIV Loop with coordinated multi-agent development
  2. Under `.claude/skills/`:
     - `agent-teams/SKILL.md` — Agent Teams skill entry point
     - `agent-teams/references/tmux-wsl-setup.md` — WSL + tmux installation guide
     - `agent-teams/references/piv-phased-control.md` — PIV-phased control deep dive
  3. Under `reference/`:
     - `agent-teams-overview.md` — Agent Teams integration: architecture, PIV control, configuration
  4. Under `templates/`:
     - `TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for Agent Teams PIV phases
  5. Update any summary counts (e.g., "20 slash commands" → "21 slash commands", "4 skills" → "5 skills", template count)
- **PATTERN**: Match existing file structure entry format: `filename` — brief description
- **IMPORTS**: N/A
- **GOTCHA**: Don't restructure the file — only add entries in the right locations. Check where each section is before adding.
- **VALIDATE**: Verify file contains entries for `team.md`, `TEAM-SPAWN-PROMPTS.md`, `agent-teams-overview.md`, and `agent-teams/SKILL.md`

### UPDATE `CLAUDE.md`

- **IMPLEMENT**: Add Agent Teams to the On-Demand Guides table in CLAUDE.md:
  ```markdown
  | `reference/agent-teams-overview.md` | Using Agent Teams, `/team` command, multi-agent coordination |
  ```
  Add this row to the existing table in the "On-Demand Guides" section. Place it after the worktrees entry since Agent Teams builds on top of worktrees.
- **PATTERN**: Match existing table row format exactly
- **IMPORTS**: N/A
- **GOTCHA**: CLAUDE.md is auto-loaded every session (~2K tokens). Only add ONE line to the table — the reference guide itself is loaded on-demand. Don't add Agent Teams to the auto-loaded sections.
- **VALIDATE**: Verify CLAUDE.md contains `agent-teams-overview.md` in the On-Demand Guides table

### UPDATE `reference/command-design-overview.md`

- **IMPLEMENT**: Add `/team` to the command registry. Find the command listing table and add:
  ```markdown
  | `/team` | Orchestrate Agent Teams for full PIV Loop | `[feature-description or plan-path]` | High |
  ```
  Also add `/team` to the trust progression if it's documented there:
  ```
  Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
  ```
  If there's a command count, update it (e.g., "20 commands" → "21 commands").
- **PATTERN**: Match existing command table row format
- **IMPORTS**: N/A
- **GOTCHA**: Read the file first to find the exact location and format of the command table. The file structure may vary.
- **VALIDATE**: Verify file contains `/team` entry

### UPDATE `memory.md`

- **IMPLEMENT**: Add Agent Teams entries to memory.md:
  1. Under **Key Decisions**:
     ```markdown
     - [2026-02-13] Integrated Agent Teams as primary multi-agent orchestration — Full integration with PIV-phased control (Coordinator/Delegate/Synthesizer)
     - [2026-02-13] WSL + tmux for split-pane display on Windows — Fallback: in-process mode (no setup required)
     - [2026-02-13] Archon as source of truth for team task management — Agent Teams task list is ephemeral, Archon persists
     ```
  2. Under **Architecture Patterns**:
     ```markdown
     - **Agent Teams PIV Control**: Coordinator (planning) → Delegate-only (implementation) → Synthesizer (validation). Used in: `/team` command
     - **Auto-Worktree per Teammate**: Implementation teammates get isolated worktrees automatically. Used in: `/team` Step 2
     ```
  3. Under **Session Notes**:
     ```markdown
     - [2026-02-13] Implemented Agent Teams integration: /team command, reference guide, skill, spawn templates, tmux setup guide
     ```
- **PATTERN**: Match existing memory.md entry format (date, brief description, context)
- **IMPORTS**: N/A
- **GOTCHA**: Keep entries concise (1-2 lines each). memory.md must stay under 100 lines. If approaching limit, archive older entries.
- **VALIDATE**: Verify memory.md contains "Agent Teams" entries in Key Decisions and Architecture Patterns

### UPDATE `reference/multi-model-strategy.md`

- **IMPLEMENT**: Add Agent Teams model guidance:
  1. Find the model routing table/section and add Agent Teams recommendations:
     - **Research teammates** (planning phase): Haiku — cost optimization for exploration tasks
     - **Implementation teammates**: Sonnet — balanced capability for coding
     - **Review teammates** (validation phase): Haiku — cost optimization for pattern-matching review
     - **Team lead**: inherits from session (typically Opus for orchestration)
  2. Add a note: "Agent Teams uses significantly more tokens than single sessions. Use Haiku for research/review teammates to control costs. Specify model in spawn prompt: 'Use Haiku for each research teammate.'"
- **PATTERN**: Match existing model routing guidance format
- **IMPORTS**: N/A
- **GOTCHA**: Don't restructure the file — just add Agent Teams as a new scenario in the existing guidance.
- **VALIDATE**: Verify file contains "Agent Teams" model routing recommendations

### VALIDATE Cross-References Across All Files

- **IMPLEMENT**: This is a validation-only task. Read all files created/modified in sub-plans 01-03 and verify:
  1. `/team` command references:
     - `reference/agent-teams-overview.md` ✓
     - `templates/TEAM-SPAWN-PROMPTS.md` ✓
     - `.claude/skills/agent-teams/references/tmux-wsl-setup.md` ✓
     - Archon tools (manage_task, find_tasks) ✓
  2. Reference guide references:
     - `/team` command ✓
     - TMUX setup guide ✓
     - PIV-phased control guide ✓
  3. SKILL.md references:
     - `references/tmux-wsl-setup.md` ✓
     - `references/piv-phased-control.md` ✓
  4. CLAUDE.md references:
     - `reference/agent-teams-overview.md` ✓
  5. No broken links to files that don't exist
  6. All file paths are consistent (no typos, correct directory structure)

  If any broken references found: fix them in the appropriate file.
- **PATTERN**: Cross-reference check pattern from validation commands
- **IMPORTS**: N/A
- **GOTCHA**: Read actual files — don't assume content from the plan. Files may have been modified slightly during implementation.
- **VALIDATE**: All cross-references verified, no broken links

---

## VALIDATION COMMANDS

### Syntax & Structure
```bash
# Verify all files from all sub-plans exist
for f in \
  ".claude/skills/agent-teams/references/tmux-wsl-setup.md" \
  "reference/agent-teams-overview.md" \
  ".claude/skills/agent-teams/SKILL.md" \
  ".claude/skills/agent-teams/references/piv-phased-control.md" \
  ".claude/commands/team.md" \
  "templates/TEAM-SPAWN-PROMPTS.md"; do
  test -f "$f" && echo "OK: $f" || echo "MISSING: $f"
done
```

### Content Verification
```bash
# Verify CLAUDE.md has agent-teams entry
grep -l "agent-teams-overview" CLAUDE.md

# Verify memory.md has Agent Teams
grep -l "Agent Teams" memory.md

# Verify file structure has new entries
grep -l "team.md" reference/file-structure.md
grep -l "TEAM-SPAWN-PROMPTS" reference/file-structure.md
```

### Cross-Reference Check
```bash
# Verify command references template
grep -l "TEAM-SPAWN-PROMPTS" .claude/commands/team.md

# Verify reference guide links to command
grep -l "team" reference/agent-teams-overview.md

# Verify skill links to references
grep -l "piv-phased-control" .claude/skills/agent-teams/SKILL.md
grep -l "tmux-wsl-setup" .claude/skills/agent-teams/SKILL.md
```

---

## SUB-PLAN CHECKLIST

- [ ] All 6 tasks completed in order
- [ ] Each task validation passed
- [ ] All validation commands executed successfully
- [ ] No broken references to other files

---

## HANDOFF NOTES

### Files Created
- No new files in this sub-plan (all creation in sub-plans 01 and 02)

### Files Modified
- `reference/file-structure.md` — Added all new files from sub-plans 01-02
- `CLAUDE.md` — Added Agent Teams to On-Demand Guides table
- `reference/command-design-overview.md` — Added `/team` to command registry
- `memory.md` — Added Agent Teams decisions, patterns, and session notes
- `reference/multi-model-strategy.md` — Added Agent Teams model routing guidance

### Patterns Established
- **On-demand guide entry pattern**: One table row in CLAUDE.md → full reference guide in `reference/`. Keeps auto-load cost minimal.

### State for Next Sub-Plan
- N/A — this is the final sub-plan. All files created, all references validated, all documentation updated.
- Ready for feature-wide manual validation and `/commit`.
