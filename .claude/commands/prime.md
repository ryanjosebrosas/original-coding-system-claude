---
description: Prime agent with codebase understanding
---

# Prime: Load Project Context

## Process

### 1. Detect Context Mode

Check for code directories using Glob patterns:
- `src/`, `app/`, `frontend/`, `backend/`, `lib/`, `api/`, `server/`, `client/`

**If ANY exist**: This is **Codebase Mode** — focus on source code entry points.
**If NONE exist**: This is **System Mode** — focus on methodology/documentation files.

Report the detected mode and what signals triggered it.

### 2. Analyze Project Structure

**System Mode**:
- List all `.md` files in root, `sections/`, `reference/`, `.claude/`
- Identify commands, agents, skills, templates

**Codebase Mode**:
- Scan using Glob: `**/*.{py,ts,js,tsx,jsx,go,rs}`
- Find config files: `**/package.json`, `**/pyproject.toml`, `**/Cargo.toml`
- Build a mental map without reading yet

If `tree` is available, show structure:
!`tree -L 3 -I 'node_modules|__pycache__|.git|dist|build' 2>/dev/null || ls -la`

### 3. Read Core Documentation

> CLAUDE.md and sections/ are ALREADY auto-loaded. Do NOT re-read them.

**Always read**:
- `memory.md` (if exists) — FULL content, this is cross-session context

**System Mode additional**:
- List `.claude/commands/` and `.claude/agents/` with descriptions

**Codebase Mode additional**:
- Main entry points (main.py, index.ts, app.py)
- Core config files (package.json, pyproject.toml)
- README.md (for project overview)

**Skip**: AGENTS.md (loaded by Claude Code separately)

Limit: Read at most 5 files total. Prioritize by importance.

### 4. Identify Key Files

**System Mode**:
- List commands with their descriptions
- List agents with their purposes
- List available skills

**Codebase Mode**:
- Main entry points
- Core configuration files
- Key model/schema definitions

### 5. Understand Current State

Check recent activity:
!`git log -10 --oneline`

Check current branch and status:
!`git status`

## Output Report

Provide a **COMPREHENSIVE** report (50-80 lines) that is LLM-ready for handoff:

```markdown
# Prime Context Report

## Detection
- **Mode**: {System|Codebase}
- **Signals**: {what directories/patterns triggered this mode}

## Project Overview
- **Type**: {project description - what this project is for}
- **Tech Stack**: {languages, frameworks, build tools}
- **Structure**: {key directories and their purposes}
- **Entry Points**: {main files - codebase mode only}

## Architecture
- {Key patterns and conventions}
- {Important architectural decisions}
- {How components interact}

## Current State
- **Branch**: {name}
- **Status**: {git status summary}
- **Recent Work**: {last 10 commits with brief descriptions}

## Memory Context
- **Last Session**: {date from memory.md}
- **Key Decisions**: {bullet list from memory.md Key Decisions section}
- **Active Patterns**: {from memory.md Architecture Patterns section}
- **Gotchas**: {from memory.md Gotchas section}
- **Memory Health**: {staleness warning if last session >7 days}

## Available Resources
### Commands
{List each command with brief description}

### Agents
{List each agent with brief description}

## Suggested Next Steps
- {Based on current state and memory context}
- {What tasks might be in progress or pending}
```

**Key principle**: The output should be comprehensive enough that a fresh LLM session can pick up full context without additional exploration. "Handoff-ready" means another agent can continue work immediately.
