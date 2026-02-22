#!/usr/bin/env python3
"""List available commands."""
import re
from pathlib import Path

def list_commands(cmd_dir='.claude/commands'):
    cmds = []
    for f in sorted(Path(cmd_dir).glob('*.md')):
        content = f.read_text(encoding='utf-8')
        m = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        if m:
            cmds.append((f.stem, m.group(1).strip()))
    return cmds

if __name__ == '__main__':
    for name, desc in list_commands():
        print(f'{name}: {desc}')
