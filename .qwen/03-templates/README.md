# Templates

Reusable templates for plans, agents, commands, and documentation.

## Contents by Category

### Plans (`plans/`)
| Template | Purpose |
|----------|---------|
| `STRUCTURED-PLAN-TEMPLATE.md` | Comprehensive feature plan (700-1000 lines) |
| `PLAN-OVERVIEW-TEMPLATE.md` | High-level plan overview |
| `SUB-PLAN-TEMPLATE.md` | Sub-plan for swarm decomposition |
| `VIBE-PLANNING-GUIDE.md` | Interactive vibe planning guide |

### Agents (`agents/`)
| Template | Purpose |
|----------|---------|
| `AGENT-TEMPLATE.md` | Create new subAgent definitions |

### Commands (`commands/`)
| Template | Purpose |
|----------|---------|
| `COMMAND-TEMPLATE.md` | Create new slash commands |

### Documentation (`documentation/`)
| Template | Purpose |
|----------|---------|
| `MEMORY-TEMPLATE.md` | Session memory and notes |
| `PRD-TEMPLATE.md` | Product Requirements Document |

## Usage

Use these templates as starting points for creating new artifacts:

```bash
# Create a new feature plan
cp .qwen/03-templates/plans/STRUCTURED-PLAN-TEMPLATE.md requests/my-feature-plan.md

# Create a new agent
cp .qwen/03-templates/agents/AGENT-TEMPLATE.md .qwen/04-agents/category/my-agent.md

# Create a new command
cp .qwen/03-templates/commands/COMMAND-TEMPLATE.md .qwen/05-commands/my-command.md
```

## Related Directories

- **[04-agents](../04-agents/)** — Agent definitions created from templates
- **[05-commands](../05-commands/)** — Command definitions created from templates
- **[08-outputs](../08-outputs/)** — Generated outputs (plans, PRDs)
