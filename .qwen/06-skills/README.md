# Skills

Skills are modular capabilities that extend Qwen Code's effectiveness.

## Available Skills

| Skill | File | Purpose |
|-------|------|---------|
| `planning-methodology` | `planning-methodology.md` | 6-phase feature planning methodology |
| `swarm-coordination` | `swarm-coordination.md` | Multi-agent coordination for parallelizable work |

## How Skills Work

- Skills are **model-invoked** — AI autonomously decides when to use them
- Each skill is a package containing `SKILL.md` with instructions
- Manual invocation: `/skills <skill-name>` with autocomplete

## Usage

```bash
# Manual invocation
> /skills planning-methodology
> /skills swarm-coordination
```

## Skill Locations

- **Project skills**: `.qwen/06-skills/` (this directory)
- **Personal skills**: `~/.qwen/skills/` (user-specific)

## Creating New Skills

Skills follow a specific structure. See the Qwen Code documentation for skill creation guidelines.

## Related Directories

- **[04-agents](../04-agents/)** — Agents coordinated by skills
- **[05-commands](../05-commands/)** — Commands that invoke skills
