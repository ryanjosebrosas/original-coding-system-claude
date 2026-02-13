# Sub-Plan 02: /team Command & Templates

> **Parent Plan**: `requests/agent-teams-plan-overview.md`
> **Sub-Plan**: 02 of 3
> **Phase**: /team Command & Templates
> **Tasks**: 7
> **Estimated Context Load**: Medium

---

## Scope

This sub-plan implements **the `/team` slash command and its supporting templates**. This is the core deliverable — a single command that orchestrates a full PIV Loop using Agent Teams with PIV-phased control, auto-worktree creation, and Archon task sync.

**What this sub-plan delivers**:
- `/team` command (`.claude/commands/team.md`) — full PIV Loop with Agent Teams
- Spawn prompt templates for each PIV phase
- End-to-end team orchestration: research → implement → review → merge → commit

**Prerequisites from previous sub-plans**:
- Sub-plan 01: Reference guide at `reference/agent-teams-overview.md` (for linking)
- Sub-plan 01: PIV-phased control guide at `.claude/skills/agent-teams/references/piv-phased-control.md` (for prompt patterns)
- Sub-plan 01: TMUX setup guide exists (for setup references)

---

## CONTEXT FOR THIS SUB-PLAN

### Files to Read Before Implementing

- `.claude/commands/parallel-e2e.md` — Why: closest existing command to mirror. Same multi-step orchestration pattern with worktrees, but uses `claude -p` instead of Agent Teams
- `.claude/commands/end-to-end-feature.md` — Why: single-feature PIV loop. `/team` extends this to multi-agent
- `.claude/commands/new-worktree.md` — Why: worktree creation logic to embed in implementation phase
- `.claude/commands/merge-worktrees.md` — Why: merge logic to embed after validation phase
- `templates/TEAM-SPAWN-PROMPTS.md` — Why: created in this sub-plan, referenced by the command

### Files Created by Previous Sub-Plans

- `reference/agent-teams-overview.md` — Created in sub-plan 01: full Agent Teams reference guide
- `.claude/skills/agent-teams/references/piv-phased-control.md` — Created in sub-plan 01: PIV-phased control with example prompts
- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — Created in sub-plan 01: WSL + tmux setup guide

---

## STEP-BY-STEP TASKS

### CREATE `templates/TEAM-SPAWN-PROMPTS.md`

- **IMPLEMENT**: Create spawn prompt templates for each PIV phase. Each template is a natural language prompt the lead uses when spawning teammates:

  **1. Planning Phase — Research Teammates** (4 roles):
  - **Codebase Researcher**: "Explore the codebase to understand existing patterns, architecture, and integration points for [feature]. Focus on: file structure, naming conventions, existing similar features, and potential conflicts. Report your findings with file paths and line numbers."
  - **External Researcher**: "Research external documentation, best practices, and examples for [feature]. Search for: official docs, community patterns, known gotchas, and recommended approaches. Report findings with source links."
  - **Architecture Analyst**: "Analyze the architectural implications of [feature]. Consider: where it fits in the existing system, what components need to change, performance implications, and the simplest viable approach. Propose 2-3 architecture options with trade-offs."
  - **Devil's Advocate**: "Challenge assumptions about [feature]. Question: Is this feature actually needed? What could go wrong? Are there simpler alternatives? What edge cases will break? Report concerns with severity ratings."

  **2. Implementation Phase — Coding Teammates** (per-feature):
  - **Feature Implementer**: "You are implementing [feature-slice] from a structured plan. Your worktree is at [worktree-path] on branch [branch-name]. Read the plan at [plan-path] and execute ALL tasks in the STEP-BY-STEP TASKS section, in order. For each task: read IMPLEMENT, follow PATTERN, use IMPORTS, watch for GOTCHA, run VALIDATE. After all tasks: run VALIDATION COMMANDS, fix failures, commit with: git add -A && git commit -m 'feat([slice]): implement [description]'. Require plan approval before making changes."

  **3. Validation Phase — Review Teammates** (4 roles):
  - **Security Reviewer**: "Review all code changes across worktrees for security vulnerabilities. Focus on: input validation, authentication, authorization, injection attacks, sensitive data exposure. Report findings with severity (Critical/High/Medium/Low), file:line, and recommended fix."
  - **Performance Reviewer**: "Review all code changes for performance issues. Focus on: N+1 queries, unnecessary computations, memory leaks, inefficient algorithms, missing caching opportunities. Report findings with impact rating and suggested optimization."
  - **Architecture Reviewer**: "Review all code changes for architecture compliance. Focus on: adherence to project patterns, DRY/YAGNI/KISS principles, proper separation of concerns, consistent naming, appropriate abstraction level. Report findings with severity and pattern reference."
  - **Test Coverage Reviewer**: "Review all code changes for test adequacy. Focus on: missing unit tests, untested edge cases, missing integration tests, test quality (assertions, not just smoke tests). Report missing tests with specific test cases to add."

  Include a **Usage Notes** section explaining: prompts are templates — replace [bracketed] values. Customize roles based on feature needs (e.g., skip devil's advocate for straightforward features, add domain-specific reviewers).

- **PATTERN**: Follow structure of existing templates — clear sections, copy-paste ready content
- **IMPORTS**: N/A
- **GOTCHA**: These are TEMPLATES, not fixed prompts. Make it clear that users should customize for their specific feature. Include [bracketed] placeholders for all variable content.
- **VALIDATE**: Verify file exists and contains all 3 phase sections with their role prompts

### CREATE `.claude/commands/team.md`

- **IMPLEMENT**: Write the `/team` command (~400-450 lines) with this structure:

  **Frontmatter**:
  ```yaml
  ---
  description: Orchestrate Agent Teams for full PIV Loop with coordinated multi-agent development
  argument-hint: [feature-description or path/to/plan.md]
  allowed-tools: Bash(git:*), Bash(claude:*), Bash(tmux:*), Bash(cd:*), Bash(cp:*), Bash(mkdir:*), Bash(wait:*), Bash(kill:*), Bash(cat:*), Bash(sleep:*), Bash(echo:*), Bash(wc:*), Bash(gh:*), Read, Write, Edit, Task, AskUserQuestion, mcp__archon__manage_project, mcp__archon__manage_task, mcp__archon__find_tasks, mcp__archon__find_projects, mcp__archon__rag_search_knowledge_base, mcp__archon__rag_search_code_examples
  ---
  ```

  **Title & Description**:
  ```markdown
  # Agent Teams — Full PIV Loop

  **Feature**: $ARGUMENTS

  Orchestrates a coordinated team of Claude Code instances through a complete PIV Loop:
  Planning (research team) → Implementation (coding team + worktrees) → Validation (review team).

  **Prerequisites**:
  - Agent Teams enabled: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings
  - For split-pane display: WSL + tmux (see `.claude/skills/agent-teams/references/tmux-wsl-setup.md`)
  - For in-process mode: no additional setup needed

  **Cost Warning**: Agent Teams uses significantly more tokens than a single session.
  Each teammate = separate Claude instance. N teammates ≈ N× token cost.

  **Trust Warning**: Only use this command if you've used `/end-to-end-feature` and `/parallel-e2e` reliably. This is the highest-coordination command in the system.
  ```

  **Step 0: Parse & Validate**:
  1. Check if $ARGUMENTS is a file path (ends in `.md`) → if so, skip planning phase, go directly to implementation
  2. Check if Agent Teams is enabled (note: the command can't check settings, so just include a reminder)
  3. Parse feature description for naming: generate kebab-case name, branch prefix `team/{feature}/`
  4. Check Archon for existing project/tasks: `find_tasks(query="{feature}")`. If tasks exist, display them and ask if we should use them or create new ones.

  **Step 1: PLANNING PHASE — Lead as Coordinator**:
  1. Tell the user: "Starting Planning Phase. The lead will coordinate research teammates."
  2. Instruct the lead to create a team with these prompts (referencing `templates/TEAM-SPAWN-PROMPTS.md`):
     ```
     Create an agent team to research and plan [feature]. Spawn these teammates:
     - Codebase researcher: explore existing patterns and integration points
     - External researcher: find documentation and best practices
     - Architecture analyst: propose implementation approaches
     - Devil's advocate: challenge assumptions and find edge cases

     Have them explore the problem, share findings with each other, and debate approaches.
     When they're done, synthesize findings into a structured plan.
     ```
  3. Wait for research to complete
  4. Lead synthesizes findings into a structured plan at `requests/{feature}-plan.md` using `templates/STRUCTURED-PLAN-TEMPLATE.md`
  5. Create Archon tasks from the plan: parse STEP-BY-STEP TASKS section, create one Archon task per step using `manage_task("create", ...)`
  6. Commit the plan: `git add requests/{feature}-plan.md && git commit -m "plan: {feature} structured plan"`
  7. Ask the lead to clean up research teammates: "Shut down all research teammates and clean up the team"

  **Step 2: IMPLEMENTATION PHASE — Lead as Delegate**:
  1. Tell the user: "Starting Implementation Phase. The lead will delegate only — no direct coding."
  2. Parse the plan to determine vertical slices (implementation tasks that can be parallelized)
  3. Create worktrees for each implementation teammate:
     ```bash
     git worktree add worktrees/team-{feature}/{slice-name} -b team/{feature}/{slice-name}
     ```
  4. Copy plan to each worktree: `cp requests/{feature}-plan.md worktrees/team-{feature}/{slice-name}/requests/`
  5. Instruct the lead to create a NEW team with implementation teammates:
     ```
     Create an agent team to implement [feature]. Use delegate mode (Shift+Tab).

     Spawn these teammates, each in their own worktree:
     - [slice-1] implementer: working in worktrees/team-{feature}/{slice-1}/
     - [slice-2] implementer: working in worktrees/team-{feature}/{slice-2}/

     Require plan approval before teammates make changes.
     Wait for all teammates to complete before proceeding.

     Assign tasks from the plan. Teammates should self-claim unblocked tasks.
     ```
  6. Update Archon task status as teammates work: `manage_task("update", task_id="...", status="doing")`
  7. Wait for all implementation teammates to complete
  8. Update Archon tasks to "review" status
  9. Ask the lead to shut down implementation teammates and clean up

  **Step 3: VALIDATION PHASE — Lead as Synthesizer**:
  1. Tell the user: "Starting Validation Phase. The lead will synthesize review findings."
  2. Instruct the lead to create a NEW team with review teammates:
     ```
     Create an agent team to review the implementation of [feature].
     Spawn these review teammates:
     - Security reviewer: check all changes for vulnerabilities
     - Performance reviewer: check for performance issues
     - Architecture reviewer: verify pattern compliance
     - Test coverage reviewer: identify missing tests

     Each reviewer should examine ALL worktrees:
     [list worktree paths]

     Have them share and challenge each other's findings.
     Synthesize all findings into a validation report.
     ```
  3. Wait for all reviews to complete
  4. Lead synthesizes into validation report format (reference `templates/VALIDATION-REPORT-TEMPLATE.md`)
  5. If critical/high issues found: present to user, ask whether to fix or proceed
  6. Ask the lead to shut down review teammates and clean up

  **Step 4: MERGE & COMMIT**:
  1. Merge all implementation worktrees (embed `/merge-worktrees` logic):
     - Create integration branch: `git checkout -b integration-team-{feature}`
     - Sequential merge: `git merge team/{feature}/{slice} --no-ff` for each slice
     - If conflicts: stop, report, provide resolution steps
     - Run project tests after each merge
  2. Final validation: run full test suite
  3. Merge to original branch
  4. Commit: `git commit -m "feat({feature}): implement via Agent Teams"`
  5. Sync final status to Archon: mark all tasks "done"
  6. Update memory.md with lessons learned
  7. Cleanup worktrees: `git worktree remove worktrees/team-{feature}/{slice}` for each

  **Step 5: REPORT**:
  ```
  Agent Teams PIV Loop Complete

  Feature: {feature}
  Team Size: {N research} + {M implementation} + {4 review} teammates
  Phases: Planning ✓ | Implementation ✓ | Validation ✓

  Planning:
  - Research teammates: {N}
  - Plan: requests/{feature}-plan.md

  Implementation:
  - Worktrees: {M}
  - Tasks completed: {X}/{Y}

  Validation:
  - Critical issues: {count}
  - High issues: {count}
  - Report: {location}

  Merge: {status}
  Commit: {hash}

  Token Usage: ~{estimate} (vs ~{single-session-estimate} single session)
  ```

  **Error Handling Table**:
  | Failure Point | Action |
  | Agent Teams not enabled | Show settings instructions, link to setup guide |
  | Research teammate failure | Continue with remaining, note gaps |
  | Planning synthesis failure | Fall back to manual plan creation |
  | Worktree creation failure | Report, offer retry or continue with others |
  | Implementation failure | Show teammate logs, offer partial merge |
  | Merge conflict | Rollback instructions, resolution steps |
  | Test failure after merge | Identify which slice, rollback instructions |
  | Archon sync failure | Continue without sync, warn user |

  **Notes section**:
  - This command creates 3 separate teams (one per PIV phase). Each team is cleaned up before the next starts. This is because Claude Code supports one team per session, but teams can be created and destroyed within a session.
  - The lead's conversation history carries across teams within the same session, providing continuity.
  - For plan-only mode: pass a plan file path instead of a feature description to skip the planning phase
  - Archon sync is best-effort: if Archon is unavailable, the command continues without task tracking

  **Carlini Patterns** (from "Building a C Compiler with Parallel Agents"):
  - **Logging**: Create `logs/team-{feature}/` directory. Tell teammates to log progress to files, not just inline output. Lead can grep logs for debugging.
  - **Time limits**: Set `--max-turns 50` equivalent awareness in spawn prompts. Tell teammates: "If you've been working for more than 30 turns without progress, report blockers to the lead."
  - **Output minimization**: Spawn prompts should instruct teammates: "Write detailed findings to files. Send concise summaries via messages. Don't pollute the lead's context with verbose output."
  - **Validation as verifier**: The validation phase IS the high-quality test suite. Review teammates are the verifiers. TaskCompleted hooks prevent premature completion.

- **PATTERN**: Mirror `.claude/commands/parallel-e2e.md` structure: frontmatter → title → steps → error handling → notes
- **IMPORTS**: N/A
- **GOTCHA**: The command is a PROMPT for Claude Code, not a script. It describes what the AI should do, not executable code. Use natural language instructions, not bash scripts (except for git/worktree commands). Keep it under 450 lines — this is already a complex command.
- **VALIDATE**: Verify file exists, has correct frontmatter, contains all 6 steps (0-5), and is between 350-450 lines

### UPDATE `templates/TEAM-SPAWN-PROMPTS.md` — Add Customization Examples

- **IMPLEMENT**: After the main templates, add a "Customization Examples" section showing:
  1. **Small feature** (2-3 tasks): Skip devil's advocate, use 2 implementation teammates, use 2 reviewers (security + architecture)
  2. **Large feature** (10+ tasks): Add domain-specific researchers, use 4-6 implementation teammates, add all 4 review roles
  3. **Research-only mode**: Use only planning phase teammates, no implementation or validation
  4. **Model selection for teammates**: "Use Sonnet for implementation teammates (need high capability). Use Haiku for research teammates (cost optimization). Specify in spawn prompt: 'Use Sonnet for each teammate.'"
- **PATTERN**: Example-driven documentation
- **IMPORTS**: N/A
- **GOTCHA**: Keep examples concise — show the spawn prompt variant, not the full flow
- **VALIDATE**: Verify file contains "Customization Examples" section

### UPDATE `.claude/commands/team.md` — Add Plan-Input Mode

- **IMPLEMENT**: In Step 0, expand the plan-input detection:
  ```markdown
  ### Plan-Input Mode

  If $ARGUMENTS is a file path ending in `.md`:
  1. Read the plan file
  2. Verify it's a valid structured plan (has STEP-BY-STEP TASKS section)
  3. Skip Step 1 (Planning Phase) entirely
  4. Proceed directly to Step 2 (Implementation Phase) using the provided plan
  5. Extract feature name from plan's "# Feature:" heading

  This allows: `/team requests/my-feature-plan.md` to skip planning and go straight to
  coordinated implementation + validation.
  ```
  Add this as a subsection within Step 0, after the parse & validate logic.
- **PATTERN**: Same as the main command
- **IMPORTS**: N/A
- **GOTCHA**: Plan-input mode still runs validation phase. Only planning is skipped.
- **VALIDATE**: Verify the command contains "Plan-Input Mode" section

### UPDATE `.claude/commands/team.md` — Add Archon Integration Details

- **IMPLEMENT**: Expand the Archon integration in each step:
  - Step 0: Check for existing Archon project. If found, display project tasks. If not, create new project: `manage_project("create", title="{feature}", description="Agent Teams implementation")`
  - Step 1 (Planning): After plan created, create Archon tasks from STEP-BY-STEP TASKS section. Parse each `### {ACTION} {file}` into a task: `manage_task("create", project_id="...", title="{ACTION} {file}", description="...")`
  - Step 2 (Implementation): Before spawning each teammate, update their assigned tasks to "doing". After teammate completes, update to "review".
  - Step 3 (Validation): After review completes, update tasks to "done" if no critical issues.
  - Step 4 (Merge): Final sync — mark all tasks "done" after successful merge.

  Add these as inline additions to each step, not separate sections. Keep additions concise (~5-10 lines per step).
- **PATTERN**: Match existing Archon integration in `/parallel-e2e.md`
- **IMPORTS**: N/A
- **GOTCHA**: Archon integration must be best-effort. If Archon tools fail (MCP server down), the command should continue without task tracking. Add fallback note.
- **VALIDATE**: Verify the command references Archon tools (manage_task, find_tasks) in multiple steps

### UPDATE `.claude/commands/team.md` — Add TMUX/Display Notes

- **IMPLEMENT**: Add a "Display Configuration" section before Step 0:
  ```markdown
  ## Display Configuration

  This command works with both display modes:

  **Split-pane mode (recommended for visibility)**:
  - Requires: WSL + tmux (see `.claude/skills/agent-teams/references/tmux-wsl-setup.md`)
  - Each teammate gets its own terminal pane
  - Click into any pane to interact directly
  - Start Claude Code inside a tmux session for automatic split panes

  **In-process mode (works anywhere)**:
  - No additional setup needed
  - Use Shift+Up/Down to navigate between teammates
  - Press Enter to view a teammate's session, Escape to interrupt
  - Press Ctrl+T to toggle the task list

  Set mode in settings.json:
  ```json
  {
    "teammateMode": "tmux",
    "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
  }
  ```
  Or per-session: `claude --teammate-mode in-process`
  ```
- **PATTERN**: Similar to platform/prerequisite notes in `/parallel-e2e.md`
- **IMPORTS**: N/A
- **GOTCHA**: Don't duplicate the full TMUX setup guide — just link to it. Keep this section to ~20 lines.
- **VALIDATE**: Verify the command contains "Display Configuration" section with both modes

---

## VALIDATION COMMANDS

### Syntax & Structure
```bash
# Verify new files exist
test -f ".claude/commands/team.md" && echo "OK" || echo "MISSING"
test -f "templates/TEAM-SPAWN-PROMPTS.md" && echo "OK" || echo "MISSING"
```

### Content Verification
```bash
# Verify command has correct frontmatter
grep -l "description:" .claude/commands/team.md
grep -l "allowed-tools:" .claude/commands/team.md

# Verify command has all steps
grep -c "## Step" .claude/commands/team.md  # Should be 6 (Steps 0-5)

# Verify PIV phases are present
grep -l "PLANNING PHASE" .claude/commands/team.md
grep -l "IMPLEMENTATION PHASE" .claude/commands/team.md
grep -l "VALIDATION PHASE" .claude/commands/team.md

# Verify spawn prompts have all phases
grep -l "Planning Phase" templates/TEAM-SPAWN-PROMPTS.md
grep -l "Implementation Phase" templates/TEAM-SPAWN-PROMPTS.md
grep -l "Validation Phase" templates/TEAM-SPAWN-PROMPTS.md
```

### Cross-Reference Check
```bash
# Verify command references template
grep -l "TEAM-SPAWN-PROMPTS" .claude/commands/team.md

# Verify command references Archon tools
grep -l "manage_task" .claude/commands/team.md
grep -l "find_tasks" .claude/commands/team.md

# Verify command references setup guide
grep -l "tmux-wsl-setup" .claude/commands/team.md
```

---

## SUB-PLAN CHECKLIST

- [ ] All 7 tasks completed in order
- [ ] Each task validation passed
- [ ] All validation commands executed successfully
- [ ] No broken references to other files

---

## HANDOFF NOTES

### Files Created
- `.claude/commands/team.md` — The `/team` slash command. Full PIV Loop with Agent Teams: 6 steps (parse, planning, implementation, validation, merge, report). ~400-450 lines.
- `templates/TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for all 3 PIV phases: research (4 roles), implementation (per-slice), review (4 roles). Includes customization examples.

### Files Modified
- `.claude/commands/team.md` was iteratively updated with: plan-input mode, Archon integration details, and display configuration section

### Patterns Established
- **3-team-per-session pattern**: One team per PIV phase, each cleaned up before the next. Lead's conversation carries across teams.
- **Plan-input mode**: Pass a `.md` file to skip planning and go straight to implementation. Pattern: detect file path → read → skip to Step 2.
- **Archon sync pattern**: Create project → create tasks from plan → update "doing" during implementation → update "done" after merge. Best-effort (continues if Archon unavailable).

### State for Next Sub-Plan
- `/team` command is complete and ready for integration testing
- Spawn prompts template is complete with customization examples
- Sub-plan 03 needs to: update `reference/file-structure.md` to list new files, update `memory.md` with decisions, verify cross-references between all created files
