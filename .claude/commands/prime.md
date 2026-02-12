---
description: Prime agent with codebase understanding
---

# Prime: Load Project Context

## Objective

Build comprehensive understanding of the codebase by analyzing structure, documentation, and key files.

## Process

### 1. Analyze Project Structure

List all tracked files:
!`git ls-files`

### 2. Read Core Documentation

- Read project rules: @CLAUDE.md
- If `sections/` directory exists, read the section files referenced in CLAUDE.md
- Read README files at project root and major directories
- Read any architecture documentation

### 3. Identify Key Files

Based on the structure, identify and read:
- Main entry points (main.py, index.ts, app.py, etc.)
- Core configuration files (pyproject.toml, package.json, tsconfig.json)
- Key model/schema definitions
- Important service or controller files

### 4. Understand Current State

Check recent activity:
!`git log -10 --oneline`

Check current branch and status:
!`git status`

### 5. Recall Project Memory (if mem0 available)

Search mem0 for project-relevant memories to carry forward:

1. Search for recent decisions and lessons:
   - Query: "{project-name} decisions lessons"
2. Search for architecture patterns and gotchas:
   - Query: "{project-name} patterns gotchas"
3. Search for recent session context:
   - Query: "{project-name} recent changes"

Include up to 10 most relevant memories in the output report. If mem0 is not available or returns no results, skip this section gracefully.

### 5b. Search Archon Knowledge Base (if available)

If Archon RAG is available, search for project-relevant documentation:

1. Get available sources: `rag_get_available_sources()`
2. Search for project setup and architecture docs:
   - Query: "{project-name} setup"
   - Query: "{primary-framework} best practices"
3. Include top 3-5 relevant results in the output report

If Archon RAG is not available, skip this section gracefully.

## Output Report

Provide a concise summary covering:

### Project Overview
- Purpose and type of application
- Primary technologies and frameworks
- Current version/state

### Architecture
- Overall structure and organization
- Key architectural patterns identified
- Important directories and their purposes

### Tech Stack
- Languages and versions
- Frameworks and major libraries
- Build tools and package managers
- Testing frameworks

### Core Principles
- Code style and conventions observed
- Documentation standards
- Testing approach

### Current State
- Active branch
- Recent changes or development focus
- Any immediate observations or concerns

### Memory Context (from mem0)
- Key decisions from past sessions
- Known gotchas and lessons
- Relevant patterns established
- (If no memories found, note "No mem0 memories found — this is a fresh project or mem0 is unavailable")

### Knowledge Base Context (from Archon RAG)
- Relevant documentation sources found
- Key articles or guides applicable to this project
- (If Archon RAG unavailable, note "No Archon RAG available — skip knowledge base search")

**Make this summary easy to scan - use bullet points and clear headers.**
