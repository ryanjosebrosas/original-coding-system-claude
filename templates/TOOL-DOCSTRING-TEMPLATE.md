# Tool Docstring Template

> Use this when writing documentation for agent tools (MCP tools, function tools, etc.).
> Agent tool docstrings guide **when to use the tool and how** for LLM reasoning —
> NOT standard code docstrings for human developers.
>
> **Core Principle**: Element 3 ("Do NOT use this for") is the most important and
> most commonly missed. Without negative guidance, agents choose the wrong tool.

---

## The 7 Required Elements

| # | Element | Purpose |
|---|---------|---------|
| 1 | One-line summary | Clear primary purpose statement |
| 2 | "Use this when" | 3-5 specific scenarios (affirmative guidance) |
| 3 | "Do NOT use this for" | Redirect to OTHER tools (prevents confusion) |
| 4 | Args with WHY | Each param with type + guidance on different values |
| 5 | Returns | Format and structure details for parsing |
| 6 | Performance notes | Token usage, execution time, resource limits |
| 7 | Examples | 2-4 realistic scenarios (not "foo"/"bar") |

---

## Template

```python
def tool_name(param1: type, param2: type = default) -> ReturnType:
    """
    {Element 1: One-line summary of what this tool does.}

    Use this when:
    - {Scenario 1 — specific condition}
    - {Scenario 2 — specific condition}
    - {Scenario 3 — specific condition}

    Do NOT use this for:
    - {Anti-scenario 1} — use {other_tool} instead
    - {Anti-scenario 2} — use {other_tool} instead

    Args:
        param1: {type} — {WHY this param exists, guidance on values}
        param2: {type} — {default: X}. {When to change the default and why}

    Returns:
        {Format description}. Structure:
        - field1: {type} — {what it contains}
        - field2: {type} — {what it contains}

    Performance:
        - Token usage: {approximate tokens per call}
        - Execution time: {typical range}
        - Limits: {rate limits, max payload, etc.}

    Examples:
        # {Scenario description 1}
        tool_name("realistic/path/here.md", param2="value")

        # {Scenario description 2}
        tool_name("another/realistic/example.md")
    """
```

---

## Anti-Patterns and Fixes

### Vague guidance

```python
# BAD: "Use this when you need to work with notes."
# GOOD: "Use this when you need to read content of a single known note,
#        extract metadata from frontmatter, or verify a note exists."
```

### Missing negative guidance

```python
# BAD: No "Do NOT use" section
# GOOD: "Do NOT use this for searching notes (use obsidian_vault_query),
#        batch reading (use batch mode), or graph analysis (use obsidian_graph_analyze)"
```

### Toy examples

```python
# BAD: read_note("test.md"); read_note("foo.md")
# GOOD: read_note("daily/2025-01-15.md", response_format="minimal")  # Check daily note metadata
#        read_note("projects/website-redesign.md")  # Get project overview
```

---

## Tool Consolidation Principle

Fewer, smarter tools reduce agent error rates. Each tool call is an opportunity for the agent to make a mistake — minimize the number of calls needed per workflow.

**Fragmented** (agent must orchestrate 3 calls):
```python
read_note(path)                      # Tool 1
patch_note(path, old, new)           # Tool 2
update_metadata(path, metadata)      # Tool 3
```

**Consolidated** (single call):
```python
note_manage(path=path, operation="patch",
    find_replace=(old, new), metadata_updates=metadata)
```

When designing tools, ask: "Can the agent complete this workflow in fewer calls?"

---

> **Reference**: See `reference/planning-methodology-guide.md` Section 5 for detailed philosophy and additional examples.
