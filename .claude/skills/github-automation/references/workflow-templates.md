# Workflow Templates — Customization Guide

> This reference is loaded on-demand during skill execution (Tier 3).

---

## Prompt Template Adaptation (Local to GitHub)

GitHub prompt templates are adapted from local commands with three key differences:

### 1. Extra INPUT Variables

GitHub Actions provides environment variables not available locally:

| Variable | Source | Example |
|----------|--------|---------|
| `$REPOSITORY` | `github.repository` | `owner/repo` |
| `$ISSUE_NUMBER` | `github.event.issue.number` | `42` |
| `$ISSUE_TITLE` | Issue title | `"Add search feature"` |
| `$ISSUE_BODY` | Issue description | Full markdown body |
| `$BRANCH_NAME` | Generated from issue | `claude/issue-42-add-search` |
| `$BASE_BRANCH` | Default branch | `main` or `master` |
| `$TRIGGERED_BY` | Comment author | `username` |

### 2. Configuration Flags

GitHub prompts include operational flags:

```yaml
# In the workflow YAML:
env:
  MAX_ITERATIONS: "3"        # Fix cycles before giving up
  AUTHORIZED_USERS: "user1"  # Who can trigger
  AUTO_MERGE: "false"        # Auto-merge after review passes
  SKIP_TESTS: "false"        # Skip validation (not recommended)
```

### 3. Adjusted OUTPUT

GitHub prompts end with PR creation instead of local commit:
- Local: `git commit -m "feat: ..."`
- GitHub: Create branch, push, `gh pr create`

---

## Variable Substitution in Prompts

Use shell-style variables in prompt templates:

```markdown
# In .github/workflows/prompts/end-to-end-feature-github.md

## Context
- Repository: $REPOSITORY
- Issue: #$ISSUE_NUMBER — $ISSUE_TITLE
- Branch: $BRANCH_NAME

## Task
Read the issue description and implement the feature:

$ISSUE_BODY
```

The workflow YAML passes these as environment variables:

```yaml
- name: Run Claude Code
  env:
    REPOSITORY: ${{ github.repository }}
    ISSUE_NUMBER: ${{ github.event.issue.number }}
    ISSUE_TITLE: ${{ github.event.issue.title }}
    ISSUE_BODY: ${{ github.event.issue.body }}
```

---

## Label-Based Routing

Labels on issues determine which prompt template loads:

```yaml
# In the workflow YAML:
- name: Determine prompt
  run: |
    if [[ "${{ contains(github.event.issue.labels.*.name, 'bug') }}" == "true" ]]; then
      PROMPT_FILE=".github/workflows/prompts/bug-fix-github.md"
    elif [[ "${{ contains(github.event.issue.labels.*.name, 'enhancement') }}" == "true" ]]; then
      PROMPT_FILE=".github/workflows/prompts/end-to-end-feature-github.md"
    else
      PROMPT_FILE=".github/workflows/prompts/implement-fix-github.md"
    fi
```

### Supported Label Routes

| Label | Prompt Template | Behavior |
|-------|----------------|----------|
| `bug` | `bug-fix-github.md` | RCA then fix |
| `enhancement` | `end-to-end-feature-github.md` | Full PIV Loop |
| `claude-fix` | `implement-fix-github.md` | Direct implementation |
| `claude-create` | `end-to-end-feature-github.md` | Plan + implement |

---

## Customizing Authorized Users

Control who can trigger the AI agent:

```yaml
env:
  AUTHORIZED_USERS: "alice,bob,charlie"

# In the job:
- name: Check authorization
  run: |
    COMMENTER="${{ github.event.comment.user.login }}"
    if [[ ",$AUTHORIZED_USERS," != *",$COMMENTER,"* ]]; then
      echo "Unauthorized user: $COMMENTER"
      exit 0  # Silent exit, no error
    fi
```

**Why this matters**: Without authorization, anyone who can comment on issues could trigger expensive API calls.

---

## Iteration Limit Configuration

The `MAX_ITERATIONS` controls how many fix cycles the agent attempts:

```yaml
env:
  MAX_ITERATIONS: "3"

# In the agent prompt:
- name: Run with iteration limit
  run: |
    for i in $(seq 1 $MAX_ITERATIONS); do
      echo "Iteration $i of $MAX_ITERATIONS"
      # Run agent, check if tests pass
      # Break if successful
    done
```

| Value | Behavior | Cost Impact |
|-------|----------|-------------|
| 1 | Single attempt, no retries | Lowest |
| 3 | Standard — retry twice on failure | Moderate (recommended) |
| 5 | Thorough — good for complex fixes | Higher |
| 10 | Maximum effort | Highest |

---

## CodeRabbit Configuration Options

The `.coderabbit.yaml` file controls review behavior:

```yaml
# Basic configuration
reviews:
  auto_review:
    enabled: true
    # Review all PRs automatically

  path_filters:
    - "!**/*.md"          # Skip markdown files
    - "!**/test/**"       # Skip test files (optional)
    - "!.github/**"       # Skip workflow files

  # Review depth
  profile: "assertive"    # Options: chill, default, assertive

# Language settings
language: "en-US"

# Custom instructions
instructions:
  - "Focus on security vulnerabilities"
  - "Check for proper error handling"
  - "Verify type safety"
```

### Review Profiles

| Profile | Behavior |
|---------|----------|
| `chill` | Only flag critical issues |
| `default` | Balanced review coverage |
| `assertive` | Thorough review, more suggestions |

---

## Example: Complete Workflow YAML

```yaml
name: Claude Fix
on:
  issues:
    types: [labeled]
  issue_comment:
    types: [created]

jobs:
  fix:
    if: |
      (github.event.action == 'labeled' &&
       contains(github.event.label.name, 'claude')) ||
      (github.event.action == 'created' &&
       contains(github.event.comment.body, '@claude-fix'))
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude Code
        uses: anthropics/claude-code-action@v1
        with:
          prompt_file: .github/workflows/prompts/implement-fix-github.md
        env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

This is a minimal example. See `reference/github-workflows/` for production-ready workflow files.
