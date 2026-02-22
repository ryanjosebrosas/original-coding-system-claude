# Swarm Coordination

Multi-agent coordination for parallelizable work in Qwen Code.

## When to Use

Use swarm coordination when:
- **3+ files** need to be modified
- Work is **parallelizable** (frontend/backend/tests can proceed independently)
- **Specialized agents** are needed for different aspects
- **Time-to-completion** matters more than cost

**Avoid swarming for:**
- 1-2 file changes
- Tightly sequential work (B depends on A completing first)
- Simple fixes or single-feature implementations

## Agent Types

| Type | Role | File Access | MCP Tools | When to Use |
|------|------|-------------|-----------|-------------|
| **Coordinator** | Orchestrates swarm, decomposes tasks, reviews work | Read-only | Yes | Task planning, delegation, final review |
| **Worker** | Executes specific subtasks | Reserved files only | Yes | Implementation, testing, focused work |
| **Background Worker** | Static/background tasks | Reserved files only | No | Documentation, formatting, non-MCP work |

## File Reservations

Workers **must** reserve files before editing:

```
Reserve: src/auth/login.ts, src/auth/login.test.ts
```

This prevents multiple workers from modifying the same file simultaneously.

**Rules:**
- Coordinator never reserves files
- Workers release reservations automatically on completion
- If a worker needs additional files, it must reserve them before editing

## Workflow

### 1. Coordinator Setup

```markdown
# Swarm Plan

## Epic: [Epic Name]
**Goal**: [What this swarm achieves]

## Subtasks

### Subtask 1: [Title]
- **Files**: [file1.ts, file2.ts]
- **Worker**: [agent type or specialty]
- **Dependencies**: [none | subtask X]

### Subtask 2: [Title]
...

## Shared Context
[What all workers need to know about the epic]
```

### 2. Spawning Workers

**Parallel (independent tasks):**
Spawn multiple workers in a single message for independent work.

**Sequential (dependent tasks):**
Wait for each worker to complete before spawning the next.

### 3. Worker Protocol

1. **Initialize**: Load `QWEN.md` and project conventions
2. **Reserve files**: Declare which files you'll modify
3. **Execute**: Complete the subtask within scope
4. **Report**: Set status to `ready_for_review`
5. **Complete**: Release reservations

### 4. Progress Reporting

Report progress at key milestones:
- **25%**: Setup complete, beginning implementation
- **50%**: Core implementation done
- **75%**: Testing/polishing, nearly complete

### 5. Review & Merge

Coordinator reviews each worker's output:
- Verify all files are modified correctly
- Check for conflicts or issues
- Set status to `passed` or `failed`

## Worker Prompt Template

```markdown
## Task: [Subtask Title]

### Context
[Epic context and shared information]

### Files to Modify
- `file1.ts` - [what to implement]
- `file2.test.ts` - [tests to add]

### Requirements
1. [Specific requirement 1]
2. [Specific requirement 2]
3. [Specific requirement 3]

### Constraints
- Follow project conventions from `QWEN.md`
- Write tests for all new functionality
- Use existing patterns and utilities

### Output
1. Implement the required changes
2. Run tests and ensure they pass
3. Report: files modified, tests added, any issues encountered
```

## Common Patterns

### Feature Development Swarm

```
Coordinator
├── Worker: Database schema & migrations
├── Worker: API endpoints & business logic
├── Worker: Frontend components
└── Worker: Integration tests
```

### Code Review Swarm

```
Coordinator
├── Reviewer: Security vulnerabilities
├── Reviewer: Type safety
├── Reviewer: Performance
└── Reviewer: Architecture patterns
```

### Refactoring Swarm

```
Coordinator
├── Worker: Module A refactoring
├── Worker: Module B refactoring
└── Worker: Update shared utilities
```

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Over-swarming** | 10 workers for 5 files | Consolidate to 2-3 focused workers |
| **Unclear scope** | Workers modify overlapping files | Define clear file boundaries per worker |
| **Missing context** | Workers don't know about each other | Provide shared context in each subtask |
| **No review** | Coordinator doesn't validate output | Always review before marking complete |

## Best Practices

1. **Start small**: Begin with 2-3 workers, scale if needed
2. **Clear boundaries**: Each worker owns specific files
3. **Shared context**: Explain how subtasks relate to each other
4. **Sequential for dependencies**: Don't parallelize dependent work
5. **Review thoroughly**: Coordinator must validate all output

## Model Selection

| Worker Type | Recommended Model | Why |
|-------------|-------------------|-----|
| Implementation | Sonnet | Balanced reasoning + speed |
| Testing | Haiku | Pattern matching, cost-effective |
| Complex logic | Sonnet/Opus | Deep reasoning needed |
| Documentation | Haiku | Straightforward, low cost |

---

**Remember**: Swarming is about **parallelization + coordination**. Without both, you're just running multiple agents independently.
