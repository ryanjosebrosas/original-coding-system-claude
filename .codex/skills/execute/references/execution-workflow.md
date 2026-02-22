# Execution Workflow

## Step 1: Parse Plan

Use `scripts/plan_parser.py` to extract:
- Feature name
- Task list
- Validation commands

## Step 2: Execute Tasks

For each task:
1. Read task specification
2. Read existing files
3. Implement changes
4. Verify syntax/types
5. Mark complete

## Step 3: Validation

Run validation commands using `scripts/task_validator.py`.

## Step 4: Report

Save execution report to `requests/execution-reports/[feature]-execution-report.md`
