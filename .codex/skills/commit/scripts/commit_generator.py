#!/usr/bin/env python3
"""Generate conventional commit messages."""
import re
from pathlib import Path

def detect_type(files_changed):
    """Detect commit type from changed files."""
    files_str = ' '.join(files_changed).lower()
    
    if any(x in files_str for x in ['test', 'spec']):
        return 'test'
    if any(x in files_str for x in ['doc', 'readme', '.md']):
        return 'docs'
    if any(x in files_str for x in ['refactor', 'restructure']):
        return 'refactor'
    if 'fix' in files_str:
        return 'fix'
    if 'feat' in files_str or 'add' in files_str:
        return 'feat'
    return 'chore'

def detect_scope(files_changed):
    """Detect scope from file paths."""
    scopes = set()
    for f in files_changed:
        parts = Path(f).parts
        if len(parts) > 0:
            scopes.add(parts[0])
    return ','.join(scopes) if scopes else None

def generate_message(commit_type, scope, description):
    """Generate conventional commit message."""
    if scope:
        return f"{commit_type}({scope}): {description}"
    return f"{commit_type}: {description}"

if __name__ == '__main__':
    import sys
    files = sys.argv[1:]
    commit_type = detect_type(files)
    scope = detect_scope(files)
    print(f"Type: {commit_type}")
    print(f"Scope: {scope}")
