# System Mode Agents

5 parallel agents for methodology/documentation projects.

## Agent 1: Commands Inventory (Sonnet)

**subagent_type**: general-purpose
**model**: sonnet
**description**: Inventory slash commands

Analyze commands via python .codex/skills/prime-context/scripts/list_commands.py

## Agent 2: Agents Inventory (Sonnet)

Read .claude/agents/README.md and catalog agents by category.

## Agent 3: Project Structure (Haiku)

Glob for .md files in root, sections/, reference/, templates/, requests/.

## Agent 4: Memory Context (Haiku)

Read memory.md if it exists.

## Agent 5: Git State (Haiku)

Run python .codex/skills/prime-context/scripts/git_state.py
