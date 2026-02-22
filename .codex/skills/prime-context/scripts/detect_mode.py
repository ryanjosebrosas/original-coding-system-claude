#!/usr/bin/env python3
from pathlib import Path
CODE_DIRS = ["src","app","frontend","backend","lib","api","server","client"]

for d in CODE_DIRS:
    if Path(d).exists(): print("codebase"); exit()
print("system")
