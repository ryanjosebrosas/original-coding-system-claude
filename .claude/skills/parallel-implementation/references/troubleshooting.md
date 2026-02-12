# Troubleshooting — Common Issues and Fixes

> This reference is loaded on-demand during skill execution (Tier 3).

---

## Worktree Creation Fails

**Symptom**: `git worktree add` errors with "branch already exists" or "is already checked out"

**Cause**: Branch name conflicts with existing branch, or the branch is checked out in another worktree.

**Fix**:
```bash
# Check existing worktrees
git worktree list

# Check existing branches
git branch -a

# Remove stale worktree references
git worktree prune

# Use a different branch name, or remove existing worktree first
git worktree remove worktrees/{name}
```

---

## Dependency Sync Fails in Worktree

**Symptom**: `npm install`, `uv sync`, or similar fails inside a worktree directory.

**Cause**: Lock file mismatch, missing environment variables, or incomplete worktree setup.

**Fix**:
```bash
# Ensure you're inside the worktree directory
cd worktrees/{name}

# Verify lock file exists (should be inherited from main repo)
ls package-lock.json  # or uv.lock, poetry.lock

# Clean and retry
rm -rf node_modules/ && npm install
# or: rm -rf .venv/ && uv sync
```

---

## Parallel Execution Hits Rate Limits

**Symptom**: One or more `claude -p` processes fail with rate limit errors.

**Cause**: Too many parallel API requests from simultaneous Claude Code instances.

**Fix**:
- Reduce parallel count (start with 2-3 instead of 5+)
- Stagger launches: add `sleep 30` between process starts
- Use different API keys for different processes (if available)
- Switch to sequential execution for the failed features:
  ```bash
  cd worktrees/{failed-feature}
  claude
  /execute requests/{feature}-plan.md
  ```

---

## Merge Conflicts During Integration

**Symptom**: `git merge` reports conflicts during `/merge-worktrees`.

**Cause**: Two features modified the same file (typically a registration point like routes or config).

**Fix**:
1. Check which files conflict: `git status`
2. **Registration point conflicts** (routes, configs):
   - Usually trivial — both features add entries to the same file
   - Accept both additions, verify order is correct
   - `git add {resolved-file} && git commit`
3. **Logic conflicts** (shared utilities, services):
   - These should not happen with proper overlap detection
   - Requires manual resolution — understand both changes
   - Consider reverting and implementing one feature at a time
4. **Rollback if needed**:
   ```bash
   git merge --abort
   git checkout $CURRENT_BRANCH
   git branch -D integration-{first}-to-{last}
   ```

---

## Validation Failures After Merge

**Symptom**: Tests or type checking fails after merging features.

**Cause**: Features work individually but have integration issues (incompatible shared state, conflicting configurations, type mismatches).

**Fix**:
1. Identify which merge introduced the failure (the gated merge process tells you)
2. Check the test output for specific failures
3. Common causes:
   - Both features imported the same dependency at different versions
   - Both features modified a shared type definition differently
   - Port conflicts between services
4. Fix the integration issue on the integration branch
5. If unfixable, rollback:
   ```bash
   git checkout $CURRENT_BRANCH
   git branch -D integration-{first}-to-{last}
   ```
6. Re-merge features one at a time to isolate the issue

---

## `claude -p` Process Hangs or Times Out

**Symptom**: A background `claude -p` process doesn't complete after expected time.

**Cause**: Agent stuck in a loop, waiting for input, or hitting max turns without completing.

**Fix**:
```bash
# Check if process is still running
ps aux | grep "claude -p"

# Kill the stuck process
kill $PID_{i}

# Check the log file for clues
cat logs/{feature}.json | jq '.result // .error'
```

**Prevention**:
- Use `--max-turns 50` to prevent infinite loops
- Ensure plans are comprehensive enough that the agent doesn't need to ask questions
- Verify the plan's VALIDATE commands are achievable in the worktree environment

---

## When to Fall Back to Sequential Execution

Switch from parallel to sequential when:

- **Rate limits**: API throttling causes consistent failures
- **Resource constraints**: Machine runs out of RAM/CPU with 3+ agents
- **Repeated merge conflicts**: Features aren't as isolated as planned
- **Complex integration**: Features have subtle dependencies not caught by overlap detection
- **First-time usage**: Run one parallel pair successfully before scaling to 3+

**Sequential fallback**:
```bash
# Instead of parallel, execute one at a time:
cd worktrees/{feature-1}
claude
/execute requests/{feature-1}-plan.md
# Wait for completion, then:
cd ../../worktrees/{feature-2}
claude
/execute requests/{feature-2}-plan.md
```

The worktrees are still useful for isolation — you just don't run them simultaneously.
