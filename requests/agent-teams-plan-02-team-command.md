# Sub-Plan 02: /team Command & Spawn Templates

> **Parent Plan**: `requests/agent-teams-plan-overview.md`
> **Sub-Plan**: 02 of 3
> **Phase**: /team Command & Templates
> **Tasks**: 5
> **Estimated Context Load**: Medium

---

## Scope

This sub-plan implements **the `/team` slash command and spawn prompt templates**. The command orchestrates a coordinated implementation team using contract-first spawning, delegate mode, auto-worktrees, and built-in validation. Research happens before `/team` (via subagents or `/planning`). Validation is built into the team workflow.

**What this sub-plan delivers**:
- `/team` command (`.claude/commands/team.md`) — contract-first implementation orchestration (~200-250 lines)
- Spawn prompt templates with contract-first pattern and ownership boundaries
- Customization examples for different team sizes and project types

**Prerequisites from previous sub-plans**:
- Sub-plan 01: Reference guide at `reference/agent-teams-overview.md` (for linking)
- Sub-plan 01: Contract-first spawning guide at `.claude/skills/agent-teams/references/contract-first-spawning.md` (for spawn prompt patterns)
- Sub-plan 01: TMUX setup guide exists (for setup references)

---

## CONTEXT FOR THIS SUB-PLAN

### Files to Read Before Implementing

- `.claude/commands/parallel-e2e.md` — Why: closest existing command to mirror. Same multi-step orchestration pattern with worktrees.
- `.claude/commands/end-to-end-feature.md` — Why: single-feature PIV loop. `/team` extends to multi-agent.
- `.claude/commands/new-worktree.md` — Why: worktree creation logic to embed in the command
- `.claude/commands/merge-worktrees.md` — Why: merge logic to embed after validation

### Files Created by Previous Sub-Plans

- `reference/agent-teams-overview.md` — Created in sub-plan 01: full Agent Teams reference guide
- `.claude/skills/agent-teams/references/contract-first-spawning.md` — Created in sub-plan 01: contract-first spawning with spawn prompt templates
- `.claude/skills/agent-teams/references/tmux-wsl-setup.md` — Created in sub-plan 01: WSL + tmux setup guide

---

## STEP-BY-STEP TASKS

### CREATE `templates/TEAM-SPAWN-PROMPTS.md`

- **IMPLEMENT**: Create spawn prompt templates following the contract-first pattern. Each template includes Cole Medin's 5 required sections (ownership, scope, mandatory communication, contract conformity, cross-cutting concerns):

  **1. Upstream Agent Template** (Database/Schema/Core — spawns FIRST):
  ```
  You are the [ROLE] agent for [FEATURE]. You are the most upstream agent in the contract chain.

  **Ownership**:
  - Files you OWN: [list specific directories/files]
  - Files you must NOT touch: [everything else]

  **Scope**: [what they build]

  **Mandatory Communication — CONTRACT FIRST**:
  Before implementing ANYTHING, you must publish your contract to the lead:
  - [For DB: complete schema with table definitions, function signatures, type definitions]
  - [For Core: public API surface, type exports, interface definitions]
  The lead will verify and forward your contract to downstream agents.
  Only begin implementation AFTER the lead confirms your contract.

  **Cross-Cutting Concerns you own**: [list shared conventions this agent defines]

  **Validation**: Before reporting done, run: [domain-specific validation commands]
  ```

  **2. Downstream Agent Template** (Backend/API — spawns AFTER upstream contract verified):
  ```
  You are the [ROLE] agent for [FEATURE].

  **Ownership**:
  - Files you OWN: [list specific directories/files]
  - Files you must NOT touch: [everything else]

  **Scope**: [what they build]

  **Contract you MUST conform to** (verified by lead):
  [paste the upstream contract here — exact schema, function signatures, etc.]

  **Mandatory Communication — CONTRACT FIRST**:
  Before implementing ANYTHING, publish your API contract to the lead:
  - [endpoint URLs, request/response shapes, error formats]
  The lead will verify and forward to the frontend agent.

  **Cross-Cutting Concerns**: [list shared conventions]

  **Validation**: Before reporting done, run: [domain-specific validation commands]
  ```

  **3. Terminal Agent Template** (Frontend/Consumer — spawns LAST):
  ```
  You are the [ROLE] agent for [FEATURE].

  **Ownership**:
  - Files you OWN: [list specific directories/files]
  - Files you must NOT touch: [everything else]

  **Scope**: [what they build]

  **Contract you MUST conform to** (verified by lead):
  [paste the full API contract here — endpoints, shapes, SSE events, etc.]

  **Cross-Cutting Concerns**: [list shared conventions]

  **Validation**: Before reporting done, run: [domain-specific validation commands]
  ```

  **4. Independent Agent Template** (Testing/DevOps/Docs — can run in parallel):
  ```
  You are the [ROLE] agent for [FEATURE].

  **Ownership**:
  - Files you OWN: [list specific directories/files]
  - Files you must NOT touch: [everything else]

  **Scope**: [what they build]

  **Dependencies**: Wait for [agent] to publish their contract before starting [specific work].
  Other work can proceed immediately.

  **Validation**: Before reporting done, run: [domain-specific validation commands]
  ```

  **Usage Notes** section:
  - Replace all [BRACKETED] values with specifics from your plan
  - The contract section should contain EXACT interfaces, not vague descriptions
  - Cross-cutting concerns should be assigned to ONE agent (usually the most upstream)
  - Add turn limits: "If you've been working for 30+ turns without progress, report blockers to the lead"
  - Log to files: "Write detailed progress to logs/team-{feature}/, send concise summaries via messages"

- **PATTERN**: Follow structure of existing templates — clear sections, copy-paste ready
- **GOTCHA**: These are TEMPLATES, not fixed prompts. Make it clear that users customize for their feature.
- **VALIDATE**: Verify file exists and contains all 4 agent templates plus Usage Notes

### CREATE `templates/TEAM-SPAWN-PROMPTS.md` — Add Customization Examples

- **IMPLEMENT**: After the main templates, add a "Customization Examples" section showing:
  1. **2-Agent Split** (frontend + backend, no separate DB): Backend is upstream, publishes API contract, frontend is downstream. Contract chain: `Backend → Frontend`.
  2. **3-Agent Full-Stack** (database + backend + frontend): Classic chain. Contract chain: `Database → Backend → Frontend`.
  3. **4-Agent Complex** (database + backend + frontend + testing): Testing agent is independent — can run in parallel using the Independent template. Receives all contracts for integration testing.
  4. **Documentation-only project** (like My Coding System): No contract chain needed. All agents are independent — each owns specific files. Use Independent template for all.
  5. **Model selection for teammates**: "Use Sonnet for implementation teammates (balanced capability). Use Haiku for research/review tasks. Specify in spawn prompt or let Claude choose."
- **PATTERN**: Example-driven documentation
- **GOTCHA**: Keep examples concise — show the contract chain and which template to use, not full prompts
- **VALIDATE**: Verify file contains "Customization Examples" section

### CREATE `.claude/commands/team.md`

- **IMPLEMENT**: Write the `/team` command (~200-250 lines) with this structure:

  **Frontmatter**:
  ```yaml
  ---
  description: Orchestrate Agent Teams for coordinated multi-agent implementation using contract-first spawning
  argument-hint: [feature-description or path/to/plan.md]
  allowed-tools: Bash(git:*), Bash(claude:*), Bash(tmux:*), Bash(cd:*), Bash(mkdir:*), Bash(cat:*), Bash(echo:*), Bash(wc:*), Read, Write, Edit, Task, AskUserQuestion
  ---
  ```

  **Title & Preamble**:
  ```markdown
  # Agent Teams — Contract-First Implementation

  **Feature**: $ARGUMENTS

  Orchestrates a coordinated team of Claude Code instances for parallel implementation
  using contract-first spawning. Upstream agents publish interface contracts before
  downstream agents begin. The lead relays and verifies all contracts.

  **When to use this**: Complex features where multiple agents need to coordinate on
  shared interfaces. For research, use subagents. For simple features, use `/end-to-end-feature`.

  **Prerequisites**:
  - Agent Teams enabled: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
  - For split-pane: WSL + tmux (see `.claude/skills/agent-teams/references/tmux-wsl-setup.md`)
  - A plan file at `requests/{feature}-plan.md` (create with `/planning` first)

  **Cost Warning**: Agent Teams uses 2-4x more tokens than a single session.
  Each teammate = separate Claude instance.
  ```

  **Display Configuration** (brief, ~15 lines):
  - Split-pane mode: requires tmux, each teammate gets own pane
  - In-process mode: no setup, use Shift+Up/Down to navigate, Ctrl+T for task list
  - Link to setup guide

  **Step 0: Parse & Prepare**:
  1. If $ARGUMENTS is a `.md` file path: read it as the plan. Extract feature name from heading.
  2. If $ARGUMENTS is a description: remind user to create a plan first with `/planning`, then re-run with the plan path.
  3. Generate kebab-case feature name for branches: `team/{feature}/`
  4. Create logs directory: `mkdir -p logs/team-{feature}/`

  **Step 1: Analyze Plan & Determine Team**:
  1. Read the plan file
  2. Identify the **contract chain**: What depends on what? Look for database/schema → API/backend → frontend/UI patterns. Ask user to confirm if unclear.
  3. Determine **team size** (from plan complexity):
     - 2 agents: Simple frontend/backend split
     - 3 agents: Full-stack (frontend + backend + database)
     - 4 agents: Complex (+ testing/DevOps)
     - 5+ agents: Large systems with many independent modules
  4. Identify **cross-cutting concerns**: shared conventions that need one owner (URL patterns, error shapes, auth approach, etc.)
  5. Present team structure to user for confirmation before proceeding

  **Step 2: Create Worktrees**:
  1. For each teammate, create a worktree:
     ```bash
     git worktree add worktrees/team-{feature}/{agent-name} -b team/{feature}/{agent-name}
     ```
  2. Copy plan to each worktree: `cp requests/{feature}-plan.md worktrees/team-{feature}/{agent-name}/`

  **Step 3: Contract-First Spawning** (core step):
  1. Enter delegate mode (Shift+Tab) — lead must NOT code, only coordinate
  2. Spawn the **most upstream agent first** using the Upstream Agent template from `templates/TEAM-SPAWN-PROMPTS.md`. Include:
     - Worktree path
     - Ownership boundaries
     - Instruction to publish contract BEFORE implementing
  3. Wait for upstream agent to publish their contract (schema, function signatures, types)
  4. **Verify the contract**: check for completeness, ambiguities, missing fields
  5. Spawn the **next downstream agent** with the verified contract pasted into their prompt
  6. Repeat until all agents are spawned
  7. For **independent agents** (testing, docs): spawn in parallel — they don't need upstream contracts

  **Step 4: Monitor & Validate**:
  1. Monitor agent progress. Intervene if:
     - An agent modifies files outside their ownership
     - An agent's implementation diverges from the contract
     - An agent is stuck (30+ turns without progress)
  2. When agents report done, verify:
     - Each agent ran their domain-specific validation (tests, type checks)
     - Pre-completion contract verification: compare actual interfaces against published contracts
  3. Cross-review phase: have agents review each other's integration points
  4. Lead end-to-end validation: verify the integrated system works

  **Step 5: Merge & Commit**:
  1. Merge worktrees sequentially (upstream first):
     ```bash
     git checkout main  # or original branch
     git merge team/{feature}/{upstream-agent} --no-ff
     # run tests after each merge
     git merge team/{feature}/{downstream-agent} --no-ff
     # run tests again
     ```
  2. If merge conflicts: stop, report, provide resolution steps
  3. Run full test suite after all merges
  4. Commit: `git commit -m "feat({feature}): implement via Agent Teams"`
  5. Cleanup worktrees: `git worktree remove worktrees/team-{feature}/{agent}` for each
  6. Sync to Archon (if available): create/update project and tasks with final status

  **Step 6: Report**:
  ```
  Agent Teams Implementation Complete

  Feature: {feature}
  Team Size: {N} agents
  Contract Chain: {upstream} → {downstream} → ...

  Agents:
  - {agent-1}: {role} — {status}
  - {agent-2}: {role} — {status}

  Validation: {pass/fail}
  Merge: {status}
  Commit: {hash}
  ```

  **Error Handling**:
  | Failure Point | Action |
  | Agent Teams not enabled | Show settings instructions, link to setup guide |
  | Plan file not found | Prompt user to run `/planning` first |
  | Worktree creation failure | Report, offer retry or continue with remaining |
  | Contract not published | Prompt upstream agent, extend turn limit |
  | Interface divergence detected | Show diff, ask lead to mediate |
  | Merge conflict | Stop, report files, provide resolution steps |
  | Test failure after merge | Identify which agent's work broke, offer rollback |

  **Notes**:
  - This command expects a plan file. Create one with `/planning [feature]` first.
  - The lead's conversation carries context across the session, providing continuity.
  - Archon sync is best-effort: if Archon tools are unavailable, the command continues without task tracking.
  - For Carlini-style logging: teammates write to `logs/team-{feature}/` for debugging.

- **PATTERN**: Mirror `.claude/commands/parallel-e2e.md` structure: frontmatter → title → steps → error handling → notes
- **GOTCHA**: The command is a PROMPT for Claude Code, not a script. Use natural language instructions, not bash scripts (except for git/worktree commands). Keep it under 250 lines.
- **VALIDATE**: Verify file exists, has correct frontmatter, contains Steps 0-6, and is between 200-250 lines

### UPDATE `templates/TEAM-SPAWN-PROMPTS.md` — Add Anti-Patterns Section

- **IMPLEMENT**: After Customization Examples, add a brief "Anti-Patterns" section from Cole's experience:
  1. **"Just share with each other"** — Never tell agents to communicate directly. The lead must relay and verify all contracts. Agents messaging each other leads to unverified, ambiguous interfaces.
  2. **"Spawn all agents at once"** — Upstream agents must publish contracts before downstream agents start. Spawning all at once = backend builds against wrong DB schema.
  3. **"Skip contract verification"** — Lead must check every contract for completeness before forwarding. Missing fields, ambiguous types, and inconsistent naming cause integration failures.
  4. **"Let agents figure out file boundaries"** — Every spawn prompt must explicitly state files owned and files NOT to touch. Without this, agents overwrite each other's work.
- **PATTERN**: Short, actionable warnings
- **GOTCHA**: Keep brief — 10-15 lines total
- **VALIDATE**: Verify file contains "Anti-Patterns" section

### UPDATE `.claude/commands/team.md` — Final Review & Polish

- **IMPLEMENT**: Read the full command and verify:
  1. All step references are consistent (Step 0-6)
  2. All file path references exist (templates, reference guide, setup guide)
  3. The command stays under 250 lines
  4. Frontmatter `allowed-tools` includes all tools used in the command
  5. Error handling table covers all failure modes
  6. Contract-first spawning is clearly the core pattern (Step 3 is the longest step)
  7. Trim any redundancy or over-explanation
  Fix any issues found.
- **PATTERN**: Quality review pass
- **GOTCHA**: Don't add content in this step — only fix issues found during review.
- **VALIDATE**: Command is complete, consistent, and under 250 lines

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

# Verify command has contract-first as core pattern
grep -l "Contract-First" .claude/commands/team.md
grep -l "contract chain" .claude/commands/team.md

# Verify spawn prompts have all templates
grep -l "Upstream Agent" templates/TEAM-SPAWN-PROMPTS.md
grep -l "Downstream Agent" templates/TEAM-SPAWN-PROMPTS.md
grep -l "Terminal Agent" templates/TEAM-SPAWN-PROMPTS.md
grep -l "Independent Agent" templates/TEAM-SPAWN-PROMPTS.md
grep -l "Anti-Patterns" templates/TEAM-SPAWN-PROMPTS.md
```

### Cross-Reference Check
```bash
# Verify command references template
grep -l "TEAM-SPAWN-PROMPTS" .claude/commands/team.md

# Verify command references setup guide
grep -l "tmux-wsl-setup" .claude/commands/team.md
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
- `.claude/commands/team.md` — The `/team` slash command. Contract-first implementation orchestration: 7 steps (parse, analyze, worktrees, spawn, validate, merge, report). ~200-250 lines.
- `templates/TEAM-SPAWN-PROMPTS.md` — Spawn prompt templates for 4 agent types (upstream, downstream, terminal, independent). Includes customization examples and anti-patterns.

### Files Modified
- `.claude/commands/team.md` was iteratively refined with anti-patterns review and polish pass

### Patterns Established
- **Contract-first spawning in the command**: Step 3 is the core — upstream first, lead relays, downstream after verified contract
- **4 agent template types**: Upstream (spawns first, publishes contract), Downstream (receives contract, publishes own), Terminal (receives contract, no downstream), Independent (parallel, no chain)
- **Plan-first workflow**: `/team` expects a plan file. Create with `/planning` first.

### State for Next Sub-Plan
- `/team` command is complete and ready for integration
- Spawn prompts template is complete with customization examples and anti-patterns
- Sub-plan 03 needs to: update `reference/file-structure.md`, update `memory.md`, update `CLAUDE.md`, verify cross-references
