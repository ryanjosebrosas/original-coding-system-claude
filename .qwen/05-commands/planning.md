---
description: "Create comprehensive feature plan with deep codebase analysis using Qwen SubAgents"
argument-hint: "[feature-description] [--swarm]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "WebSearch", "WebFetch", "Task"]
---

# Planning: Comprehensive Feature Plan (Qwen-Optimized)

## Feature Request

$ARGUMENTS

## Mission

Transform this feature request into a **comprehensive implementation plan** through systematic codebase analysis, external research, and strategic planning using Qwen Code's native capabilities.

**Core Principle**: The template is the control mechanism. All research fills specific template sections. Nothing is missed because the template specifies what's needed.

**Key Rules**:
- We do NOT write code in this phase. Create a context-rich plan.
- Plan must be **700-1000 lines minimum**.
- Use Qwen Code's **SubAgents** for parallel research execution.
- Use **Skills** for specialized capabilities.
- Leverage **@file** and **@symbol** references for precise context.

## Swarm Decision

**Check for `--swarm` in arguments.**

**If --swarm flag present** → Use Swarm Decomposition Mode (creates plan series with SubAgents)
**If not** → Standard Single Plan Mode

### When to Use Swarm Mode

Use `--swarm` when:
- Feature has 4+ independent components
- Multiple modules need simultaneous changes
- Estimated implementation time > 2 hours
- Risk of conflicts between changes is high

### When NOT to Use Swarm Mode

- Simple feature (1-2 files)
- Changes are sequential/dependent
- Quick bug fix or small enhancement

## Determine Feature Name

Create kebab-case feature name (e.g., "user-authentication", "payment-processing").

**Feature Name**: [create-feature-name]
**Plan File**: `requests/[feature-name]-plan.md`
**Swarm Mode**: Yes/No

---

## THE TEMPLATE (CONTROL MECHANISM)

Read `.qwen/03-templates/plans/STRUCTURED-PLAN-TEMPLATE.md` now — it defines the exact structure. All 6 phases below fill those template sections.

---

## PHASE 0: Interactive Discovery (Vibe Planning Buddy)

**Goal**: Collaboratively discover scope, approach, and priorities before formal planning.

**Escape hatch**: If the user provides detailed requirements, references an existing plan, or wants to skip discovery — proceed to Phase 1.

**Process**:

1. **Understand the user's level**: Adapt language — technical users get architecture questions, non-technical get outcome-focused questions.
2. **Challenge constructively**: Ask probing questions to sharpen the vision — what problem does this solve? What's the simplest valuable version? Have you seen this done well?
3. **Explore inspiration**: If user has reference projects/repos, analyze their approach. If not, suggest 2-3 approaches with trade-offs.
4. **Scope negotiation**: Push back on scope creep. Suggest vertical slices. Identify hidden complexity.
5. **Confirm readiness**: Summarize agreed scope, list key decisions, get user confirmation before proceeding.

**Rules**: This is a CONVERSATION, not a checklist. Be genuinely curious. If the user has a clear vision, respect that. Spend 3-10 minutes depending on clarity.

---

## PHASE 1: Feature Understanding & Scoping

**Goal**: Fill → Feature Description, User Story, Problem Statement, Solution Statement, Feature Metadata

1. Check memory.md for past decisions about this feature area
2. Parse the feature request. If unclear, ask user to clarify BEFORE continuing.
3. Create User Story: `As a [user], I want [goal], so that [benefit]`
4. State Problem and Solution approach
5. Document Feature Metadata: Type (New/Enhancement/Refactor/Fix), Complexity (Low/Medium/High), Systems Affected, Dependencies

**Qwen Tools**: Use `@file` references to link to related existing code during scoping.

---

## PHASE 2: Codebase Intelligence (Parallel SubAgents)

**Goal**: Fill → Relevant Codebase Files, New Files to Create, Patterns to Follow

After Phase 1 scopes the feature, launch **2 parallel SubAgents** for codebase research.

**Launch simultaneously** — all SubAgents run in parallel using Qwen Code's native SubAgent system.

### SubAgent A: Similar Implementations & Integration Points
**Type**: SubAgent (general-purpose)
**Description**: "Find similar code and integration points"

**Prompt includes**:
- The feature description and systems affected from Phase 1
- Specific Grep/Glob queries for relevant patterns
- "Document all relevant file paths WITH line numbers"
- "Identify which existing files need changes"
- Use `@file` and `@symbol` references for precision

### SubAgent B: Project Patterns & Conventions
**Type**: SubAgent (general-purpose)
**Description**: "Extract project patterns"

**Prompt includes**:
- Instruction to read 2-3 representative files
- Extract: naming conventions, error handling, logging, type patterns
- Include code snippets with file:line references
- Use Qwen's file reading tools for pattern extraction

**Fallback**: If feature is trivial (1-2 files, obvious pattern), skip SubAgents and explore directly with Glob/Grep.

**Qwen Advantage**: SubAgents can reference files using `@path/to/file` syntax for precise context sharing.

---

## PHASE 3: External Research

**Goal**: Fill → Relevant Documentation

Launch SubAgent to find:
- Official documentation with specific section links
- Version compatibility and breaking changes
- Known gotchas and recommended patterns

**Qwen Tool**: Use `web_search` and `web_fetch` tools available in Qwen Code SubAgents.

**Fallback**: If purely internal changes, skip and note "No external research needed."

---

## SWARM DECOMPOSITION (Only if --swarm flag)

### Determine Decomposition Strategy

Based on codebase analysis, choose strategy:

**Strategy Options**:
1. **file-based** (default): By file/module boundaries
   - Worker A: auth/controller.ts
   - Worker B: auth/service.ts

2. **feature-based**: By functional areas
   - Worker A: OAuth implementation
   - Worker B: Session management

3. **risk-based**: By risk/complexity
   - Worker A: CRITICAL - Schema changes
   - Worker B: MEDIUM - Query updates

### Create Sub-Plan Files

For each subtask, create: `requests/[feature-name]-plan-[NN].md`

Example for "auth" with 3 workers:
- `requests/auth-plan-01.md` - OAuth flow
- `requests/auth-plan-02.md` - Session management
- `requests/auth-plan-03.md` - Tests & middleware

Each sub-plan:
- 500-700 lines minimum
- Specific to one worker's scope
- Contains file reservations
- References patterns from main plan

### Create Master Plan Overview

`requests/[feature-name]-plan.md` (the main file):

```markdown
<!-- PLAN-SERIES -->
# [Feature Name] - Implementation Plan (Swarm Mode)

## Overview
Master plan coordinating [N] parallel workers.

## PLAN INDEX
1. [requests/auth-plan-01.md] - OAuth flow implementation
2. [requests/auth-plan-02.md] - Session management
3. [requests/auth-plan-03.md] - Tests & middleware

## Shared Context
- Common patterns from codebase
- External documentation references
- Testing requirements
- Validation commands

## Worker Coordination
- Worker A: Files [list]
- Worker B: Files [list]
- Worker C: Files [list]

## Integration Points
- Where workers interface
- Shared data structures
- API contracts

## HANDOFF NOTES
Notes to carry between sub-plans...
```

### File Reservation Strategy

Document which files each worker will reserve:

```
Worker A (OAuth):
- src/auth/oauth.ts (CREATE)
- src/config/oauth.ts (UPDATE)

Worker B (Session):
- src/auth/session.ts (CREATE)
- src/middleware/session.ts (CREATE)

Worker C (Tests):
- tests/auth/*.test.ts (CREATE)
```

**Qwen Coordination**: Use SubAgent messaging for worker synchronization when executing.

---

## PHASE 4: Strategic Design & Synthesis

**Goal**: Fill → Implementation Plan (phases), Testing Strategy, Acceptance Criteria

1. **Synthesize SubAgent findings** from Phases 2 & 3
2. **Design implementation approach**: fit with existing architecture, dependency ordering
3. **Plan testing strategy**: unit tests, integration tests, edge cases
4. **Define acceptance criteria**: specific, measurable

---

## PHASE 5: Step-by-Step Task Generation

**Goal**: Fill → STEP-BY-STEP TASKS section

**CRITICAL Rule**: Each task MUST include ALL fields:

- **ACTION**: CREATE / UPDATE / ADD / REMOVE / REFACTOR / MIRROR
- **TARGET**: Specific file path
- **IMPLEMENT**: What to implement (code-level detail)
- **PATTERN**: Reference to codebase pattern (file:line)
- **IMPORTS**: Exact imports needed
- **GOTCHA**: Known pitfalls
- **VALIDATE**: Executable verification command

Break Phase 4's implementation phases into atomic tasks. Order by dependency.

**Qwen Enhancement**: Use `@file:line` references in PATTERN fields for clickable navigation.

---

## PHASE 6: Quality Validation & Confidence Score

**Goal**: Fill → Validation Commands, Completion Checklist, Notes

1. **Compile validation commands**: Syntax, Types, Unit Tests, Integration Tests, Manual
2. **Create completion checklist**: all tasks done, validations pass
3. **Assess confidence**: Score X/10, strengths, uncertainties, mitigations

**Qwen Integration**: Document which validation commands can use Qwen's built-in tools vs external CLI commands.

---

## OUTPUT

### Standard Mode

Save to: `requests/[feature-name]-plan.md`

Use `.qwen/03-templates/plans/STRUCTURED-PLAN-TEMPLATE.md`. Every section must be filled.

### Swarm Mode

Save master to: `requests/[feature-name]-plan.md`
Save sub-plans to: `requests/[feature-name]-plan-[NN].md`

### Confirmation

Report:
- Feature name and plan file path(s)
- Mode: Single Plan / Swarm ([N] workers)
- Complexity and key risks
- Confidence score
- Next step: `/execute` or `/swarm`

**For Swarm Mode**:
```
Created master plan: requests/[feature]-plan.md
Created [N] sub-plans for parallel execution:
  - requests/[feature]-plan-01.md → Worker A
  - requests/[feature]-plan-02.md → Worker B
  ...

Run `/swarm [feature]` to execute with parallel coordination.
```

---

## QWEN CODE INTEGRATION NOTES

### SubAgent System
- SubAgents are specialized agents that handle specific tasks within your workflow
- Use `general-purpose` SubAgent type for research tasks
- SubAgents can use: Read, Glob, Grep, Bash, WebSearch, WebFetch
- SubAgents return structured findings to parent conversation
- Use `@file` syntax for precise file references in SubAgent prompts

### Skills System
- Skills are modular capabilities that extend Qwen Code's effectiveness
- Each Skill is a package containing `SKILL.md` with instructions
- Skills are **model-invoked** — AI autonomously decides when to use them
- Manual invocation: `/skills <skill-name>` with autocomplete
- Planning methodology skill: `skill: "planning-methodology"`

### Context Management
- Use `@file` to reference files in chat
- Use `@symbol` to reference specific functions/classes
- SubAgents inherit context from parent conversation
- Plan files serve as context handoff to execution agents
- Context files: `QWEN.md` or `.qwen/QWEN.md` for hierarchical instructions

### Settings
- User settings: `~/.qwen/settings.json`
- Project settings: `.qwen/settings.json`
- Skills location: `~/.qwen/skills/` (personal) or `.qwen/skills/` (project)
