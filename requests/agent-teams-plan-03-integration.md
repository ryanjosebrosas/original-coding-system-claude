# Sub-Plan 03: Integration & System Updates

> **Parent Plan**: `requests/agent-teams-plan-overview.md`
> **Sub-Plan**: 03 of 3
> **Phase**: Integration & System Updates
> **Tasks**: 5
> **Estimated Context Load**: Low

---

## Scope

This sub-plan implements **system-wide integration** — updating existing documentation to reflect Agent Teams, adding file structure entries, updating memory, and ensuring all cross-references are correct.

**What this sub-plan delivers**:
- Updated file structure documentation
- Updated memory.md with Agent Teams decisions
- Updated CLAUDE.md on-demand guide entry
- Updated command design overview with `/team`
- Cross-reference validation across all new and modified files

**Prerequisites from previous sub-plans**:
- Sub-plan 01: All infrastructure files created (reference guide, skill, tmux guide, contract-first guide)
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

- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — Created in sub-plan 01
- `reference/agent-teams-overview.md` — Created in sub-plan 01
- `.claude/skills/agent-teams/SKILL.md` — Created in sub-plan 01
- `.claude/skills/agent-teams/references/contract-first-spawning.md` — Created in sub-plan 01
- `.claude/commands/team.md` — Created in sub-plan 02
- `templates/TEAM-SPAWN-PROMPTS.md` — Created in sub-plan 02

---

## STEP-BY-STEP TASKS

### UPDATE `reference/file-structure.md`

- **IMPLEMENT**: Add all new files created in sub-plans 01 and 02 to the file structure documentation:
  1. Under `.claude/commands/`:
     - `team.md` — Agent Teams orchestration: contract-first multi-agent implementation
  2. Under `.claude/skills/`:
     - `agent-teams/SKILL.md` — Agent Teams skill entry point
     - `agent-teams/references/tmux-wsl-setup.md` — WSL + tmux installation guide
     - `agent-teams/references/contract-first-spawning.md` — Contract-first spawning deep dive
  3. Under `reference/`:
     - `agent-teams-overview.md` — Agent Teams integration: architecture, contract-first spawning, configuration
  4. Under `templates/`:
     - `TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for Agent Teams (4 agent types)
  5. Update summary counts (e.g., "20 slash commands" → "21", "4 skills" → "5", template count)
- **PATTERN**: Match existing file structure entry format: `filename` — brief description
- **GOTCHA**: Don't restructure the file — only add entries in the right locations.
- **VALIDATE**: Verify file contains entries for `team.md`, `TEAM-SPAWN-PROMPTS.md`, `agent-teams-overview.md`, and `agent-teams/SKILL.md`

### UPDATE `CLAUDE.md`

- **IMPLEMENT**: Add Agent Teams to the On-Demand Guides table:
  ```markdown
  | `reference/agent-teams-overview.md` | Using Agent Teams, `/team` command, contract-first spawning |
  ```
  Add this row after the worktrees entry (since Agent Teams builds on worktrees in the trust progression).
- **PATTERN**: Match existing table row format exactly
- **GOTCHA**: CLAUDE.md is auto-loaded every session (~2K tokens). Only add ONE line to the table. Don't add Agent Teams to the auto-loaded sections.
- **VALIDATE**: Verify CLAUDE.md contains `agent-teams-overview.md` in the On-Demand Guides table

### UPDATE `reference/command-design-overview.md`

- **IMPLEMENT**: Add `/team` to the command registry:
  1. Find the command listing table and add:
     ```markdown
     | `/team` | Orchestrate Agent Teams for contract-first multi-agent implementation | `[feature-description or plan-path]` | High |
     ```
  2. Update trust progression if documented:
     ```
     Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
     ```
  3. Update command count if present (e.g., "20 commands" → "21 commands")
- **PATTERN**: Match existing command table row format
- **GOTCHA**: Read the file first to find exact location and format.
- **VALIDATE**: Verify file contains `/team` entry

### UPDATE `memory.md`

- **IMPLEMENT**: Add Agent Teams entries:
  1. Under **Key Decisions**:
     ```markdown
     - [2026-02-13] Integrated Agent Teams with contract-first spawning — Upstream agents publish contracts before downstream agents start; lead relays and verifies
     - [2026-02-13] Agent Teams for implementation only, subagents for research — 2-4x token savings vs using Agent Teams for everything
     ```
  2. Under **Architecture Patterns**:
     ```markdown
     - **Contract-First Spawning**: Upstream agents first → lead verifies contract → relays to downstream. Used in: `/team` command
     - **Auto-Worktree per Teammate**: Implementation teammates get isolated worktrees. Branch: `team/{feature}/{agent}`. Used in: `/team` Step 2
     ```
  3. Under **Session Notes**:
     ```markdown
     - [2026-02-13] Implemented Agent Teams integration: /team command, reference guide, skill, spawn templates, contract-first spawning guide
     ```
- **PATTERN**: Match existing memory.md entry format (date, brief description)
- **GOTCHA**: Keep entries concise (1-2 lines each). memory.md must stay under 100 lines.
- **VALIDATE**: Verify memory.md contains "Agent Teams" and "contract-first" entries

### VALIDATE Cross-References Across All Files

- **IMPLEMENT**: Read all files created/modified in sub-plans 01-03 and verify:
  1. `/team` command references:
     - `reference/agent-teams-overview.md` ✓
     - `templates/TEAM-SPAWN-PROMPTS.md` ✓
     - `.claude/skills/agent-teams/references/tmux-wsl-setup.md` ✓
  2. Reference guide references:
     - `/team` command ✓
     - Contract-first spawning guide ✓
     - TMUX setup guide ✓
  3. SKILL.md references:
     - `references/contract-first-spawning.md` ✓
     - `references/tmux-wsl-setup.md` ✓
  4. CLAUDE.md references:
     - `reference/agent-teams-overview.md` ✓
  5. No broken links to files that don't exist
  6. All file paths are consistent (no typos, correct directory structure)

  If any broken references found: fix them in the appropriate file.
- **PATTERN**: Cross-reference validation
- **GOTCHA**: Read actual files — don't assume content from the plan.
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
  ".claude/skills/agent-teams/references/contract-first-spawning.md" \
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
grep -l "contract-first" memory.md

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
grep -l "contract-first-spawning" .claude/skills/agent-teams/SKILL.md
grep -l "tmux-wsl-setup" .claude/skills/agent-teams/SKILL.md
```

---

## SUB-PLAN CHECKLIST

- [x] All 5 tasks completed in order
- [x] Each task validation passed
- [x] All validation commands executed successfully
- [x] No broken references to other files

---

## HANDOFF NOTES

### Files Created
- No new files in this sub-plan (all creation in sub-plans 01 and 02)

### Files Modified
- `reference/file-structure.md` — Added all new files from sub-plans 01-02
- `CLAUDE.md` — Added Agent Teams to On-Demand Guides table
- `reference/command-design-overview.md` — Added `/team` to command registry
- `memory.md` — Added Agent Teams decisions, patterns, and session notes

### Patterns Established
- **On-demand guide entry pattern**: One table row in CLAUDE.md → full reference guide in `reference/`

### State for Next Sub-Plan
- N/A — this is the final sub-plan. All files created, all references validated, all documentation updated.
- Ready for feature-wide manual validation and `/commit`.
