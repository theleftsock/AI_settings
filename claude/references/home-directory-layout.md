# Home directory layout

> What Claude Code stores in the user's home directory on macOS/Linux (`~`) and Windows (`%USERPROFILE%`). Compiled by inspecting an actual `~/.claude` install; not official Anthropic documentation.

## Top-level file

| Path | Contents |
| :--- | :--- |
| `~/.claude.json` | Main config: account/OAuth info, `projects` map (per-project settings, allowed tools, MCP servers, trust state), onboarding/feature flags, usage and experiment caches |

## `~/.claude/` directory

| Path | Contents |
| :--- | :--- |
| `CLAUDE.md` | Global user instructions, loaded into every session |
| `settings.json` / `settings.local.json` | Permissions, model, theme, hooks, env vars |
| `backups/.claude.json.backup.<timestamp>` | Rotating backups of `~/.claude.json` |
| `projects/<url-encoded-cwd-path>/` | One directory per project worked in |
| `projects/<...>/<session-uuid>.jsonl` | Full transcript for each session in that project |
| `projects/<...>/memory/` | Persistent memory files for that project |
| `sessions/` | Session metadata + auth key files (`<pid>.json`, `<pid>.<hash>.key`) |
| `session-env/<session-uuid>/` | Per-session environment snapshots |
| `shell-snapshots/snapshot-<shell>-<ts>-<rand>.sh` | Captured shell state for Bash tool persistence across calls |
| `history.jsonl` | Command/prompt history |
| `ide/<port>.lock` | Lock files for detecting a running IDE extension connection |
| `plugins/known_marketplaces.json` | Registered plugin marketplaces |
| `plugins/marketplaces/<name>/` | Installed plugin marketplace sources |
| `cache/changelog.md` | Cached changelog content |
| `file-history/` | Undo history for file edits |
| `.last-cleanup` | Auto-cleanup bookkeeping |
| `.last-update-result.json` | Auto-update bookkeeping |

## Feature directories (created only when populated)

| Path | Contents |
| :--- | :--- |
| `~/.claude/commands/` | Custom slash commands |
| `~/.claude/agents/` | Custom subagents |
| `~/.claude/skills/` | Custom skills |
| `~/.claude/keybindings.json` | Custom keybindings |

## Windows notes

Same structure under `%USERPROFILE%\.claude\...` and `%USERPROFILE%\.claude.json` — Claude Code resolves paths via the OS home directory, so the layout doesn't otherwise differ by platform.
