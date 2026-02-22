#!/usr/bin/env python3
"""Validate task completion."""
import subprocess

def run_validation(cmd):
    """Run validation command and return success."""
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.returncode == 0, result.stdout.decode(), result.stderr.decode()

def validate_all(commands):
    """Run all validation commands."""
    results = []
    for cmd in commands:
        success, stdout, stderr = run_validation(cmd)
        results.append({
            'command': cmd,
            'success': success,
            'output': stdout if success else stderr
        })
    return results

if __name__ == '__main__':
    import sys
    cmds = sys.argv[1:]
    for result in validate_all(cmds):
        status = 'PASS' if result['success'] else 'FAIL'
        print(f"[{status}] {result['command']}")
