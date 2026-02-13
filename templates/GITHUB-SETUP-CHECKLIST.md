# GitHub Actions Setup Checklist

> Step-by-step guide for adding automated code review (CodeRabbit) and AI coding agent workflows (Claude Code) to your GitHub repository.
> This enables automated PR reviews, review-fix loops, and issue-triggered PIV Loops.

---

## Prerequisites

- [ ] GitHub repository (public or private)
- [ ] Claude Code installed and authenticated locally (for OAuth token generation)
- [ ] Repository admin access (to install Apps, configure secrets, and permissions)
- [ ] CodeRabbit account (free for open source, 14-day Pro trial for private repos)

---

## Step 1: Install CodeRabbit GitHub App

1. Go to [CodeRabbit on GitHub Marketplace](https://github.com/marketplace/coderabbit-ai)
2. Click **Install** (or **Configure** if already installed)
3. Choose which repositories to grant access to
4. Confirm permissions (read/write: code, commit statuses, issues, pull requests)

After installation, CodeRabbit will automatically review every new PR. No workflow YAML needed for reviews.

---

## Step 2: Add `.coderabbit.yaml` to Your Repo

Copy the template configuration to your project root:

```bash
cp .coderabbit.yaml your-project-root/.coderabbit.yaml
```

Customize key settings:
- `reviews.profile` — `"chill"` (fewer comments) or `"assertive"` (thorough)
- `reviews.auto_review.enabled` — `true` to auto-review all PRs
- `reviews.auto_review.drafts` — `false` to skip draft PRs

See the [CodeRabbit documentation](https://docs.coderabbit.ai/) for full configuration reference.

---

## Step 3: Add Claude Code OAuth Token Secret

1. Run `claude setup-token` locally (requires Claude Code installed and authenticated)
2. Copy the generated OAuth token
3. Go to your repository on GitHub
4. Navigate to **Settings** → **Secrets and variables** → **Actions**
5. Click **New repository secret**
6. Add: Name = `CLAUDE_CODE_OAUTH_TOKEN`, Value = the token from step 1

---

## Step 4: Enable PR Creation

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Check **"Allow GitHub actions to create and approve pull requests"**
4. Click **Save**

> **Organization repos**: You may also need to enable this at the organization level under Organization Settings → Actions → General.

---

## Step 5: Copy Workflow Files

Copy the workflow YAML files to your repository:

```bash
# Create the workflows directory
mkdir -p .github/workflows

# Copy the review-fix loop workflow (auto-applies CodeRabbit suggestions)
cp reference/github-workflows/claude-fix-coderabbit.yml .github/workflows/

# Copy the issue-triggered fix workflow
cp reference/github-workflows/claude-fix.yml .github/workflows/
```

---

## Step 6: Copy Prompt Templates

Copy the GitHub-adapted prompt templates:

```bash
# Create the prompts directory
mkdir -p .github/workflows/prompts

# Copy prompt templates (used by claude-fix.yml for issue-triggered fixes)
cp .github/workflows/prompts/*.md your-project/.github/workflows/prompts/
```

The three prompt files:
- `end-to-end-feature-github.md` — Full PIV Loop for enhancement issues
- `bug-fix-github.md` — RCA + fix for bug issues
- `prime-github.md` — Context loading for GitHub Actions

---

## Step 7: Customize for Your Project

1. **Update authorized users** — In `claude-fix.yml`, replace `your-github-username` with your actual GitHub username(s)
2. **Customize CodeRabbit** — Adjust `.coderabbit.yaml` settings for your project
3. **Customize prompts** — Add project-specific instructions, tech stack details, and conventions to the prompt templates
4. **Adjust labels** — Ensure your issue labels match what the workflows expect (`enhancement`, `bug`, etc.)
5. **Tune iteration limit** — Adjust `MAX_ITERATIONS` in `claude-fix-coderabbit.yml` (default: 3)

---

## Step 8: Push and Verify

```bash
git add .coderabbit.yaml .github/workflows/ .github/workflows/prompts/
git commit -m "feat: add CodeRabbit + Claude Code automated review-fix loop"
git push
```

Verify:
1. Go to your repository → **Actions** tab
2. You should see the new workflows listed
3. They won't run yet — they trigger on reviews and comments

---

## Step 9: Test the Review-Fix Loop

1. Create a new branch and make a change with an intentional issue (e.g., unused variable, missing error handling)
2. Open a Pull Request
3. Watch CodeRabbit post a review (usually within 1-2 minutes)
4. Watch the Claude Code fix workflow trigger and apply suggestions
5. Watch CodeRabbit re-review the fixed code
6. Verify the loop stops after `MAX_ITERATIONS` or when no more issues are found

For issue-triggered fixes:
1. Create a new issue (e.g., "Update README formatting")
2. Add the `enhancement` label
3. Comment: `@claude-create`
4. Go to **Actions** tab and watch the workflow run
5. Check the issue for the agent's response

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| CodeRabbit doesn't review PRs | Check App installation: Settings → Integrations → CodeRabbit |
| Reviews are too noisy | Set `reviews.profile: "chill"` in `.coderabbit.yaml` |
| Claude Code workflow doesn't trigger | Verify `CLAUDE_CODE_OAUTH_TOKEN` secret exists; check Actions tab for errors |
| Comment not recognized | Ensure comment starts with exact trigger (e.g., `@claude-fix`) |
| Can't create PR | Enable PR creation in Settings → Actions → General |
| Infinite loop | Check `MAX_ITERATIONS` setting; verify `[claude-fix]` commit prefix |
| Free tier after trial | Private repos need Lite/Pro plan for full CodeRabbit reviews |
| Workflow fails silently | Check Actions tab → click the failed run → view logs |
| Org-level block | Enable Actions permissions at the organization level too |
