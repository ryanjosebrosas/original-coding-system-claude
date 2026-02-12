# Feature: CLAUDE.md Slim Restructure

## Feature Description

Move task-specific sections (06-14) from auto-loaded `sections/` to on-demand `reference/`, keeping only essential every-session rules in `sections/`. Replace removed sections with a slim index in CLAUDE.md that tells the AI what exists and when to load it.

## User Story

As a developer using this system, I want CLAUDE.md to only auto-load rules I need every session, so that ~12,000 tokens of context window aren't wasted on GitHub Integration, Worktrees, and MCP docs when I'm just implementing a feature.

## Problem Statement

All 15 sections are auto-loaded via `@sections/` in CLAUDE.md. Sections 06-14 (~9,000 words / ~12,000 tokens) are task-specific — only relevant when doing that specific workflow. This violates the system's own Two-Question Framework: "Is this needed every session? No → on-demand in reference/."

Current cost: ~15,000-18,000 tokens auto-loaded. Target: ~3,500-4,500 tokens auto-loaded + slim index (~500 tokens).

## Solution Statement

- Decision 1: Move sections 06-14 content to `reference/` — because they're task-specific, not every-session
- Decision 2: Keep sections 01-05 + 15 as auto-loaded — because they're needed every session
- Decision 3: Add slim "Available Guides" index in CLAUDE.md — because the AI needs to know what exists and when to load it (one line per guide, no full content)
- Decision 4: Rename moved files to match reference/ naming convention — because reference/ uses kebab-case descriptive names, not numbered prefixes

## Feature Metadata

- **Feature Type**: Refactor
- **Estimated Complexity**: Low-Medium
- **Primary Systems Affected**: CLAUDE.md, sections/, reference/, 4 existing plans in requests/
- **Dependencies**: None

---

## CONTEXT REFERENCES

### Relevant Codebase Files

> IMPORTANT: The execution agent MUST read these files before implementing!

- `CLAUDE.md` (lines 1-84) — Why: main file being restructured, contains all @sections/ references
- `sections/08_file_structure.md` (all) — Why: documents the file structure, must be updated to reflect new locations
- `reference/global-rules-optimization.md` (lines 1-50) — Why: contains the Two-Question Framework that justifies this change

### Files to Move (section → reference)

| Current Path | New Path | Words |
|---|---|---|
| `sections/06_layer1_guide.md` | `reference/layer1-guide.md` | 474 |
| `sections/07_validation_strategy.md` | `reference/validation-strategy.md` | 297 |
| `sections/08_file_structure.md` | `reference/file-structure.md` | 678 |
| `sections/09_command_design.md` | `reference/command-design-overview.md` | 1,608 |
| `sections/10_github_integration.md` | `reference/github-integration.md` | 1,253 |
| `sections/11_remote_system.md` | `reference/remote-system-overview.md` | 744 |
| `sections/12_mcp_servers_cloud_skills.md` | `reference/mcp-skills-overview.md` | 1,407 |
| `sections/13_subagents.md` | `reference/subagents-overview.md` | 1,138 |
| `sections/14_git_worktrees.md` | `reference/git-worktrees-overview.md` | 1,432 |

### Cross-References to Update

These files reference sections 06-14 and need path updates:

**Reference guides (section path mentions in text):**
- `reference/piv-loop-practice.md` — references sections 06, 07
- `reference/global-rules-optimization.md` — references sections 06, 09, 12
- `reference/command-design-framework.md` — references section 09
- `reference/implementation-discipline.md` — references section 09
- `reference/github-orchestration.md` — references section 10
- `reference/remote-agentic-system.md` — references sections 10, 11
- `reference/mcp-skills-archon.md` — references sections 12, 15
- `reference/subagents-deep-dive.md` — references section 13
- `reference/git-worktrees-parallel.md` — references sections 13, 14
- `reference/subagents-guide.md` — references section 07
- `reference/validation-discipline.md` — references section 07

**Sections (cross-references between sections):**
- `sections/02_piv_loop.md` (line 40) — references section 10
- `sections/09_command_design.md` (lines 172, 183) — references sections 10, 13

**Templates:**
- `templates/VALIDATION-PROMPT.md` (line 6) — references section 07

**Agents:**
- `.claude/agents/_examples/README.md` (line 243) — references section 09

**Commands:**
- `.claude/commands/init-c.md` — references sections 06, 07, 09, 10 (note: these appear to be generic section refs like `@sections/06_testing.md` for project generation, NOT references to this system's sections — verify before changing)

**Existing plans (in requests/):**
- `requests/skills-expansion-plan.md` — references sections 08, 12, 14
- `requests/command-completion-enhancement-plan.md` — references section 08
- `requests/mem0-to-memory-migration-plan.md` — references sections 08, 12
- `requests/reference-templates-completion-plan.md` — references section 08

### Patterns to Follow

**Existing reference/ naming convention:**
```
reference/system-foundations.md
reference/piv-loop-practice.md
reference/global-rules-optimization.md
reference/command-design-framework.md
```
- Kebab-case, descriptive names, no number prefixes

**Existing on-demand loading pattern** (from CLAUDE.md footer):
```
> For deeper context on this system, see the reference guides in `reference/`
```

---

## IMPLEMENTATION PLAN

### Phase 1: Move Files

Git-move sections 06-14 to reference/ with new names. Delete original section files.

### Phase 2: Restructure CLAUDE.md

Remove @sections/ references for 06-14. Add slim "Available Guides" index section that lists each moved guide with a one-line "load when..." trigger.

### Phase 3: Update Cross-References

Update all files that reference the old `sections/06-14` paths to point to new `reference/` paths.

### Phase 4: Validate

Verify no broken references remain. Verify sections/ only contains 01-05 + 15.

---

## STEP-BY-STEP TASKS

### 1. MOVE sections/06-14 to reference/ via git mv

- **IMPLEMENT**: Run `git mv` for each file:
  ```
  git mv sections/06_layer1_guide.md reference/layer1-guide.md
  git mv sections/07_validation_strategy.md reference/validation-strategy.md
  git mv sections/08_file_structure.md reference/file-structure.md
  git mv sections/09_command_design.md reference/command-design-overview.md
  git mv sections/10_github_integration.md reference/github-integration.md
  git mv sections/11_remote_system.md reference/remote-system-overview.md
  git mv sections/12_mcp_servers_cloud_skills.md reference/mcp-skills-overview.md
  git mv sections/13_subagents.md reference/subagents-overview.md
  git mv sections/14_git_worktrees.md reference/git-worktrees-overview.md
  ```
- **GOTCHA**: Use `git mv` not manual move — preserves git history
- **VALIDATE**: `ls sections/` should show only 01-05 + 15. `ls reference/` should include all new files.

### 2. UPDATE CLAUDE.md

- **IMPLEMENT**: Replace lines 30-79 (sections 06-14 references) with a slim index:

  Keep sections 01-05 and 15 as-is (auto-loaded). Replace the middle block with:

  ```markdown
  ---

  ## On-Demand Guides

  > These guides are NOT auto-loaded. Read them when the task requires it.

  | Guide | Load when... |
  |-------|-------------|
  | `reference/layer1-guide.md` | Setting up CLAUDE.md for a new project |
  | `reference/validation-strategy.md` | Planning or running validation |
  | `reference/file-structure.md` | Looking up where files belong |
  | `reference/command-design-overview.md` | Designing or modifying slash commands |
  | `reference/github-integration.md` | Setting up GitHub Actions or CodeRabbit |
  | `reference/remote-system-overview.md` | Deploying or using the remote coding agent |
  | `reference/mcp-skills-overview.md` | Configuring MCP servers or creating skills |
  | `reference/subagents-overview.md` | Creating or debugging subagents |
  | `reference/git-worktrees-overview.md` | Parallel feature implementation with worktrees |

  ---
  ```

- **GOTCHA**: Keep the Archon Workflow (section 15) auto-loaded — it's needed every session when Archon is active
- **VALIDATE**: Read CLAUDE.md, confirm only 6 @sections/ references remain (01-05 + 15)

### 3. UPDATE reference/file-structure.md (formerly sections/08)

- **IMPLEMENT**: Update the file tree to reflect the new structure:
  - `sections/` directory should only list 01-05 + 15
  - `reference/` directory should include the 9 newly moved guides
  - Update any self-referencing paths
- **VALIDATE**: Read the updated file, confirm it matches actual file structure

### 4. UPDATE cross-references in reference/ guides

- **IMPLEMENT**: For each reference guide that mentions `sections/06-14`, update the path to the new `reference/` location. Specific changes:

  **reference/piv-loop-practice.md:**
  - `sections/06_layer1_guide.md` → `reference/layer1-guide.md`
  - `sections/07_validation_strategy.md` → `reference/validation-strategy.md`

  **reference/global-rules-optimization.md:**
  - `sections/06_layer1_guide.md` → `reference/layer1-guide.md`
  - `sections/09_command_design.md` → `reference/command-design-overview.md`
  - `sections/12_mcp_servers_cloud_skills.md` → `reference/mcp-skills-overview.md`
  - Remove/update "always-loaded" language since these are now on-demand

  **reference/command-design-framework.md:**
  - `sections/09_command_design.md` → `reference/command-design-overview.md`

  **reference/implementation-discipline.md:**
  - `sections/09_command_design.md` → `reference/command-design-overview.md`

  **reference/github-orchestration.md:**
  - `sections/10_github_integration.md` → `reference/github-integration.md`

  **reference/remote-agentic-system.md:**
  - `sections/10_github_integration.md` → `reference/github-integration.md`
  - `sections/11_remote_system.md` → `reference/remote-system-overview.md`

  **reference/mcp-skills-archon.md:**
  - `sections/12_mcp_servers_cloud_skills.md` → `reference/mcp-skills-overview.md`

  **reference/subagents-deep-dive.md:**
  - `sections/13_subagents.md` → `reference/subagents-overview.md`

  **reference/git-worktrees-parallel.md:**
  - `sections/13_subagents.md` → `reference/subagents-overview.md`
  - `sections/14_git_worktrees.md` → `reference/git-worktrees-overview.md`

  **reference/subagents-guide.md:**
  - `sections/07_validation_strategy.md` → `reference/validation-strategy.md`

  **reference/validation-discipline.md:**
  - `sections/07_validation_strategy.md` → `reference/validation-strategy.md`

- **GOTCHA**: Some references say "always-loaded overview in `sections/XX`" — update these to "on-demand guide at `reference/XX`" since they're no longer always-loaded
- **VALIDATE**: `grep -r "sections/0[6-9]\|sections/1[0-4]" reference/` should return zero results

### 5. UPDATE cross-references in remaining sections/

- **IMPLEMENT**:
  - `sections/02_piv_loop.md` line 40: `sections/10_github_integration.md` → `reference/github-integration.md`
  - `sections/09_command_design.md` becomes `reference/command-design-overview.md` — update its internal refs:
    - Line 172: `sections/13_subagents.md` → `reference/subagents-overview.md`
    - Line 183: `sections/10_github_integration.md` → `reference/github-integration.md`

  Wait — section 09 IS being moved. So the cross-references within the moved files also need updating. Apply the same pattern: any moved file that references another moved file should use the new reference/ path.

- **VALIDATE**: `grep -r "sections/0[6-9]\|sections/1[0-4]" sections/` should return zero results

### 6. UPDATE templates and agents

- **IMPLEMENT**:
  - `templates/VALIDATION-PROMPT.md` line 6: `sections/07_validation_strategy.md` → `reference/validation-strategy.md`
  - `.claude/agents/_examples/README.md` line 243: `sections/09_command_design.md` → `reference/command-design-overview.md`

- **VALIDATE**: `grep -r "sections/0[6-9]\|sections/1[0-4]" templates/ .claude/agents/` should return zero results

### 7. UPDATE existing plans in requests/

- **IMPLEMENT**: Update path references in the 4 existing plans:
  - `requests/skills-expansion-plan.md`: sections/08 → reference/file-structure.md, sections/12 → reference/mcp-skills-overview.md, sections/14 → reference/git-worktrees-overview.md
  - `requests/command-completion-enhancement-plan.md`: sections/08 → reference/file-structure.md
  - `requests/mem0-to-memory-migration-plan.md`: sections/08 → reference/file-structure.md, sections/12 → reference/mcp-skills-overview.md
  - `requests/reference-templates-completion-plan.md`: sections/08 → reference/file-structure.md

- **VALIDATE**: `grep -r "sections/0[6-9]\|sections/1[0-4]" requests/` should return zero results

### 8. VERIFY init-c.md (special case)

- **IMPLEMENT**: Read `.claude/commands/init-c.md` and check if its section references (06_testing, 07_api_contracts, 09_dev_commands, 10_ai_instructions) are references to THIS system's sections or generic section names for project generation. If they're template placeholders for new projects, leave them unchanged. If they reference this system's files, update them.

- **VALIDATE**: Manual verification — read the file and confirm

### 9. FINAL VALIDATION

- **IMPLEMENT**: Run comprehensive grep to find any remaining references:
  ```
  grep -r "sections/06\|sections/07\|sections/08\|sections/09\|sections/10\|sections/11\|sections/12\|sections/13\|sections/14" . --include="*.md"
  ```
  Exclude false positives (e.g., git history, this plan file itself).

- **VALIDATE**: Zero results (excluding this plan file)

---

## VALIDATION COMMANDS

### Level 1: File Structure
```bash
# Verify sections/ only has 01-05 + 15
ls sections/

# Verify reference/ has the 9 new files
ls reference/*overview* reference/layer1* reference/validation-strategy* reference/file-structure* reference/github-integration*
```

### Level 2: No Broken References
```bash
# No remaining references to old section paths
grep -r "sections/0[6-9]\|sections/1[0-4]" . --include="*.md" | grep -v "requests/claude-md-slim-restructure-plan.md"

# CLAUDE.md only has 6 @sections references
grep "@sections/" CLAUDE.md
```

### Level 3: Content Integrity
```bash
# Word count of auto-loaded content (should be ~2,500 words, down from ~11,200)
cat sections/*.md | wc -w
```

### Level 4: Manual Validation
- Read CLAUDE.md end-to-end — should be scannable, slim, with clear index
- Verify the on-demand guides table makes sense
- Spot-check 2-3 reference guides to confirm paths updated

---

## ACCEPTANCE CRITERIA

- [x] CLAUDE.md auto-loads only sections 01-05 + 15 (~2,215 words vs ~11,200)
- [x] On-demand guides table in CLAUDE.md lists all 9 moved guides with "load when..." triggers
- [x] All 9 section files moved to reference/ with new names (git history preserved via git mv)
- [x] Zero remaining references to old `sections/06-14` paths across entire codebase
- [x] reference/file-structure.md reflects the new directory structure
- [x] Existing plans in requests/ updated with new paths

---

## COMPLETION CHECKLIST

- [x] All tasks completed in order (1-9)
- [x] Each task validation passed
- [x] Final grep shows zero broken references
- [x] CLAUDE.md is readable and slim
- [x] Git mv preserves history

---

## NOTES

### Key Design Decisions
- Keep section 15 (Archon) auto-loaded — it's the task management system used nearly every session
- Use a table format for the index — scannable, one line per guide, easy to extend
- Rename files to match reference/ convention (kebab-case, no numbers) — consistency matters

### Risks
- Risk: Commands or skills that use `@sections/XX` for file inclusion will break → Mitigation: grep verified no commands use @sections/ for 06-14 (init-c uses different section names for project generation)
- Risk: Existing plans become stale with wrong paths → Mitigation: Task 7 updates all 4 plans

### Token Savings Estimate
- Before: ~15,000-18,000 tokens auto-loaded
- After: ~3,500-4,500 tokens auto-loaded + ~500 token index
- Savings: ~11,000-13,000 tokens per session (~10-12% of context window)

### Confidence Score: 9/10
- **Strengths**: Straightforward file moves + find-and-replace. No logic changes. The system's own rules justify this.
- **Uncertainties**: init-c.md section references need manual verification
- **Mitigations**: Task 8 handles init-c.md as a special case
