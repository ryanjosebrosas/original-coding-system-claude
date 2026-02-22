#!/usr/bin/env python3
"""Get git state."""
import subprocess

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return r.stdout.strip()

print('BRANCH:', run('git rev-parse --abbrev-ref HEAD'))
status = run('git status --short')
print('STATUS:', status if status else 'clean')
print('RECENT_COMMITS:')
for line in run('git log -10 --oneline').splitlines()[:10]:
    if line:
        print(f'  - {line}')
