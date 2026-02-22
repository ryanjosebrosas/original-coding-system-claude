# Qwen Code Planning System — Final Implementation

Complete Qwen-optimized planning system based on official Qwen Code documentation.

---

## What Was Built

### 1. Command: `.qwen/commands/planning.md`

**Purpose**: Main planning command for comprehensive feature planning

**Key Features**:
- 6-phase planning methodology
- Parallel SubAgent research (2+ agents simultaneously)
- Swarm decomposition mode (`--swarm` flag)
- Skills integration for specialized capabilities
- `@file` and `@symbol` context references

**Usage**:
```bash
qwen
> /planning user-authentication
> /planning complex-feature --swarm
```

---

### 2. SubAgents: `.qwen/agents/` (12 files)

All agents use Qwen Code's SubAgent system with `general-purpose` type.

#### Research Agents (2)
| Agent | Purpose | Tools |
|-------|---------|-------|
| `research-codebase` | Codebase exploration | Read, Glob, Grep |
| `research-external` | Documentation research | Read, Glob, Grep, WebSearch, WebFetch |

#### Code Review Agents (4)
| Agent | Purpose |
|-------|---------|
| `code-review-architecture` | Architecture and pattern compliance |
| `code-review-type-safety` | Type annotations and checking |
| `code-review-security` | Security vulnerability detection |
| `code-review-performance` | Performance optimization |

#### Utility Agents (2)
| Agent | Purpose |
|-------|---------|
| `plan-validator` | Plan quality validation (1-10 scoring) |
| `test-generator` | Test case generation |

#### Specialist Agents (4)
| Agent | Expertise |
|-------|-----------|
| `specialist-devops` | CI/CD, Docker, infrastructure |
| `specialist-data` | Database design, ORM, migrations |
| `specialist-copywriter` | UX writing, microcopy |
| `specialist-tech-writer` | API documentation, technical guides |

---

### 3. Skill: `.qwen/skills/planning-methodology.md`

**Format**: Qwen Skills standard with YAML frontmatter

```yaml
---
name: planning-methodology
description: Systematic 6-phase feature planning methodology. Use when creating comprehensive implementation plans...
---
```

**Key Features**:
- Model-invoked (AI autonomously decides when to use)
- Manual invocation: `/skills planning-methodology`
- 6-phase process documentation
- Swarm decomposition guidance
- Quality checklist

---

### 4. Template: `templates/STRUCTURED-PLAN-TEMPLATE.md`

**Updates**:
- Qwen Code integration notes
- `@file:line` syntax for IDE navigation
- SubAgent references
- Skills integration

**Target Length**: 700-1000 lines minimum

---

### 5. Documentation Index: `QWEN-DOCUMENTATION-INDEX.md`

Complete reference to Qwen Code documentation:
- 70+ documentation pages indexed
- User Guide features and configuration
- Developer Guide SDKs and tools
- Direct links to all feature pages

---

## Qwen Code Integration (Verified from Official Docs)

### SubAgents
- **What they are**: Specialized agents that handle specific tasks within your workflow
- **Type**: `general-purpose` for research/review tasks
- **Tools available**: Read, Glob, Grep, Bash, WebSearch, WebFetch
- **Context**: Isolated per-agent context windows
- **Syntax**: `@file` and `@symbol` references

### Skills
- **What they are**: Modular capabilities that extend Qwen Code's effectiveness
- **File structure**: `SKILL.md` with YAML frontmatter + optional supporting files
- **Invocation**: 
  - Automatic (model-invoked based on description)
  - Manual: `/skills <skill-name>` with autocomplete
- **Locations**:
  - Personal: `~/.qwen/skills/<skill>/`
  - Project: `.qwen/skills/<skill>/`

### Settings
- **User settings**: `~/.qwen/settings.json`
- **Project settings**: `.qwen/settings.json`
- **Configuration layers**: Default → System → User → Project → CLI args
- **Key settings**: `model`, `tools`, `context`, `mcpServers`, `ui`

### Context Files
- **Default name**: `QWEN.md` (configurable via `context.fileName`)
- **Hierarchy**: Global (`~/.qwen/QWEN.md`) → Project root & ancestors
- **Commands**: `/memory refresh`, `/memory show`
- **Import syntax**: `@path/to/file.md`

### Tools Available
| Tool | Purpose |
|------|---------|
| File System | Read/write files |
| Multi-File Read | Analyze multiple files |
| Shell | Execute commands |
| Todo Write | Track tasks |
| Task | Manage work items |
| Web Fetch | Retrieve web content |
| Web Search | Search the internet |
| Memory | Store/retrieve information |
| MCP Servers | Connect external services |

---

## Workflow Examples

### Standard Planning
```bash
# 1. Install Qwen Code
npm install -g @qwen-code/qwen-code@latest

# 2. Start Qwen Code
cd your-project
qwen

# 3. Load context
> /prime

# 4. Plan feature
> /planning user-authentication

# 5. Fresh session for execution
qwen
> /execute requests/user-authentication-plan.md

# 6. Review and commit
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

### Skill Invocation
```bash
# Automatic (model decides)
"I need to plan a new feature"

# Manual
> /skills planning-methodology
```

---

## File Structure

```
opencode-coding-system/
├── .qwen/
│   ├── commands/
│   │   └── planning.md              # Main planning command
│   ├── agents/
│   │   ├── research-codebase.md
│   │   ├── research-external.md
│   │   ├── code-review-*.md         (4 files)
│   │   ├── plan-validator.md
│   │   ├── test-generator.md
│   │   └── specialist-*.md          (4 files)
│   └── skills/
│       └── planning-methodology.md  # Planning methodology skill
├── templates/
│   └── STRUCTURED-PLAN-TEMPLATE.md  # Updated for Qwen
├── sections/                         # Core rules (unchanged)
├── reference/                        # Deep guides (unchanged)
├── requests/                         # Plan output directory
├── QWEN-OPTIMIZATION.md             # Transformation summary
├── QWEN-DOCUMENTATION-INDEX.md      # Complete docs reference
└── README.md                         # Updated for Qwen Code
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

## Key Differences from Claude Code System

| Aspect | Claude Code | Qwen Code |
|--------|-------------|-----------|
| CLI command | `claude` | `qwen` |
| Directory | `.claude/` | `.qwen/` |
| Context file | `CLAUDE.md` | `QWEN.md` |
| Agents | subagents | SubAgents |
| Skills | `.claude/skills/` | `.qwen/skills/` (YAML frontmatter) |
| Settings | `.claude/settings.json` | `.qwen/settings.json` |
| Model family | Opus/Sonnet | Qwen3-Coder |
| Plan Mode | Custom | Native `/plan` (if available) |

---

## Official Documentation

All Qwen Code documentation: https://qwenlm.github.io/qwen-code-docs/en/

**Key Pages**:
- [Overview](https://qwenlm.github.io/qwen-code-docs/en/users/overview/)
- [QuickStart](https://qwenlm.github.io/qwen-code-docs/en/users/quickstart/)
- [SubAgents](https://qwenlm.github.io/qwen-code-docs/en/users/features/subagents/)
- [Skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/)
- [Commands](https://qwenlm.github.io/qwen-code-docs/en/users/features/commands/)
- [Settings](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)

See `QWEN-DOCUMENTATION-INDEX.md` for complete 70+ page index.

---

## Next Steps

1. **Test the workflow**: Run `/prime` and `/planning` on a small feature
2. **Verify SubAgents**: Confirm all 12 agents work correctly
3. **Test Skills**: Verify `planning-methodology` skill invocation
4. **Update reference guides**: Add Qwen-specific examples to `reference/`
5. **Create QWEN.md**: Add project-specific context file

---

## Installation

```bash
# Install Qwen Code
npm install -g @qwen-code/qwen-code@latest

# Clone this system
git clone https://github.com/ryanjosebrosas/opencode-coding-system.git
cd opencode-coding-system

# Create memory file
cp templates/MEMORY-TEMPLATE.md memory.md

# Start
qwen
> /prime
```
