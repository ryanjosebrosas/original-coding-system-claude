# SubAgents

SubAgent definitions for specialized tasks.

## Agent Catalog

### Research Agents
| Agent | Purpose |
|-------|---------|
| `research/research-codebase.md` | Codebase exploration with file:line references |
| `research/research-external.md` | External documentation research with web search/fetch |

### Code Review Agents
| Agent | Purpose |
|-------|---------|
| `code-review/code-review-architecture.md` | Design patterns and conventions review |
| `code-review/code-review-security.md` | Security vulnerability detection |
| `code-review/code-review-type-safety.md` | Type annotations and checking |
| `code-review/code-review-performance.md` | Performance and scalability review |

### Utility Agents
| Agent | Purpose |
|-------|---------|
| `utility/plan-validator.md` | Plan quality validation (1-10 scoring) |
| `utility/test-generator.md` | Test case generation from changed code |

### Specialist Agents
| Agent | Purpose |
|-------|---------|
| `specialist/specialist-devops.md` | CI/CD, Docker, infrastructure |
| `specialist/specialist-data.md` | Database design, migrations, queries |
| `specialist/specialist-copywriter.md` | UX writing, microcopy |
| `specialist/specialist-tech-writer.md` | API documentation, technical guides |

### Swarm Agents
| Agent | Purpose |
|-------|---------|
| `swarm/swarm-coordinator.md` | Multi-agent orchestration and task decomposition |
| `swarm/swarm-worker.md` | Focused subtask execution with file reservations |

## Usage

Reference these agents in commands and plans:

```bash
# Use an agent in a command
> /swarm my-task  # Uses swarm-coordinator

# Reference in a plan
See: .qwen/04-agents/code-review/code-review-security.md
```

## Creating New Agents

Use the template:
```bash
cp .qwen/03-templates/agents/AGENT-TEMPLATE.md .qwen/04-agents/<category>/my-agent.md
```

## Related Directories

- **[03-templates/agents](../03-templates/agents/)** — Agent template
- **[05-commands](../05-commands/)** — Commands that use these agents
- **[06-skills](../06-skills/)** — Skills that coordinate agents
