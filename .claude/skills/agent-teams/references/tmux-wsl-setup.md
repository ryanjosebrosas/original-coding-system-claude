# WSL + tmux Setup for Agent Teams

Split-pane display for Agent Teams requires tmux (Linux/WSL) or iTerm2 (macOS). This guide covers WSL + tmux setup for Windows users and the universal in-process fallback.

---

## 1. Prerequisites

- **Windows 10/11** with WSL2 installed
- A Linux distribution (Ubuntu recommended): `wsl --install -d Ubuntu`
- Claude Code CLI installed inside WSL (not Windows-side)
- Agent Teams experimental flag enabled (see Section 3)

---

## 2. Install tmux

Inside your WSL terminal:

```bash
sudo apt update && sudo apt install tmux -y
```

Verify installation:

```bash
tmux -V
# Expected: tmux 3.x
```

---

## 3. Configure Claude Code

Enable Agent Teams and set tmux as the teammate display mode. Settings can be configured globally or per-project.

**Global** (`~/.claude/settings.json`):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "tmux"
}
```

**Per-project** (`.claude/settings.local.json`):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "tmux"
}
```

**Settings reference**:

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `"1"` / unset | unset | Enable Agent Teams feature |
| `teammateMode` | `"auto"`, `"tmux"`, `"in-process"` | `"auto"` | How teammates are displayed |

---

## 4. Verify Installation

```bash
# Check tmux version
tmux -V

# Test tmux session creation
tmux new-session -s test -d
tmux list-sessions
tmux kill-session -t test

# Verify Claude Code recognizes Agent Teams
claude --help | grep -i team
```

If `tmux new-session` works and you can list/kill sessions, tmux is correctly installed.

---

## 5. Running Claude Code with tmux

**Start tmux first, then launch Claude Code inside it:**

```bash
# Start a named tmux session
tmux new-session -s coding

# Inside tmux, launch Claude Code
claude
```

When Agent Teams spawns teammates, tmux automatically creates split panes — one per teammate. The lead agent stays in the original pane.

**tmux basics for Agent Teams:**

| Key | Action |
|-----|--------|
| `Ctrl+B` then `o` | Switch between panes |
| `Ctrl+B` then `z` | Toggle pane zoom (fullscreen) |
| `Ctrl+B` then `d` | Detach from session (agents keep running) |
| `tmux attach -t coding` | Reattach to session |

---

## 6. Fallback: In-Process Mode

If tmux isn't available or has issues, use in-process mode. No setup required — works everywhere.

**Set in settings:**

```json
{
  "teammateMode": "in-process"
}
```

**Or pass as CLI flag:**

```bash
claude --teammate-mode in-process
```

**Navigation in in-process mode:**

| Key | Action |
|-----|--------|
| `Shift+Up` / `Shift+Down` | Navigate between teammates |
| `Ctrl+T` | Toggle shared task list |

In-process mode runs all teammates in the same terminal. Less visual separation than tmux, but fully functional.

---

## 7. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `tmux: command not found` | tmux not installed or PATH issue | `sudo apt install tmux` inside WSL |
| Panes don't split | Not running inside tmux session | Launch `tmux` first, then `claude` |
| Orphaned tmux sessions | Sessions from previous runs | `tmux ls` to list, `tmux kill-session -t <name>` to clean up |
| Split panes not working in VS Code terminal | VS Code terminal doesn't support tmux split panes | Use a standalone WSL terminal (Windows Terminal recommended) |
| Split panes not working in Windows Terminal | Some terminal emulators interfere with tmux | Use `tmux` inside a plain WSL terminal window |
| Ghostty doesn't support split panes | Known limitation | Use in-process mode or a different terminal |
| Permission errors | Claude Code not installed in WSL | Install Claude Code inside WSL, not Windows-side |

**Cleaning up orphaned sessions:**

```bash
# List all tmux sessions
tmux ls

# Kill specific session
tmux kill-session -t <session-name>

# Kill ALL sessions
tmux kill-server
```

---

## 8. iTerm2 Alternative (macOS)

macOS users can use iTerm2 instead of tmux for native split-pane support:

1. Install iTerm2: `brew install --cask iterm2`
2. Open iTerm2 Preferences → General → Magic → Enable Python API
3. Set teammate mode: `"teammateMode": "iterm2"` in settings
4. Launch Claude Code from iTerm2

iTerm2 creates native split panes (no tmux needed). Same functionality, native macOS experience.
