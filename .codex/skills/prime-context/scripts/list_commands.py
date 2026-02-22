#!/usr/bin/env python3
import re
from pathlib import Path
cmds = []
for f in sorted(Path(".claude/commands").glob("*.md")):
    m = re.search(r"^description:\s*(.+)$", f.read_text(encoding="utf-8"), re.M)
    if m: cmds.append((f.stem, m.group(1).strip()))
print("COMMANDS:"); [print(f"- {n}: {d}") for n,d in cmds]
