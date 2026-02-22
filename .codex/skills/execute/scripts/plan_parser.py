#!/usr/bin/env python3
"""Parse and execute implementation plans."""
import re
from pathlib import Path

def parse_plan(filepath):
    """Parse plan file and extract tasks."""
    content = Path(filepath).read_text(encoding='utf-8')
    
    # Extract feature name
    feature_match = re.search(r'##\s*Feature Name[\s\S]*?\*\*([^*]+)\*\*', content)
    feature_name = feature_match.group(1).strip() if feature_match else 'unknown'
    
    # Extract tasks
    tasks = []
    task_pattern = r'-\s*\[\s*([ x])\s*\]\s*(.+)'
    for match in re.finditer(task_pattern, content):
        tasks.append({
            'done': match.group(1).strip() == 'x',
            'description': match.group(2).strip()
        })
    
    # Extract validation commands
    validations = []
    val_section = re.search(r'##\s*Validation Commands[\s\S]*?(?=##|$)', content)
    if val_section:
        for line in val_section.group(0).splitlines():
            if line.strip().startswith('- '):
                validations.append(line.strip()[2:])
    
    return {
        'feature': feature_name,
        'tasks': tasks,
        'validations': validations
    }

def is_plan_series(filepath):
    """Check if file contains PLAN-SERIES marker."""
    content = Path(filepath).read_text(encoding='utf-8')
    return '<!-- PLAN-SERIES -->' in content

def extract_subplans(filepath):
    """Extract sub-plan paths from series."""
    content = Path(filepath).read_text(encoding='utf-8')
    pattern = r'\[.+?\]\(requests/(.+?)\)'
    return re.findall(pattern, content)

if __name__ == '__main__':
    import sys
    plan = parse_plan(sys.argv[1])
    print(f"Feature: {plan['feature']}")
    print(f"Tasks: {len(plan['tasks'])}")
    print(f"Validations: {len(plan['validations'])}")
