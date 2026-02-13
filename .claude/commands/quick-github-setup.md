---
description: Quick setup for GitHub automation using existing scripts
argument-hint: [claude|codex|both]
---

# Quick GitHub Setup

**Agent**: $ARGUMENTS (default: both)

Run the setup scripts to configure GitHub automation in one command.

---

## PROCESS

### Step 1: Run Setup Scripts

```bash
# Determine which agent(s) to set up
AGENT="${ARGUMENTS:-both}"

echo "🚀 Quick GitHub Setup - Agent: $AGENT"
echo ""

# Setup Claude Code secrets
if [ "$AGENT" == "claude" ] || [ "$AGENT" == "both" ]; then
  echo "📦 Setting up Claude Code..."
  if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI not found. Install from: https://code.claude.com/"
    exit 1
  fi

  # Generate token and set secret
  echo "Generating Claude Code OAuth token..."
  TOKEN=$(claude setup-token 2>&1 | tail -1)
  echo "$TOKEN" | gh secret set CLAUDE_CODE_OAUTH_TOKEN

  echo "✅ Claude Code configured"
  echo ""
fi

# Setup Codex secrets
if [ "$AGENT" == "codex" ] || [ "$AGENT" == "both" ]; then
  echo "📦 Setting up Codex..."
  if [ ! -f "$HOME/.codex/auth.json" ]; then
    echo "❌ Codex not authenticated. Run: codex login"
    exit 1
  fi

  # Run the setup script
  bash scripts/setup-codex-secrets.sh

  echo "✅ Codex configured"
  echo ""
fi

# Configure GitHub Actions Permissions (IMPORTANT!)
echo "🔐 Configuring GitHub Actions permissions..."
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

# Set workflow permissions to read and write
gh api -X PUT "/repos/$REPO/actions/permissions/workflow" \
  -f default_workflow_permissions=write \
  -F can_approve_pull_request_reviews=false

# Enable Actions to create PRs
gh api -X PATCH "/repos/$REPO" \
  -f allow_auto_merge=false

echo "✅ Permissions configured:"
echo "   - Workflow permissions: read and write"
echo "   - Actions can create PRs: enabled"
echo ""

# Note: "Allow GitHub Actions to create and approve pull requests"
# must be enabled manually in Settings > Actions > General
echo "⚠️  Manual step required:"
echo "   Go to: https://github.com/$REPO/settings/actions"
echo "   Under 'Workflow permissions':"
echo "   ✓ Check 'Allow GitHub Actions to create and approve pull requests'"
echo ""
read -p "Press Enter after enabling this setting (or Ctrl+C to skip)..." || true
echo ""

# Setup git hooks
echo "📦 Setting up git hooks..."
bash scripts/setup-git-hooks.sh

echo "✅ Git hooks configured"
echo ""

# Deploy workflows
echo "📦 Deploying GitHub Actions workflows..."

# Always use multi-agent workflow if both are set up
if [ "$AGENT" == "both" ]; then
  # Multi-agent workflow is already in .github/workflows/multi-agent-fix.yml
  echo "✅ Using multi-agent workflow (Claude + Codex)"
elif [ "$AGENT" == "claude" ]; then
  # Claude-only workflow is already in .github/workflows/claude-fix-coderabbit.yml
  echo "✅ Using Claude Code workflow"
elif [ "$AGENT" == "codex" ]; then
  echo "⚠️  Codex-only workflow not yet created"
  echo "   Using multi-agent workflow (will only use Codex)"
fi

echo ""

# Check for CodeRabbit config
if [ ! -f .coderabbit.yaml ]; then
  echo "📝 Creating CodeRabbit configuration..."
  cp .coderabbit.yaml .coderabbit.yaml 2>/dev/null || echo "⚠️  .coderabbit.yaml template not found"
fi

# Verify secrets
echo "🔍 Verifying secrets..."
gh secret list

echo ""
echo "✅ GitHub automation setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Enable 'Allow GitHub Actions to create PRs' in repo settings"
echo "  2. Install CodeRabbit: https://github.com/marketplace/coderabbit-ai"
echo "  3. Push to a feat/* branch to test!"
echo ""
echo "Usage:"
if [ "$AGENT" == "both" ]; then
  echo "  - Comment '@claude-fix' on a PR → Claude Code fixes it"
  echo "  - Comment '@codex-fix' on a PR → Codex fixes it"
  echo "  - CodeRabbit reviews automatically use Claude Code"
else
  echo "  - Comment '@$AGENT-fix' on a PR → Fixes are applied"
  echo "  - CodeRabbit reviews trigger automatic fixes"
fi
```

---

## OUTPUT

Displays setup progress and final configuration summary.

---

## NOTES

- Requires: `gh`, `claude` (for Claude), `codex` (for Codex)
- Must be run from repository root
- Internet connection required
- Re-run anytime to update secrets
