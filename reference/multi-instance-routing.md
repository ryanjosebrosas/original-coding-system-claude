# Multi-Instance Routing Guide

> **Load when**: You have multiple Claude accounts and want to route different tasks to different instances for cost optimization, load distribution, or team collaboration

---

## What Is Multi-Instance Routing?

Instead of using different models (Haiku/Sonnet/Opus), you use **different Claude accounts/instances** to distribute work across:
- Multiple API keys (distribute load, avoid rate limits)
- Team member accounts (track who did what)
- Specialized instances (cheap tasks vs premium tasks)
- Cost centers (bill different work to different accounts)

**Key difference from multi-model**:
- Multi-model: Same account, different model intelligence (Haiku/Sonnet/Opus)
- Multi-instance: Different accounts, potentially different billing/limits/permissions

---

## Your Available Instances

Based on your `claude-list` output:

| Instance | Account | Best For |
|----------|---------|----------|
| `claude1` | Main Account | **Planning, PIV Loop, main orchestration** |
| `claude2` | design@brainforge.ai | **Vital Sonnet work** (load balanced with claude3) |
| `claude3` | Ryan.Brosas@brainforge.ai | **Vital Sonnet work** (load balanced with claude2) |
| `claude-zai` | Z.AI GLM (Cheap Tasks) | **Spammable, non-critical tasks** |

**Key insight**: `claude2` and `claude3` distribute vital Sonnet-level work to avoid hitting rate limits on a single account.

---

## Strategic Routing

### Strategy 1: Criticality-Based Routing (RECOMMENDED)

Route based on how vital the task is:

```
Main Conversation (claude1 - Main Account)
  ├─> Type Safety Review (claude-zai, Haiku) ─── Non-critical, spammable
  ├─> Security Review (claude2, Sonnet) ───────── VITAL, can't fail
  ├─> Architecture Review (claude2, Sonnet) ───── VITAL, design expertise
  └─> Performance Review (claude3, Sonnet) ────── VITAL, critical issues
```

**Routing rules**:
- `claude-zai` → Tasks where false negatives are acceptable
- `claude2/3` → Tasks where quality matters, can't afford to miss issues
- `claude1` → Orchestration, main work

**Use case**: Parallel code review with smart cost/quality tradeoffs

### Strategy 2: Load-Balanced Vital Work

Distribute Sonnet-level vital tasks across `claude2` and `claude3`:

```
Main Planning (claude1 - PIV Loop orchestration)
  ├─> Security Review (claude2 - Vital Sonnet work)
  ├─> Architecture Review (claude2 - Vital Sonnet work)
  └─> Performance Review (claude3 - Vital Sonnet work)
```

**Use case**: Avoid hitting rate limits on single account, distribute vital work across two instances

### Strategy 3: Load Distribution

Distribute parallel agents across instances to avoid rate limits:

```
Main Agent (claude1)
  ├─> Agent 1 (claude1)
  ├─> Agent 2 (claude2)
  ├─> Agent 3 (claude3)
  └─> Agent 4 (claude-zai)
```

**Use case**: High-volume parallel execution, avoid hitting API rate limits on single account

### Strategy 4: Combined Multi-Model + Multi-Instance

Best of both worlds:

```
Main Conversation (claude1, Sonnet)
  ├─> Type Safety (claude-zai, Haiku) ─── cheapest
  ├─> Security (claude-zai, Haiku) ────── cheapest
  ├─> Architecture (claude2, Sonnet) ──── design expertise
  └─> Performance (claude1, Opus) ─────── premium analysis
```

---

## How to Configure Agents for Specific Instances

### Method 1: Environment Variable (Per Session)

Set the instance before running commands:

```bash
# Use cheap instance for code review
export CLAUDE_INSTANCE=claude-zai
claude code-review

# Use main instance for planning
export CLAUDE_INSTANCE=claude1
claude planning "new feature"
```

### Method 2: Command Prefix

Prefix commands with specific instance:

```bash
claude-zai code-review          # Route to Z.AI cheap instance
claude1 planning "feature"      # Route to main account
claude2 design-review           # Route to design account
```

### Method 3: Agent Frontmatter (if supported)

Add instance to agent configuration:

```yaml
---
name: code-review-type-safety
model: haiku
instance: claude-zai  # Route to cheap instance
tools: ["Read", "Glob", "Grep", "Bash"]
---
```

**Note**: This requires Claude Code support for instance routing in agents. Check with `claude --help` if this is available.

### Method 4: Wrapper Scripts

Create routing scripts for common workflows:

```bash
# .claude/scripts/cheap-review.sh
#!/bin/bash
export CLAUDE_INSTANCE=claude-zai
claude code-review "$@"
```

Then use: `./claude/scripts/cheap-review.sh`

---

## Recommended Routing Rules

### Route to `claude-zai` (Spammable, Non-Critical):
- ✅ Type safety checks (helpful but not critical)
- ✅ Linting and formatting
- ✅ Simple refactoring (rename, extract)
- ✅ Test generation from patterns
- ✅ Documentation generation
- ✅ Search and analysis (grep, glob, read)
- ✅ Code style checks
- ❌ NOT security review (too vital!)
- ❌ NOT architecture review (consistency is vital)
- ❌ NOT performance review (critical issues can't be missed)

### Route to `claude1` (Main - Planning & PIV Loop):
- ✅ **Planning** (`/planning`) - Core PIV Loop
- ✅ **Implementation** (`/execute`) - Core PIV Loop
- ✅ **Main conversation orchestration** - Primary work
- ✅ **Commit messages and PR creation** - PIV Loop completion
- ✅ **Complex architecture decisions** (with Opus model)
- ✅ **End-to-end workflows** (`/end-to-end-feature`)

### Route to `claude2` (Vital Sonnet Work - Load Balanced):
- ✅ Security review (VITAL - can't miss vulnerabilities)
- ✅ Architecture review (VITAL - consistency + patterns)
- ✅ Any vital task requiring Sonnet
- ✅ Load distribution to avoid rate limits

### Route to `claude3` (Vital Sonnet Work - Load Balanced):
- ✅ Performance review (VITAL - critical issues)
- ✅ Complex code analysis
- ✅ Any vital task requiring Sonnet
- ✅ Load distribution to avoid rate limits

---

## Integration with Parallel Code Review

### Current Setup (Multi-Model Only)

```
Main Agent (Sonnet)
  ├─> Type Safety (Haiku)
  ├─> Security (Haiku)
  ├─> Architecture (Haiku)
  └─> Performance (Haiku)
```

### Enhanced Setup (Multi-Instance + Multi-Model)

```
Main Agent (claude1, Sonnet)
  ├─> Type Safety (claude-zai, Haiku) ──┐
  ├─> Security (claude-zai, Haiku) ─────┤  Routed to cheap instance
  ├─> Architecture (claude-zai, Haiku) ─┤  + using cheap model
  └─> Performance (claude-zai, Haiku) ──┘  = Maximum savings
```

**Combined savings**:
- Cheap model (Haiku): 70% cost reduction vs Sonnet
- Cheap instance (Z.AI GLM): Additional savings on top
- Parallel execution: 40-50% time savings

---

## Cost Optimization Examples

### Scenario 1: Code Review

**Without routing** (all on claude1):
- 4 agents × Sonnet cost × main account rate = $$$$

**With multi-model only** (all on claude1):
- 4 agents × Haiku cost × main account rate = $$ (70% savings)

**With multi-instance + multi-model**:
- 4 agents × Haiku cost × cheap instance rate = $ (80-90% savings)

### Scenario 2: Parallel Research

**Without routing**:
- 5 parallel agents on claude1 → hit rate limit, sequential fallback

**With multi-instance**:
- Distribute across claude1, claude2, claude3, claude-zai → no rate limits

---

## How to Implement

### Step 1: Test Instance Routing

Verify you can route commands:

```bash
claude-zai --version
claude1 --version
claude2 --version
claude3 --version
```

### Step 2: Update Code Review Agents

If agent frontmatter supports `instance` field, add it:

```yaml
---
name: code-review-type-safety
model: haiku
instance: claude-zai
tools: ["Read", "Glob", "Grep", "Bash"]
---
```

### Step 3: Create Routing Wrapper Scripts

```bash
mkdir -p .claude/scripts

# cheap-review.sh
echo '#!/bin/bash
export CLAUDE_INSTANCE=claude-zai
claude /code-review "$@"' > .claude/scripts/cheap-review.sh

chmod +x .claude/scripts/cheap-review.sh
```

### Step 4: Update Commands to Use Routing

Modify `/code-review` command to explicitly route to cheap instance:

```markdown
When parallel mode is enabled, route all 4 review agents to claude-zai instance for cost savings.

Launch agents with instance routing:
- claude-zai: code-review-type-safety
- claude-zai: code-review-security
- claude-zai: code-review-architecture
- claude-zai: code-review-performance
```

---

## Team Collaboration Patterns

### Pattern 1: Work Assignment

Route work to specific team member accounts:

```markdown
/planning → claude1 (main orchestration)
/execute backend → claude3 (Ryan's account - backend work)
/execute frontend → claude2 (design account - UI work)
/code-review → claude-zai (cheap automated review)
```

### Pattern 2: Approval Workflow

```
Developer creates PR → claude-zai reviews (cheap, fast)
  ↓
If issues found → claude1 analyzes (main account, detailed)
  ↓
Senior review needed → claude3 (team lead account)
```

### Pattern 3: Load Balancing

Distribute heavy parallel workloads:

```python
agents = [
    ('agent1', 'claude1'),
    ('agent2', 'claude2'),
    ('agent3', 'claude3'),
    ('agent4', 'claude-zai'),
    ('agent5', 'claude1'),  # Round-robin back
]
```

---

## Limitations & Considerations

### Rate Limits
- Each instance has its own rate limits
- Distributing work helps avoid hitting limits
- But adds coordination complexity

### Cost Tracking
- Work spread across accounts = harder to track total cost
- Use instance routing strategically, not randomly
- Document routing rules in CLAUDE.md

### Context Isolation
- Each instance is separate → no shared conversation history
- Plan must be explicit (agents can't reference main conversation context)
- Good for isolation, bad for context-heavy tasks

### Authentication
- Must authenticate each instance separately
- Credentials stored in separate `.claude-*` directories
- Ensure team members have access to their assigned instances

---

## When to Use Multi-Instance

**Use multi-instance when**:
- ✅ You have multiple accounts with different pricing
- ✅ You need to distribute load across rate limits
- ✅ You want team-based work attribution
- ✅ You want to isolate cheap tasks from premium tasks

**Stick with multi-model (single instance) when**:
- ❌ You only have one account
- ❌ Cost tracking across accounts is complex
- ❌ Team coordination overhead isn't worth it
- ❌ Rate limits aren't an issue

---

## Combining with Existing System

### Multi-Model Strategy (reference/multi-model-strategy.md)
- Haiku for pattern matching
- Sonnet for balanced work
- Opus for complex reasoning

### Multi-Instance Strategy (this guide)
- claude-zai for cheap repetitive tasks
- claude1 for main orchestration
- claude2/3 for team-specific work

### Combined Strategy
- `claude-zai + Haiku` = cheapest (code review)
- `claude1 + Sonnet` = default (planning, implementation)
- `claude1 + Opus` = premium (complex architecture)
- `claude2 + Sonnet` = specialized (design work)

---

## Quick Reference

```bash
# Check available instances
claude-list

# Route specific command
claude-zai /code-review
claude1 /planning "feature"
claude2 /design-review

# Set instance for session
export CLAUDE_INSTANCE=claude-zai
claude /code-review

# Wrapper script
./.claude/scripts/cheap-review.sh
```

---

## Next Steps

1. **Test routing**: Try `claude-zai --version` and other instances
2. **Update agents**: Add `instance: claude-zai` to code review agents if supported
3. **Create wrapper scripts**: For common cheap tasks
4. **Document routing rules**: Add to your project's CLAUDE.md
5. **Monitor costs**: Track savings from routing cheap tasks to claude-zai

---

## Questions to Investigate

- Does agent frontmatter support `instance` field?
- Can Task tool accept instance parameter?
- What's the pricing difference between instances?
- Do all instances have same rate limits?
- How to track which instance did what work?

Run `claude --help` and check agent documentation to answer these.
