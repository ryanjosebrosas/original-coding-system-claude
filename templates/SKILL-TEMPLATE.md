# Creating a New Skill

Skills extend commands with directory structure and progressive disclosure.

## When to Create a Skill

Use a Skill (not a Command) when:
- Workflow requires supporting files (templates, examples, references)
- Content exceeds 250 lines with distinct sections
- You want auto-loading based on task context
- Better organization via subdirectories improves clarity

Use a Command (not a Skill) when:
- Simple, single-file workflow
- Under 200 lines
- No supporting files needed
- User-only invocation (no auto-loading)

## Directory Structure

```
.claude/skills/
  {skill-name}/           # Kebab-case, descriptive
    SKILL.md              # Entry point (required)
    references/           # Detailed guides (optional)
      detailed-guide.md
    examples/             # Usage examples (optional)
      good-example.md
      bad-example.md
    scripts/              # Executable scripts (optional)
      setup.sh
```

## SKILL.md Format

### Frontmatter (YAML)

```yaml
---
description: "Brief description for auto-loading decision (~100 tokens)"
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Read, Bash(git:*), Edit  # Optional
disable-model-invocation: false  # Set true to prevent auto-loading
user-invocable: true  # Set false to hide from / menu
---
```

### Body (Markdown)

Follow INPUT → PROCESS → OUTPUT framework:

```markdown
# Skill Name

## INPUT
- What context does the AI need?
- What should the user provide?

## PROCESS
1. Step 1 with validation
2. Step 2 with validation
3. Reference supporting files: `@references/detailed-guide.md`

## OUTPUT
- What format should results take?
- What files are created/modified?
```

## Progressive Disclosure

- **Tier 1 (Metadata)**: `description` field (~100 tokens) loaded at session start
- **Tier 2 (Full SKILL.md)**: Loaded when skill invoked or auto-loaded by AI
- **Tier 3 (Supporting files)**: Loaded when explicitly referenced in SKILL.md

## Example: Planning Methodology Skill

```
.claude/skills/planning-methodology/
  SKILL.md                    # 80-100 lines (high-level 6-phase overview)
  references/
    STRUCTURED-PLAN-TEMPLATE.md  # Template loaded during Phase 4
    PHASE-1-SCOPING.md           # Deep-dive loaded on-demand
    PHASE-2-RESEARCH.md          # Deep-dive loaded on-demand
  examples/
    good-plan-500-lines.md       # Example of well-scoped plan
    bad-plan-overscoped.md       # Example of what to avoid
```

**Token savings**: ~100 tokens upfront (description) vs ~600 tokens (full planning.md command).

## Testing Your Skill

1. Invoke explicitly: `/skill-name [args]`
2. Check context: `/context` to see token usage
3. Verify auto-loading: Start conversation with task description, see if skill loads
4. Test supporting files: Reference `@references/file.md` in SKILL.md, verify it loads

## Backward Compatibility

- Existing commands in `.claude/commands/` continue working
- Skills in `.claude/skills/` coexist with commands
- If both exist with same name, Skill takes precedence
- No migration required — Skills are additive
