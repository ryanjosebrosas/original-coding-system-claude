### Extending the PIV Loop with Parallel Workers

Subagents are isolated AI instances with custom system prompts that run in their own context window. They're not critical to the PIV Loop but are a powerful addition for parallelizing research, isolating context-heavy tasks, and building specialized AI workers. Think of them as "specialized employees" — each with a focused job description and their own workspace.

### What Subagents Are

- Isolated context windows with custom system prompts
- The main agent delegates work via the Task tool
- Each subagent works independently and returns results to the main agent
- Really just another markdown file — a prompt in your prompt toolbox
- Lives in `.claude/agents/` (project) or `~/.claude/agents/` (personal)

Subagents are not a new concept — the `/planning` command already uses them. Phases 2 and 3 launch Explore and general-purpose Task agents in parallel for research. The subagents deep dive guide makes this pattern explicit and teaches you to create your own.

### The Context Handoff Mental Model

```
You → Main Agent → Subagent → Main Agent → You
         ↓              ↓
    Handoff #1     Handoff #2
   (Can lose       (Can lose
    context)        context)
```

Two handoff points where context can be lost. The main agent summarizes YOUR request for the subagent (Handoff 1). The subagent summarizes ITS findings for the main agent (Handoff 2). Solution: obsessively control output formats to minimize information loss at both handoffs.

### When to Use Subagents

| Great For | Not Ideal For |
|-----------|---------------|
| Parallel research (codebase + docs simultaneously) | Simple sequential tasks |
| Parallel research (5-10 simultaneous explorations) | Priming (context gets lost in handoff) |
| Code review with controlled feedback | Tasks requiring ALL context, not summaries |
| System compliance checks across modules | Quick targeted changes |
| Plan vs execution analysis | Tasks needing iterative back-and-forth |
| Context-heavy tasks that would pollute main thread | Single-file focused edits |

### Parallel Execution

Up to 10 concurrent subagents — this is the real power. Instead of one agent researching 5 aspects sequentially, launch 5 agents each researching one aspect simultaneously. Results return to the main conversation when complete.

Warning: many agents returning detailed results can consume significant main context. Keep agent outputs concise, or use file-based reports where agents save findings to disk instead of returning them inline.

### Agent Teams (Coordinated Multi-Agent Implementation)

Agent Teams are a separate capability from subagents. They enable **two-way communication** between Claude Code instances via a shared task list and mailbox. The lead agent orchestrates teammates using **contract-first spawning** — upstream agents publish interface contracts before downstream agents begin.

Key difference: subagents provide **isolation** (one-way results back to main), Agent Teams provide **collaboration** (shared tasks, inter-agent messaging, contract relay).

| Aspect | Subagents | Agent Teams |
|--------|-----------|-------------|
| Communication | One-way (results to main) | Two-way (shared task list + mailbox) |
| Coordination | Main agent manages | Lead orchestrates via delegate mode |
| File isolation | None | Via worktrees (auto-created) |
| Token cost | Low | 2-4x higher |
| Best for | Research, analysis, code review | Coordinated implementation |

**Rule of thumb**: Subagents for research, Agent Teams for implementation. Don't use Agent Teams for tasks that don't require inter-agent coordination — it wastes tokens.

See `reference/agent-teams-overview.md` for the full Agent Teams guide.

### Output Format: The Primary Control Lever

The output format in your subagent's system prompt is the MOST critical part. It controls what the main agent sees and how it responds. Make outputs:

- **Structured and parsable** — headers, tables, severity levels
- **Include metadata** — files reviewed, line numbers, severity
- **Explicit about next steps** — what should the main agent do with results?
- **Easy to combine** — with other agents/commands downstream

Critical pattern: include "instruct the main agent to NOT start fixing issues without user approval" in your output format. Without this, the main agent may automatically act on all findings when you just wanted a report.

### Creating Custom Subagents

File location: `.claude/agents/*.md` (project) or `~/.claude/agents/*.md` (personal). Structure: YAML frontmatter + markdown body. The markdown body IS the system prompt.

Key frontmatter fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase-with-hyphens) |
| `description` | Yes | When to use — guides autonomous delegation |
| `model` | No | haiku, sonnet, opus (default: inherits from parent) |
| `tools` | No | Tool list or `["*"]` (default: inherits all) |

Two creation methods: manual (create the `.md` file yourself) or `/agents` command (Claude generates the agent for you). Use `templates/AGENT-TEMPLATE.md` for the full design guide.

### The Agent Design Framework

Five components every effective agent needs:

1. **Role Definition** — clear identity and specialized purpose
2. **Core Mission** — why this agent exists (singular focus)
3. **Context Gathering** — what files/info does it need?
4. **Analysis Approach** — specific steps to accomplish the mission
5. **Output Format** — structured, parsable results for downstream use

See `templates/AGENT-TEMPLATE.md` for the complete framework with starter template.

### Agents + Commands: Working Together

Two integration patterns:

- **Command invokes agent**: A slash command instructs the main agent to use a specific subagent, then acts on results (e.g., "use code-reviewer agent, then fix critical issues only")
- **Agent produces artifact for command**: A subagent saves a report file that a subsequent command consumes (e.g., agent writes review → `/code-review-fix` reads it)

The `/planning` command already uses this pattern — launching Explore and general-purpose agents in parallel for research. You can build the same pattern into your own commands.

### Built-in Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| Explore | Haiku | Read-only | File discovery, codebase search |
| Plan | Inherits | Read-only | Codebase analysis for planning |
| General-purpose | Inherits | All | Complex research, multi-step tasks |

Already used in `/planning` command (Phases 2 & 3 launch Explore + general-purpose in parallel).

**Model selection for agents**: When choosing `model` in frontmatter (haiku, sonnet, opus), see `reference/multi-model-strategy.md` for cost-performance trade-offs and task routing guidance.

### Pre-installed Agents

12 agents are pre-installed in `.claude/agents/` across 4 categories (research, code review, utility, specialist).

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| research-codebase | Haiku | Read, Glob, Grep | File discovery, pattern extraction |
| research-external | Sonnet | Read, Glob, Grep, WebSearch, WebFetch | Documentation search, best practices |
| code-review-type-safety | Haiku | Read, Glob, Grep, Bash | Type annotations, type checking |
| code-review-security | Haiku | Read, Glob, Grep, Bash | Security vulnerabilities |
| code-review-architecture | Haiku | Read, Glob, Grep | Architecture compliance |
| code-review-performance | Haiku | Read, Glob, Grep | Performance issues |
| plan-validator | Haiku | Read, Glob, Grep | Plan structure validation |
| test-generator | Haiku | Read, Glob, Grep | Test case suggestions |

These are distinct from Built-in agents above — Built-in agents are always available, example agents require user activation. Example agents use cost-optimized model selection (7 Haiku + 1 Sonnet).

### Agents vs Skills vs Commands

| Aspect | Commands | Skills | Subagents |
|--------|----------|--------|-----------|
| What | Saved prompts | Knowledge directories | Separate AI instances |
| Who invokes | User (`/command`) | User or auto-load | User or auto-delegate |
| Context | Main conversation | Main conversation | Own isolated context |
| Best for | Workflows, automation | Conventions, procedures | Parallel work, isolation |

Use ALL together: commands orchestrate, skills provide knowledge, agents do the work.

### Trust Progression (Complete)

```
Manual → Commands → Chained → Subagents → Worktrees → Agent Teams → Remote
  ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑
```

Before creating subagents: your manual prompts for the task work reliably. Before parallelizing: your single-agent workflow produces consistent results. Don't skip stages.

### Reference Files

- `templates/AGENT-TEMPLATE.md` — Design guide for creating subagents
- `reference/subagents-guide.md` — Detailed creation walkthrough, frontmatter reference, advanced patterns
- Load when: creating a new subagent, debugging agent handoffs, designing parallel workflows
