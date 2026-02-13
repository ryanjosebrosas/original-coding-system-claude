# AGENTS.md

This file provides guidance for AI coding agents operating in the My Coding System repository.

---

## Project Overview

This is a **development methodology/documentation system** for AI-assisted coding with Claude Code. It contains no application code - only Markdown, YAML, and configuration files for workflow automation.

**Primary artifacts:**
- Slash commands (`.claude/commands/`)
- Reusable templates (`templates/`)
- Reference documentation (`reference/`)
- Core rules (`sections/` - auto-loaded via CLAUDE.md)

---

## Build/Lint/Test Commands

### There Are No Build Commands

This project has no package.json, Makefile, or build system. It consists entirely of documentation and configuration files.

### Validation

For documentation changes, validate manually:
```bash
# Check markdown links (if tool available)
markdown-link-check **/*.md

# Verify YAML syntax
yamllint .coderabbit.yaml
```

### Git Operations (Primary Workflow)

```bash
# Status and diff
git status
git diff HEAD

# Commit (conventional format required)
git add .
git commit -m "type(scope): description"

# Push and PR
git push -u origin <branch>
gh pr create --title "type(scope): description" --body "..."
```

### Running Commands

Slash commands are invoked directly in Claude Code:
```
/prime              # Load codebase context
/planning           # Create implementation plan
/execute            # Implement from plan
/commit             # Git commit
/code-review        # Review code changes
```

---

## Code Style Guidelines

### File Naming

| Type | Convention | Example |
|------|------------|---------|
| Documentation | kebab-case | `code-review.md` |
| Templates | UPPERCASE-KEBAB | `STRUCTURED-PLAN-TEMPLATE.md` |
| Directories | lowercase-hyphenated | `github-workflows/` |
| Commands | kebab-case | `end-to-end-feature.md` |

### Markdown Conventions

- **Headers**: Use `#` hierarchy consistently (H1 > H2 > H3)
- **Lists**: Use `-` for unordered, `1.` for ordered
- **Code blocks**: Always include language hint (```bash, ```yaml)
- **Emphasis**: Use `**bold**` for important terms
- **Tables**: Pipe-delimited with header separators
- **Blockquotes**: Use `>` for callouts and warnings

### Frontmatter (Commands)

```yaml
---
description: "Brief description for /help"
argument-hint: [expected-arguments]
allowed-tools: Bash(git:*), Read, Write, Edit
model: claude-sonnet-4
---
```

### Frontmatter (Agents)

```yaml
---
name: agent-name-kebab-case
description: When to use this agent
model: haiku|sonnet|opus
tools: ["Read", "Glob", "Grep"]
---
```

### Commit Messages

**Format**: Conventional commits
```
type(scope): imperative description (50 chars max)
```

**Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`, `plan`

**Critical Rules**:
- NEVER include `Co-Authored-By` lines
- Use imperative mood ("add" not "added")
- Keep subject line under 50 characters

### Placeholders

- `{curly-braces}` - User input placeholders
- `$ARGUMENTS` - Command arguments
- `[square-brackets]` - Optional elements

---

## Project Structure

```
My-Coding-System/
├── CLAUDE.md              # Auto-loaded rules (~2K tokens)
├── memory.md              # Cross-session memory
├── sections/              # Core rules (auto-loaded via @)
│   ├── 01_core_principles.md
│   ├── 02_piv_loop.md
│   ├── 03_context_engineering.md
│   ├── 04_git_save_points.md
│   └── 05_decision_framework.md
├── reference/             # Deep guides (on-demand, ~89K tokens)
├── templates/             # Reusable templates (18 files)
├── .claude/
│   ├── commands/          # Slash commands (20 commands)
│   ├── skills/            # Cloud skills (4 skills)
│   └── agents/_examples/  # Subagent examples
└── .github/workflows/     # GitHub Action workflows
```

---

## Core Principles

Agents must follow these principles from `sections/01_core_principles.md`:

1. **YAGNI** - Only implement what's needed right now
2. **KISS** - Prefer simple, readable solutions over clever abstractions
3. **DRY** - Extract common patterns, but don't over-abstract
4. **Limit AI Assumptions** - Be explicit in plans and prompts
5. **Always Be Priming (ABP)** - Start every session with `/prime`

---

## PIV Loop Methodology

Every feature follows the Plan-Implement-Validate cycle:

| Layer | Phase | Output |
|-------|-------|--------|
| 1 | Prime | Context loaded |
| 2 | Plan | `requests/{feature}-plan.md` |
| 3 | Implement | Working code + tests |
| 4 | Validate | All levels pass |

**Commit plans before implementing** (Git Save Points methodology).

---

## Decision Framework

### Proceed Autonomously When
- Task is clear from context
- Following established patterns
- Implementation plan is explicit

### Ask User When
- Requirements are ambiguous
- Multiple valid approaches exist
- Breaking changes are needed
- Business logic decisions required

### Never
- Use `EnterPlanMode` - Use `/planning` command instead
- Commit without explicit user request
- Skip validation levels

---

## Context Management

### Auto-Loaded (~2K tokens)
- `CLAUDE.md` and `sections/*.md`

### On-Demand (Load When Needed)
| Guide | Load when... |
|-------|-------------|
| `reference/layer1-guide.md` | Setting up CLAUDE.md |
| `reference/validation-strategy.md` | Planning validation |
| `reference/command-design-overview.md` | Designing commands |
| `reference/subagents-overview.md` | Creating subagents |

---

## Output Format Standards

### Code Reviews
```markdown
## Summary
- Total issues: N
- Critical: X | High: Y | Medium: Z

## Findings
### [SEVERITY] Category: Brief description
**File**: `path/to/file.ts:42`
**Issue**: Description
**Suggestion**: Recommended fix
```

### Plans
```markdown
## Phase N: Phase Name
### Step N.1: Step Name
- **Files**: `path/to/modify.ts`
- **Action**: What to do
- **GOTCHA**: Known pitfalls
```

---

## Error Handling

- Include GOTCHA fields in plans for known pitfalls
- Run full validation pyramid before marking complete
- Don't fix issues without user approval during reviews

---

## Agent Design Pattern

Follow the Role-Mission-Context-Approach-Output framework:

```markdown
## Role
[Agent's expertise area]

## Mission
[Primary objective]

## Context
[What the agent knows/receives]

## Approach
[Step-by-step methodology]

## Output
[Expected deliverable format]
```

---

## Important Reminders

1. This is documentation, not application code - no build/test commands exist
2. `/prime` should be run at session start to load context
3. Plans go in `requests/{feature}-plan.md`
4. Never skip the Plan phase - commit plans before implementing
5. Keep `memory.md` under 100 lines for cross-session context
6. Use structured output formats with file:line references
