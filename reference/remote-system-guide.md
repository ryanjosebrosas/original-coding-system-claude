# Remote Agentic Coding System — Setup & Deployment Guide

On-demand reference for setting up and deploying the Remote Agentic Coding System.

**Repository**: The Remote Agentic Coding System lives in a separate repository. See `reference/remote-agentic-system.md` for the full architecture guide and repository details.
**Cloud Deployment Guide**: See the repository's `docs/cloud-deployment.md` for cloud setup instructions.

---

## Prerequisites

- **Docker** (recommended) or Node.js for local development
- **GitHub account** with a personal access token (classic, `repo` scope)
- **One coding assistant**: Claude Code or Codex (or both)
- **One platform**: Telegram or GitHub (or both)

---

## Environment Variables

### Core (required)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Postgres connection string (local or remote e.g., Supabase, Neon) |
| `GH_TOKEN` | GitHub personal access token — used by GitHub CLI for PRs and comments |
| `GITHUB_TOKEN` | GitHub personal access token — used for cloning repositories |

For local Postgres, use the default connection string from `docker-compose.yml`. For remote Postgres (Supabase), use the Transaction Pooler IPv4-compatible connection string.

### Coding Assistant

**Claude Code** (pick one auth method):
| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | **(Recommended)** OAuth token from `claude setup-token` (uses your MAX/Pro subscription) |
| `ANTHROPIC_API_KEY` | (Alternative — pay-per-use) Anthropic API key via API dashboard |

> **WARNING**: If both are set, `ANTHROPIC_API_KEY` takes priority and you'll be billed per-token via API instead of using your subscription. Remove or unset `ANTHROPIC_API_KEY` to ensure subscription billing.

**Codex**:
| Variable | Description |
|----------|-------------|
| `CODEX_CLIENT_ID` | From `~/.codex/auth.json` after `codex login` |
| `CODEX_CLIENT_SECRET` | From `~/.codex/auth.json` |
| `CODEX_ACCESS_TOKEN` | From `~/.codex/auth.json` |
| `CODEX_REFRESH_TOKEN` | From `~/.codex/auth.json` |

Set `DEFAULT_ASSISTANT` to `claude` or `codex` to control which is used by default. The system auto-detects `.claude/` or `.codex/` folders in repositories.

### Platform

**Telegram**:
| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | From BotFather (`/newbot` command in Telegram) |

**GitHub**:
| Variable | Description |
|----------|-------------|
| `GITHUB_WEBHOOK_SECRET` | Generated secret shared between your app and GitHub webhook |

---

## Platform Setup

### Telegram

1. Install Telegram (desktop or mobile)
2. Message `@BotFather` on Telegram
3. Run `/newbot`, provide a name and username
4. Copy the bot token → set as `TELEGRAM_BOT_TOKEN`
5. Search for your bot in Telegram contacts to start a conversation

### GitHub Webhooks

1. **Generate webhook secret**: Use `openssl rand -hex 32` (Linux/Mac) or PowerShell equivalent
2. **Set environment variable**: Add secret as `GITHUB_WEBHOOK_SECRET`
3. **Expose your server**:
   - Local: Install and run `ngrok http 3000` for HTTPS tunneling
   - Cloud: Use Caddy for automatic SSL (see Cloud Deployment below)
4. **Create webhook in GitHub**: Repository → Settings → Webhooks → Add webhook
   - **Payload URL**: `https://{your-url}/webhook/github`
   - **Content type**: `application/json`
   - **Secret**: Your generated webhook secret
   - **Events**: Select individual → Issues, Issue comments, Pull requests
   - Uncheck Pushes (not needed)
5. **Verify**: After creating, refresh the page — green checkmark = success

The same webhook secret works across multiple repositories. Set up a webhook per repo you want to use.

---

## Running Locally

```bash
# With remote Postgres (recommended)
docker compose up --build -d

# With local Postgres
docker compose --profile database up --build -d
```

**Check logs**: `docker compose logs -f` (verify no errors on startup)

**Verify in Telegram**: Send `/help` to your bot — should list available commands.

---

## Cloud Deployment Summary

Deploy to any Ubuntu Linux instance (DigitalOcean, Hetzner, etc.). Full guide: `docs/cloud-deployment.md` in the repository.

### High-Level Steps

1. **Create instance** — Ubuntu with Docker (~$14/month on DigitalOcean, 2GB RAM, 1 CPU)
2. **Security setup**:
   - Generate SSH key, add to instance
   - Create `deploy` user with sudo permissions
   - Copy SSH keys to deploy user
   - Disable password authentication in SSH config
   - Configure firewall (ports 22, 80, 443)
3. **DNS setup** — Create A record pointing subdomain to instance IP (e.g., `remote-agent.yourdomain.com`)
4. **Clone repository** on the instance
5. **Configure** — Copy `.env` from local setup (same variables work)
6. **Caddy setup** — Copy `Caddyfile.example` to `Caddyfile`, set your domain (Caddy auto-generates SSL certificates)
7. **Run**: `docker compose -f docker-compose.yml -f docker-compose.cloud.yml up --build -d`
8. **Update GitHub webhook** — Change payload URL from ngrok to your domain
9. **Test** — Send messages via Telegram and GitHub to verify

### Key Differences from Local

- **Caddy replaces ngrok** for HTTPS (production-grade, automatic SSL renewal)
- **Domain + DNS A record** instead of ngrok tunnel URL
- **Deploy user** instead of root (security best practice)
- **Runs 24/7** — accessible from any device, anywhere

---

## Using the System

### System Commands

| Command | Description |
|---------|-------------|
| `/help` | List available system commands |
| `/clone {url}` | Clone a GitHub repository into the workspace |
| `/repos` | List cloned repositories |
| `/load-commands {path}` | Load slash commands from a directory (e.g., `.claude/commands`) |
| `/commands` | List loaded commands |
| `/command-invoke {name} {args}` | Execute a loaded command |
| `/reset` | Clear conversation, start fresh session |
| `/git {command}` | Run git commands (e.g., `/git current working directory`) |

### GitHub Trigger

Comment `@remote-agent {message}` on any Issue or PR in a webhook-connected repository.

### Typical Workflow

```
/clone {repo-url}
/load-commands .claude/commands
/command-invoke prime
/command-invoke plan-feature "Build feature X"
  → (review plan in feature branch)
/command-invoke execute
  → (new session, implements, creates PR)
/command-invoke code-review
  → (review on the PR)
  → merge PR locally after validation
```

---

## When to Use Which

| Scenario | Recommended Approach |
|----------|---------------------|
| Simple trigger-response (README fix, small bug) | GitHub Actions (see `reference/github-orchestration.md`) |
| Full PIV Loop with conversation | Remote System (this) |
| Real-time interactive development | Remote System via Telegram |
| Git-native workflow with auto-context | Remote System via GitHub |
| CI/CD integration | GitHub Actions (see `reference/github-orchestration.md`) |
