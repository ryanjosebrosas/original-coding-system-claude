### Beyond GitHub Actions

GitHub Actions (section 10) works well for trigger-response workflows, but has limitations: single-shot execution (no mid-task conversation), limited visibility (must check Action logs), and no persistent sessions. The **Remote Agentic Coding System** solves these with a custom, extensible application that runs your PIV Loop remotely with real-time conversation, multi-platform support, and persistent sessions.

The system lives in its own repository (`dynamous-community/remote-coding-agent`) — this section documents the architecture and concepts, not the implementation code.

### Architecture Overview

The system uses an **orchestrator pattern** with two generic interfaces:

- **`IPlatformAdapter`** — How platforms communicate (receive message, send message, get conversation ID)
- **`IAssistantClient`** — How coding assistants operate (start session, resume session, send message, end session)

This creates **M+N integrations** instead of M×N. Adding a new platform (e.g., Slack) only requires implementing `IPlatformAdapter` — it automatically works with all coding assistants. Adding a new assistant only requires implementing `IAssistantClient` — it works with all platforms.

```
Apps (Telegram, GitHub, Slack)  →  Orchestrator  →  Coding Assistants (Claude Code, Codex)
         IPlatformAdapter              ↕                  IAssistantClient
```

### Platform Integrations

| Platform | Output Style | Context Injection | Best For |
|----------|-------------|-------------------|----------|
| **Telegram** | Real-time streamed (tool calls, thoughts) | Manual (conversation-based) | Interactive development, quick tasks |
| **GitHub** | Final summary comment on Issue/PR | Auto-injected (issue/PR body at conversation start) | Full PIV loops, code review, Git-native workflows |
| **Slack** | Coming soon | TBD | Team collaboration |

Telegram gives the closest experience to using a CLI locally. GitHub is ideal for Git-native workflows where issue and PR context is automatically injected.

### Command System (Remote)

Your local `.claude/commands/` or `.codex/commands/` work remotely:

1. `/load-commands .claude/commands` — Load commands from the cloned repository
2. `/command-invoke {name} {args}` — Execute a loaded command (same INPUT→PROCESS→OUTPUT framework)
3. `/commands` — List all loaded commands

The system auto-detects `.claude/` or `.codex/` folders to determine which coding assistant to use. Commands like `plan-feature` and `execute` automatically trigger **session separation** — a new conversation starts between planning and execution, just like switching contexts locally.

### PIV Loop — Remote Workflow

The full PIV Loop runs remotely via GitHub Issues:

1. **Create Issue** — Describe the feature or bug (this becomes the auto-injected context)
2. **Load commands** — `@remote-agent /load-commands .claude/commands`
3. **Prime** — `@remote-agent /command-invoke prime` (issue context auto-injected)
4. **Plan** — `@remote-agent /command-invoke plan-feature "description"` (creates branch, pushes plan)
5. **Validate plan** — Review the plan in the feature branch on GitHub
6. **Execute** — `@remote-agent /command-invoke execute` (new session, reads plan, implements, creates PR)
7. **Code review** — `@remote-agent /command-invoke code-review` (on the PR)
8. **Validate locally** — Pull the branch, test manually
9. **Merge** — Close the loop by merging the PR

Key difference from local: fresh context between plan and execute is handled automatically by the system.

### Session & Data Management

- **Postgres database** stores sessions, conversations, and codebase references
- **Session persistence** — survives container restarts
- **Concurrent sessions** — multiple agents on different issues simultaneously (e.g., Codex on Telegram + Claude Code on GitHub)
- **`/reset`** — Clear conversation and start fresh
- **`/repos`** — List cloned repositories

### Local vs Cloud Deployment

| Aspect | Local | Cloud |
|--------|-------|-------|
| **Runtime** | Docker + ngrok (for HTTPS) | Docker + Caddy (for SSL) |
| **Availability** | Only when your computer is on | 24/7 |
| **Cost** | Free (your hardware) | ~$14/month (DigitalOcean/Ubuntu) |
| **GitHub webhooks** | ngrok URL (same per device) | Domain + DNS A record |
| **Setup** | Clone, `.env`, `docker compose up` | SSH, deploy user, firewall, Caddy config |

Same environment variables, same behavior. Cloud deployment adds security hardening (deploy user, disabled password auth, firewall) and Caddy for automatic SSL certificates.

### Trust Progression (Complete)

```
Manual Prompts → Commands → Chained Commands → GitHub Actions → Remote System
     ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑  ↑ trust & verify ↑
```

The Remote System is the final level: full PIV Loop with real-time conversation, multi-platform support, persistent sessions, and automatic session separation. Only move here when GitHub Actions workflows are proven reliable.

### Getting Started

1. Clone the repository: `github.com/dynamous-community/remote-coding-agent`
2. Prerequisites: Docker, GitHub account, Claude Code or Codex, Telegram or GitHub
3. Configure environment variables (database, GitHub token, coding assistant, platform)
4. Run: `docker compose up --build -d`
5. See `reference/remote-system-guide.md` for detailed setup and cloud deployment
