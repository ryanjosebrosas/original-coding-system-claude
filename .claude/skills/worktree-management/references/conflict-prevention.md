# Conflict Prevention — Strategies for Parallel Implementation

> This reference is loaded on-demand during skill execution (Tier 3).

Git worktrees provide code isolation — agents in different worktrees cannot see or modify each other's files. However, conflicts can emerge at merge time. These strategies prevent conflicts before they happen.

---

## The Scope Boundary Principle

Each parallel agent should have a clear, non-overlapping scope:

```
Agent 1 OWNS features/search/    — creates and modifies files here
Agent 2 OWNS features/export/    — creates and modifies files here
NEITHER agent modifies shared files during implementation
```

This works naturally with vertical slice architecture. When planning parallel features, verify each feature's plan only touches files within its own slice.

**The rule**: If two plans modify the same file (beyond registration points), don't parallelize those features.

---

## Shared File Strategy (Registration Points)

Registration points are shared files where multiple features need to add entries (e.g., route definitions, tool registrations, config entries).

### During Implementation
- Agents do NOT modify the shared file
- Each agent implements their feature in isolation
- Registration happens during the merge phase

### During Merge
- The merge step handles registration conflicts
- Typical conflict: two features add a line to the same file
- Git auto-merges if additions are in different locations
- Manual resolution needed if additions are at the same line

### Best Practice: Design for Append-Friendly Registration
- Structure config and route files so new entries are appended at the end
- This reduces positional conflicts between parallel features
- Example: alphabetical ordering or section-based organization

---

## Research Agent Deduplication

When running parallel research agents (e.g., during `/planning`), partition work by scope to prevent duplicate findings:

### Codebase Research Agents
- Assign each agent to different directories or file patterns
- Agent 1 searches `features/`, Agent 2 searches `shared/`, Agent 3 searches `tests/`
- Prevents redundant findings that waste context window

### External Research Agents
- Assign each agent to different documentation sources or topics
- Agent 1 researches framework docs, Agent 2 researches library docs
- Prevents duplicate results from overlapping searches

---

## Detecting Overlap Before Parallelizing

### 4-Step Verification Process

**Step 1: List target files from each plan**
- Read "New Files to Create" and "STEP-BY-STEP TASKS" sections
- Extract every file path that will be created or modified

**Step 2: Check for intersection**
- Compare file lists across all plans
- Any file appearing in 2+ plans is a potential conflict

**Step 3: Classify overlaps**
- **Registration points** (routes, configs, registries): Expected and handled at merge time
- **Shared logic files** (utilities, services, models): Dangerous — requires sequential implementation

**Step 4: Decide**
- Registration-only overlaps: Safe to parallelize
- Logic file overlaps: Implement those features sequentially
- Mixed: Remove overlapping features from parallel set, implement separately

---

## Vertical Slice Architecture Prerequisite

Parallel implementation requires features isolated in independent modules:

```
project/
  app/
    core/           # Shared infrastructure (rarely modified)
    features/       # Vertical slices
      tool_a/       # Agent 1 works here exclusively
      tool_b/       # Agent 2 works here exclusively
      tool_c/       # Agent 3 works here exclusively
    shared/         # Shared utilities (rarely modified)
```

### Why It Works
- Each feature is self-contained in its own directory
- Agents never touch each other's files during development
- Merge conflicts are limited to predictable registration points

### Without Vertical Slices
- Agents may modify the same utility files, services, or configs
- Merge conflicts become frequent and hard to resolve
- The merge step becomes a manual conflict-resolution exercise
- Sequential implementation is safer

### Designing for Parallelization
When writing your PRD and architecture decisions, consider:
- Can features be implemented independently?
- What shared files would multiple features touch?
- Can registration points be designed for minimal conflict?

---

## Summary: Three Layers of Protection

1. **Code isolation (automatic)**: Git worktrees give each agent its own file system
2. **Scope boundaries (planning phase)**: Verify plans only modify files within their slice
3. **Merge-time validation (automatic)**: `/merge-worktrees` tests after each merge, catching integration issues immediately
