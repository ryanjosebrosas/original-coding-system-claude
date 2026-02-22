# Codebase Mode Agents

6 parallel agents for code projects.

## Agent 1: Architecture and Structure (Sonnet)

**subagent_type**: general-purpose
**model**: sonnet
**description**: Analyze project architecture

Run git ls-files, 	ree -L 3, detect architectural patterns.

## Agent 2: Tech Stack (Sonnet)

Read package.json, pyproject.toml, Cargo.toml, go.mod.
Extract language, framework, dependencies, scripts.

## Agent 3: Code Conventions (Sonnet)

Read 1-2 representative files, main entry point, schema definitions.
Identify naming, error handling, organization patterns.

## Agent 4: README (Haiku)

Read README.md for purpose, capabilities, setup.

## Agent 5: Memory Context (Haiku)

Read memory.md if exists.

## Agent 6: Git State (Haiku)

Run git commands for branch, status, recent commits.
