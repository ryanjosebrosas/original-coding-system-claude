# Slash Commands

Command definitions for Qwen Code slash commands.

## Command Catalog

| Command | File | Purpose |
|---------|------|---------|
| `/prime` | `prime.md` | Load project context using parallel agents |
| `/planning` | `planning.md` | Create comprehensive implementation plan |
| `/execute` | `execute.md` | Implement from a plan document |
| `/swarm` | `swarm.md` | Orchestrate multi-agent swarm |
| `/code-review` | `code-review.md` | Technical code review with parallel agents |
| `/code-review-fix` | `code-review-fix.md` | Fix issues from code review |
| `/commit` | `commit.md` | Create git commit with conventional message |
| `/create-pr` | `create-pr.md` | Create GitHub PR from current branch |
| `/create-prd` | `create-prd.md` | Generate PRD from vibe planning |
| `/rca` | `rca.md` | Root cause analysis for GitHub issue |
| `/implement-fix` | `implement-fix.md` | Implement fix from RCA document |
| `/system-review` | `system-review.md` | Analyze implementation vs plan |
| `/execution-report` | `execution-report.md` | Generate implementation report |
| `/end-to-end-feature` | `end-to-end-feature.md` | Full feature development workflow |
| `/init-c` | `init-c.md` | Create modular QWEN.md global rules |
| `/agents` | `agents.md` | Create new subAgent definition |

## Usage

```bash
# In Qwen Code chat
> /prime
> /planning user-authentication
> /execute requests/user-authentication-plan.md
> /swarm add-user-authentication
```

## Creating New Commands

Use the template:
```bash
cp .qwen/03-templates/commands/COMMAND-TEMPLATE.md .qwen/05-commands/my-command.md
```

## Related Directories

- **[03-templates/commands](../03-templates/commands/)** — Command template
- **[04-agents](../04-agents/)** — Agents used by commands
- **[06-skills](../06-skills/)** — Skills invoked by commands
