---
description: Safely merge feature branches from worktrees with validation gates
argument-hint: [branch1] [branch2] ... [branchN] (2-10 branches)
allowed-tools: Bash(git:*), Bash(pytest:*), Bash(mypy:*), Bash(pyright:*), Bash(pwd:*), AskUserQuestion, Read
---

# Merge Worktrees

Merge N feature branches from worktrees with full testing and validation.

**Safety First**: Uses temporary integration branch. Main branch only updated after ALL validations pass.

## Parameters

- **Branches**: $ARGUMENTS (2-10 branch names, space-separated, required)
- Minimum 2 branches required
- Examples:
  - Two: `/merge-worktrees feature/search feature/export`
  - Three: `/merge-worktrees feature/search feature/export feature/analytics`
  - Many: `/merge-worktrees feature/search feature/export feature/analytics feature/notifications`

## Steps

### Step 1: Verify Preconditions

1. Parse $ARGUMENTS into a list of branch names
2. Count branches (N). If N < 2: Error — "At least 2 branches required"
3. If N > 10: Error — "Maximum 10 branches supported"
4. Verify NOT inside a worktree subdirectory

```bash
[[ $(pwd) =~ /worktrees/ ]] && echo "ERROR: Must run from main repository root" && exit 1
```

5. For EACH branch: verify it exists

```bash
# For each branch in the list:
git rev-parse --verify {branch} || { echo "ERROR: Branch {branch} does not exist"; exit 1; }
```

6. Store current branch name for later:

```bash
CURRENT_BRANCH=$(git branch --show-current)
```

7. Report: "Current branch: $CURRENT_BRANCH. Will merge: {list all N branches}"

**If any verification fails**: Stop execution, report the error, provide instructions to fix.

---

### Step 2: Create Integration Branch

```bash
git checkout -b integration-{first_branch}-to-{last_branch}
echo "✓ Created integration branch: integration-{first_branch}-to-{last_branch}"
```

Example for 3 branches (feature/search, feature/export, feature/analytics):
`integration-feature/search-to-feature/analytics`

**Why temporary branch?** Testing happens here. If anything fails, we can delete this branch without affecting the main branch.

---

### Step 3: Sequential Merge with Validation

For EACH branch (in the order provided):

#### Merge branch {i+1} of N: {branch_name}

```bash
git merge {branch_name} --no-ff -m "merge: integrate {branch_name}"
```

**`--no-ff` (no fast-forward) is critical**: Preserves feature branch history even if merge is trivial. Makes it clear what commits belong to which feature.

**If conflicts occur**:

Stop execution and report:
```
✗ Conflicts detected during merge of {branch_name} (branch {i+1} of N)

Files with conflicts:
  {list conflicted files from git status}

Previous merges completed: {list branches 1 through i-1, or "none" if first branch}

Resolution steps:
  1. Fix conflicts in the listed files
  2. git add <resolved-files>
  3. git commit
  4. Re-run: /merge-worktrees {all branches}

To abort and start over:
  git merge --abort
  git checkout $CURRENT_BRANCH
  git branch -D integration-{first_branch}-to-{last_branch}
```

#### Test after merge {i+1}

```bash
pytest -v || {
  echo "✗ Tests failed after merging {branch_name} (branch {i+1} of N)"
  echo "Rollback:"
  echo "  git checkout $CURRENT_BRANCH"
  echo "  git branch -D integration-{first_branch}-to-{last_branch}"
  exit 1
}
echo "✓ Tests passed after merging {branch_name} ({i+1}/{N})"
```

**Note**: Replace `pytest` with your project's test command (`npm test`, `cargo test`, etc.)

[Repeat merge + test for each remaining branch...]

---

### Step 4: Run Full Validation Suite

After all N branches merged successfully, run complete validation:

```bash
# Run tests
echo "Running final test suite..."
pytest -v || {
  echo "✗ Final tests failed after all merges"
  echo "Rollback:"
  echo "  git checkout $CURRENT_BRANCH"
  echo "  git branch -D integration-{first_branch}-to-{last_branch}"
  exit 1
}

# Run type checkers
echo "Running mypy..."
mypy app/ || {
  echo "✗ Type check failed (mypy)"
  echo "Rollback:"
  echo "  git checkout $CURRENT_BRANCH"
  echo "  git branch -D integration-{first_branch}-to-{last_branch}"
  exit 1
}

echo "Running pyright..."
pyright app/ || {
  echo "✗ Type check failed (pyright)"
  echo "Rollback:"
  echo "  git checkout $CURRENT_BRANCH"
  echo "  git branch -D integration-{first_branch}-to-{last_branch}"
  exit 1
}

echo "✓ All validation passed"
```

**Note**: Customize validation commands for your project:
- Tests: `pytest` → `npm test`, `cargo test`, `go test`, etc.
- Type checking: `mypy/pyright` → `tsc`, `flow`, language-specific tools
- Additional: Linting, formatting, security scans as needed

**Critical rule**: ALL validations must pass before continuing. No exceptions.

---

### Step 5: Merge to Original Branch

```bash
git checkout $CURRENT_BRANCH
git merge integration-{first_branch}-to-{last_branch} --no-ff -m "merge: integrate features from {first_branch} to {last_branch}"
echo "✓ Merged to $CURRENT_BRANCH"
```

**Only reached if**: All N features merged successfully AND all validations passed.

---

### Step 6: Cleanup Integration Branch

```bash
git branch -d integration-{first_branch}-to-{last_branch}
echo "✓ Cleaned up integration branch"
```

**`-d` (not `-D`)**: Safe delete. Git will prevent deletion if branch has unmerged commits (extra safety check).

---

### Step 7: Ask About Worktree Cleanup

Use AskUserQuestion tool:

**Question**: "Remove all N worktrees and delete feature branches?"

**Options**:
1. **"Yes, clean up everything"** (recommended)
   - Removes all worktrees
   - Deletes all feature branches
   - Keeps the codebase clean

2. **"No, keep them for now"**
   - Worktrees remain for continued development
   - Branches remain for reference
   - User cleans up manually later

**If user chooses "Yes"**:

```bash
# For each branch:
git worktree remove worktrees/{branch_name}
git branch -d {branch_name}
```

```
✓ Removed all worktrees and deleted all feature branches
```

**If user chooses "No"**:

```
Worktrees still active:
[For each branch:]
  - worktrees/{branch_name} (branch: {branch_name})

To clean up manually later:
[For each branch:]
  git worktree remove worktrees/{branch_name}
  git branch -d {branch_name}
```

---

## Success Output

```
✓ Integration branch created: integration-{first_branch}-to-{last_branch}
[For each branch:]
✓ Merged {branch_name} ({i+1}/{N})
✓ Tests passed after merge {i+1}
✓ All validation passed (pytest, mypy, pyright)
✓ Merged to {original_branch}
✓ Cleaned up integration branch

[If worktrees removed]
✓ Removed all worktrees and deleted all feature branches

[If worktrees kept]
Worktrees still active:
[For each branch:]
  - worktrees/{branch_name} (branch: {branch_name})

To clean up manually:
[For each branch:]
  git worktree remove worktrees/{branch_name}
  git branch -d {branch_name}

All N features successfully integrated into {original_branch}!
```

---

## Failure Output

When any step fails:

```
✗ Merge failed at step: {step_name}

Error: {error_details}

Current state:
  - On branch: integration-{first_branch}-to-{last_branch}
  - Original branch: {original_branch}
  - Branches merged so far: {list successfully merged branches, or "none"}
  - Branch that failed: {branch_name} ({i+1} of N)
  - Branches not yet attempted: {list remaining branches}

To rollback:
  git checkout {original_branch}
  git branch -D integration-{first_branch}-to-{last_branch}

To continue after fixing:
  1. Resolve the issue ({specific guidance based on failure type})
  2. Re-run: /merge-worktrees {all branches}
```

**Partial merge failure** (e.g., branch 3 of 5 fails):
- Branches 1-2 already merged to integration branch
- Branch 3 failed (conflicts or test failure)
- Branches 4-5 not yet attempted
- Provide rollback to clean state OR continue-after-fix instructions

---

## Error Handling

**Conflict during merge**:
- Stop execution immediately
- List conflicted files
- Report which branch caused the conflict and how many merges completed
- Provide resolution instructions (fix → add → commit → retry)
- Offer abort instructions

**Missing branch**:
- Verify all branches exist before starting (Step 1)
- Provide clear error message with the branch name that doesn't exist

**Wrong directory**:
- Check not running from inside `worktrees/` subdirectory
- Require execution from main repository root

**Test failures**:
- Provide rollback instructions (checkout original → delete integration branch)
- Show which tests failed and error details
- Report which branch's merge caused the failure

**Type check failures**:
- Same rollback pattern as test failures
- Show which type checker failed (mypy vs pyright)
- Display error output for debugging

---

## Notes

**Why `--no-ff` (No Fast-Forward)?**
- Preserves feature branch history in Git graph
- Makes it clear which commits belong to which feature
- Enables easier rollback if needed (revert the merge commit)
- Follows Git best practices for feature integration

**Why Temporary Integration Branch?**
- Test merges without affecting main branch
- Roll back easily if anything fails (just delete branch)
- Original branch only updated after ALL validation passes
- Industry-standard safe merging pattern

**Why Test After Each Merge?**
- Catch issues early (fail fast principle)
- If branch 3 breaks tests, no point merging branches 4-5
- Narrows down which feature caused the problem
- Saves time by not running full suite on known-broken code

**Integration Branch Naming**:
- Uses first-to-last pattern: `integration-{first}-to-{last}`
- Stays readable regardless of how many branches are merged
- Example: `integration-feature/search-to-feature/notifications` (not a long list)

**Project-Agnostic Template**:
Users customize validation commands:
- Python: `pytest`, `mypy`, `pyright`
- Node.js: `npm test`, `tsc --noEmit`
- Rust: `cargo test`, `cargo clippy`
- Go: `go test ./...`, `golangci-lint run`

**Worktree Cleanup Decision**:
- Use AskUserQuestion for user preference (not hardcoded)
- Some users want to keep worktrees for continued iteration
- Some users want clean repository state
- Both choices are valid — let user decide

**Safety Layers**:
1. Verify preconditions (all branches exist, correct directory)
2. Use temporary integration branch (not main)
3. Test after each merge (fail fast)
4. Run full validation suite (comprehensive check)
5. Only merge to main after all checks pass
6. Provide rollback instructions on every failure

**When to Use This Command**:
- After implementing features in parallel worktrees
- All features are complete and locally tested
- Ready to integrate into main codebase
- Want automated validation before merge

**When NOT to Use**:
- Features still in development (not ready for integration)
- High merge conflict risk (overlapping changes)
- Want to merge features one at a time (use `git merge` directly)
- Testing manually before automation (merge manually first)
