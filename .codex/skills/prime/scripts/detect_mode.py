#!/usr/bin/env python3
"""Detect project mode: System vs Codebase."""
from pathlib import Path
import sys

CODE_DIRS = ['src', 'app', 'frontend', 'backend', 'lib', 'api', 'server', 'client']

def detect_mode(root='.'):
    for d in CODE_DIRS:
        p = Path(root) / d
        if p.exists() and any(p.iterdir()):
            return 'codebase'
    return 'system'

if __name__ == '__main__':
    print(detect_mode(sys.argv[1] if len(sys.argv) > 1 else '.'))
