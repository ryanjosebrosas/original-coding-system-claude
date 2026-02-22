#!/usr/bin/env python3
"""Git operations for commit command."""
import subprocess
import sys

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def get_changed_files():
    """Get list of changed files."""
    return run('git status --short').splitlines()

def get_diff(files=None):
    """Get diff of changes."""
    cmd = 'git diff HEAD'
    if files:
        cmd += ' -- ' + ' '.join(files)
    return run(cmd)

def stage_files(files=None):
    """Stage files for commit."""
    if files:
        subprocess.run(['git', 'add'] + files, check=True)
    else:
        subprocess.run(['git', 'add', '.'], check=True)
    return True

def commit(message):
    """Create commit with message."""
    subprocess.run(['git', 'commit', '-m', message], check=True)
    return run('git rev-parse --short HEAD')

def get_commit_info():
    """Get last commit info."""
    hash_short = run('git rev-parse --short HEAD')
    message = run('git log -1 --format=%s')
    stats = run('git show --stat --format=')
    return {'hash': hash_short, 'message': message, 'stats': stats}

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        for f in get_changed_files():
            print(f)
    elif cmd == 'info':
        info = get_commit_info()
        print(f"Hash: {info['hash']}")
        print(f"Message: {info['message']}")
