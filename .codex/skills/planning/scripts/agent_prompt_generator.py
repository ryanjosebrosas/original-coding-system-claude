#!/usr/bin/env python3
"""Generate agent prompts for planning."""
import sys

def agent_a_prompt(feature, systems):
    """Agent A: Similar implementations."""
    return f"""Find similar code for: {feature}
Systems: {systems}

Tasks:
1. Grep for relevant patterns
2. Find integration points
3. Identify files to modify
4. List new files needed

Return with file:line references."""

def agent_b_prompt(feature, systems):
    """Agent B: Project patterns."""
    return f"""Extract patterns for: {feature}

Read 2-3 files in {systems} area.
Extract:
- Naming conventions
- Error handling
- Type patterns
- Testing approach

Return with code snippets."""

if __name__ == '__main__':
    feature = sys.argv[1] if len(sys.argv) > 1 else 'feature'
    systems = sys.argv[2] if len(sys.argv) > 2 else 'system'
    print("=== AGENT A ===")
    print(agent_a_prompt(feature, systems))
    print("\n=== AGENT B ===")
    print(agent_b_prompt(feature, systems))
