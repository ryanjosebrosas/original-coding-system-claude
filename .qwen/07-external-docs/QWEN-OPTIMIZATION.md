# Qwen Code Optimization Summary

## Overview

This document summarizes the transformation of the coding system from Claude Code to Qwen Code optimization.

---

## What Was Created

### 1. `.qwen/commands/planning.md`

**Purpose**: Main planning command optimized for Qwen Code

**Key Changes**:
- References Qwen's `general-purpose` SubAgent type
- Uses Qwen's Plan Mode (`/plan`) workflow
- Integrates `@file` and `@symbol` reference syntax
- Supports `--swarm` flag for parallel execution

**Usage**:
```bash
qwen
> /planning user-authentication
```

---

### 2. `.qwen/agents/` — 12 SubAgent Definitions

All agents use Qwen3-Coder models with `general-purpose` SubAgent type.

#### Research Agents (2)
- `research-codebase.md` — Codebase exploration with `@file:line` references
- `research-external.md` — Documentation research with `web_search`/`web_fetch` tools

#### Code Review Agents (4)
- `code-review-architecture.md` — Architecture and pattern compliance
- `code-review-type-safety.md` — Type annotations and type checking
- `code-review-security.md` — Security vulnerability detection
- `code-review-performance.md` — Performance optimization opportunities

#### Utility Agents (2)
- `plan-validator.md` — Plan quality validation (1-10 scoring)
- `test-generator.md` — Test case generation

#### Specialist Agents (4)
- `specialist-devops.md` — CI/CD, Docker, infrastructure
- `specialist-data.md` — Database design, ORM, migrations
- `specialist-copywriter.md` — UX writing, microcopy
- `specialist-tech-writer.md` — API documentation, technical guides

---

### 3. `.qwen/skills/planning-methodology.md`

**Purpose**: Systematic 6-phase planning methodology as a Qwen Skill

**Key Features**:
- Compatible with Qwen Code v2.0+
- Invokable via `skill: "planning-methodology"`
- Maps each phase to template sections
- Includes Swarm Decomposition guidance

**Usage**:
```bash
qwen
> skill: "planning-methodology"
```

---

### 4. `templates/STRUCTURED-PLAN-TEMPLATE.md` (Updated)

**Changes**:
- Added Qwen Code Integration notes
- `@file:line` syntax for IDE navigation
- SubAgent references for specialized tasks
- Plan Mode workflow integration

---

### 5. `README.md` (Updated)

**Major Changes**:
- Replaced all Claude Code references with Qwen Code
- Added "Qwen Code Integration" section
- Updated installation instructions (`npm i @qwen-code/qwen-code@latest -g`)
- Updated command examples (`qwen` instead of `claude`)
- Removed Archon MCP references (replaced with web tools)
- Updated model strategy section (removed Opus/Sonnet references)

---

## Qwen Code Features Leveraged

### SubAgents
- **Type**: `general-purpose` for all agents
- **Model**: Qwen3-Coder (default)
- **Tools**: Read, Glob, Grep, Bash, WebSearch, WebFetch
- **Context**: Isolated per-agent context windows
- **Syntax**: `@file` and `@symbol` references

### Plan Mode
- **Command**: `/plan`
- **Workflow**: Enter Plan Mode → Run planning → Review → Execute
- **Benefit**: Structured planning workflow native to Qwen Code

### Skills
- **System**: Extensible capability library
- **Integration**: `skill: "skill-name"` syntax
- **Custom**: Skills stored in `.qwen/skills/`

### Context Management
- **File References**: `@file:line` for clickable navigation
- **Inheritance**: SubAgents inherit parent context
- **Handoff**: Plan files serve as context bridge

---

## Directory Structure

```
opencode-coding-system/
├── .qwen/
│   ├── commands/
│   │   └── planning.md          # Main planning command
│   ├── agents/
│   │   ├── research-codebase.md
│   │   ├── research-external.md
│   │   ├── code-review-*.md     (4 files)
│   │   ├── plan-validator.md
│   │   ├── test-generator.md
│   │   └── specialist-*.md      (4 files)
│   └── skills/
│       └── planning-methodology.md
├── templates/
│   └── STRUCTURED-PLAN-TEMPLATE.md  (updated)
├── sections/                      (unchanged)
├── reference/                     (unchanged)
├── requests/                      (plan output directory)
└── README.md                      (updated)
```

---

## Command Comparison: Claude Code → Qwen Code

| Claude Code | Qwen Code | Notes |
|-------------|-----------|-------|
| `claude` | `qwen` | CLI command |
| `claude --model opus` | `qwen --model [deep-reasoning]` | Model selection |
| `.claude/commands/` | `.qwen/commands/` | Commands directory |
| `.claude/agents/` | `.qwen/agents/` | SubAgent definitions |
| `.claude/skills/` | `.qwen/skills/` | Skills directory |
| Subagents | SubAgents | Qwen's multi-agent system |
| Sonnet/Opus | Qwen3-Coder | Model family |
| web_search tool | web_search tool | Same capability |
| — | Plan Mode (`/plan`) | Qwen native feature |

---

## Workflow Examples

### Standard Planning Workflow

```bash
# 1. Start Qwen Code
qwen

# 2. Load context
> /prime

# 3. Plan feature
> /planning user-authentication

# 4. Fresh session for execution
qwen
> /execute requests/user-authentication-plan.md

# 5. Review and commit
> /code-review
> /commit
```

### Swarm Mode (Parallel Execution)

```bash
# Plan with swarm decomposition
> /planning complex-feature --swarm

# Execute with parallel coordination
> /swarm complex-feature
```

### Skill Usage

```bash
# Invoke planning methodology skill
> skill: "planning-methodology"

# Use during planning for guidance
> /planning feature-x
> skill: "planning-methodology" # Reference methodology
```

---

## Model Strategy

| Phase | Recommended Model | Why |
|-------|-------------------|-----|
| `/planning` | Deep reasoning model | Better feature scoping, edge case detection |
| `/execute` | Default Qwen model | Follows plans well, cost-effective |
| `/code-review` | Default (via SubAgents) | 4 parallel agents, specialized focus |
| `/commit`, `/prime` | Default Qwen model | General-purpose tasks |

---

## Token Budget

| Component | Tokens | Loading |
|-----------|--------|---------|
| CLAUDE.md + 6 sections | ~2K | Auto-loaded |
| Commands | varies | On invocation |
| Reference guides | varies | On-demand |
| Templates | varies | On-demand |
| **Typical session** | **<10K** | Leaves ~100K+ for work |

---

## Migration Notes

### For Existing Users

1. **Directory rename**: `.claude/` → `.qwen/`
2. **Command syntax**: `claude` → `qwen`
3. **Agent terminology**: "subagents" → "SubAgents"
4. **Model references**: Opus/Sonnet → Qwen3-Coder/deep reasoning

### Breaking Changes

- Archon MCP integration removed (use `web_search`/`web_fetch` tools)
- Hook system may differ (check Qwen Code docs for SessionStart hooks)
- Settings file location: `.qwen/settings.json` vs `.claude/settings.json`

### Preserved Concepts

- PIV Loop methodology (unchanged)
- 6-phase planning process (unchanged)
- Template-driven execution (unchanged)
- 7-field atomic tasks (unchanged)
- Context engineering pillars (unchanged)

---

## Next Steps

1. **Test the workflow**: Run `/prime` and `/planning` on a small feature
2. **Verify SubAgents**: Confirm all 12 agents work correctly
3. **Test Plan Mode**: Use `/plan` for structured planning
4. **Validate Skills**: Test `planning-methodology` skill invocation
5. **Update documentation**: Add Qwen-specific examples to reference guides

---

## References

- [Qwen Code Documentation](https://qwenlm.github.io/qwen-code-docs/)
- [Getting Started](https://qwenlm.github.io/qwen-code-docs/en/user-guide/quickstart/)
- [SubAgents](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/subagents/)
- [Skills](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/skills/)
- [Commands](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/commands/)
- [Settings](https://qwenlm.github.io/qwen-code-docs/en/user-guide/configuration/settings/)
- [Approval Mode](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/approval-mode/)
- [MCP](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/mcp/)
- [LSP](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/lsp/)
- [Token Caching](https://qwenlm.github.io/qwen-code-docs/en/user-guide/features/token-caching/)
- [IDE Integration (VS Code)](https://qwenlm.github.io/qwen-code-docs/en/user-guide/vscode/)
- [IDE Integration (Zed)](https://qwenlm.github.io/qwen-code-docs/en/user-guide/zed-ide/)
- [IDE Integration (JetBrains)](https://qwenlm.github.io/qwen-code-docs/en/user-guide/jetbrains-ides/)
- [GitHub Actions](https://qwenlm.github.io/qwen-code-docs/en/user-guide/github-actions/)
- Qwen Code CLI: `npm i @qwen-code/qwen-code@latest -g`
- SubAgent system: `general-purpose` type with Qwen3-Coder
- Skills: `skill: "skill-name"` syntax for capability invocation
