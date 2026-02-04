# qute-marketplace

Personal Claude Code plugin marketplace. Single install gives access to all plugins.

## Project Structure

```
qute-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # AUTO-GENERATED — do not edit directly
├── plugins/                    # Internal plugins (source of truth)
│   ├── doc-enforcer/           # Hook: reminds when docs may need updating
│   ├── forced-eval/            # Hook: force tool evaluation before implementation
│   ├── notifications/          # Commands + hook: ntfy.sh push notifications
│   ├── research-workflow/      # Commands: ML/DS research lifecycle
│   ├── session-persistence/     # Hooks + commands: save/restore session state
│   ├── skill-use-logger/       # Hook: logs skill invocations to JSONL
│   └── strategic-compact/      # Hook: suggests /compact at tool-call thresholds
├── external/                   # Plugins cloned from GitHub (gitignored)
│   ├── compound-engineering-plugin/  # Workflow: plan → work → review
│   └── homunculus/             # Learning + memory: observation → instincts
├── scripts/
│   ├── build.py                # Regenerate marketplace.json from plugins/
│   ├── create.py               # Scaffold new plugin from template
│   ├── fetch.py                # Clone external plugin from GitHub
│   └── update.py               # Git pull external plugins
└── templates/
    └── plugin-template/        # Skeleton for new plugins
```

## Key Workflow

### After adding or modifying any plugin:

```bash
python scripts/build.py
```

This scans `plugins/` and `external/`, generates `.claude-plugin/plugin.json` per plugin,
converts hooks to the new format if needed, and rebuilds `marketplace.json`.

**Never hand-edit `.claude-plugin/marketplace.json`** — it is overwritten by `build.py`.
Edit individual `plugins/*/plugin.json` files instead.

### Creating a new plugin:

```bash
python scripts/create.py my-plugin
# Edit plugins/my-plugin/plugin.json, add commands/skills/hooks
python scripts/build.py
```

### Fetching an external plugin:

```bash
python scripts/fetch.py github:user/repo [--branch main]
python scripts/build.py
```

## Plugin Anatomy

Every plugin has a `plugin.json` manifest:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What it does",
  "author": "twilc",
  "commands": ["commands/example.md"],
  "skills": ["skills/skill-name"],
  "rules": ["rules/rule-name.md"],
  "hooks": "hooks/hooks.json"
}
```

Standard directories inside a plugin:

| Directory    | Purpose                              |
|------------- |--------------------------------------|
| `commands/`  | Markdown files defining slash commands |
| `skills/`    | `SKILL.md` files with domain knowledge |
| `rules/`     | Markdown files always loaded into conversations |
| `hooks/`     | `hooks.json` for lifecycle hooks     |
| `scripts/`   | Python/shell scripts invoked by hooks |
| `config/`    | JSON configuration files             |
| `templates/` | File templates for scaffolding       |

## Plugin Types

**Hook-only** (invisible, no user commands): `doc-enforcer`, `forced-eval`, `strategic-compact`, `skill-use-logger`
**Command + hook** (user-invokable + automatic): `session-persistence`, `notifications`
**Command-based** (user-invokable): `research-workflow`
**External workflow** (commands + skills + hooks): `homunculus`, `compound-engineering`

## Hook System

Hooks fire at lifecycle events. Current format:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/script.py",
            "tools": ["Read"]
          }
        ]
      }
    ]
  }
}
```

Available hook points used in this project:

| Hook                | When                        | Used By                                    |
|---------------------|-----------------------------|---------------------------------------------|
| `UserPromptSubmit`  | Before processing prompt    | homunculus, forced-eval                     |
| `PreToolUse`        | Before tool execution       | strategic-compact                           |
| `PostToolUse`       | After tool execution        | doc-enforcer, homunculus, notifications, skill-use-logger |
| `PreCompact`        | Before context compaction   | strategic-compact                           |
| `SessionStart`      | Session begins              | session-persistence                         |
| `Stop`              | Session ends                | homunculus, session-persistence              |

## Hook Script Conventions

- Use `#!/usr/bin/env python3`
- Reference paths via `${CLAUDE_PLUGIN_ROOT}`
- Exit 0 on success
- Keep execution under 100ms — hooks run synchronously

## Conventions

- Plugin names: lowercase, hyphen-separated (`context-management`)
- Command format: `/plugin-name:command-name`
- One command per markdown file in `commands/`
- One skill per directory in `skills/` with a `SKILL.md`
- One rule per markdown file in `rules/`
- All plugins must have a `plugin.json` at their root
- Run `build.py` after any structural change

## Current Plugin Registry (7 internal + 3 external)

### Internal plugins

| Plugin               | Category | Components               |
|----------------------|----------|--------------------------|
| doc-enforcer         | utility  | hook, script             |
| forced-eval          | utility  | hook, script             |
| notifications        | utility  | commands, hook, scripts  |
| research-workflow    | utility  | commands, skill          |
| session-persistence  | utility  | commands, hooks, scripts |
| skill-use-logger     | utility  | hook, script             |
| strategic-compact    | utility  | hooks, scripts           |

### External plugins (via fetch.py)

| Plugin               | Source                                    | Components                    |
|----------------------|-------------------------------------------|-------------------------------|
| compound-engineering | github:EveryInc/compound-engineering-plugin | agents, commands, skills     |
| coding-tutor         | github:EveryInc/compound-engineering-plugin | commands, skills             |
| homunculus           | github:humanplane/homunculus              | skills, hooks, agents, commands |

## Common Tasks

- **Add a plugin**: create in `plugins/`, run `build.py`, commit
- **Remove a plugin**: delete directory, run `build.py`, commit
- **Update hooks format**: `build.py` auto-converts old → new format
- **Install marketplace**: `claude plugin install github:tomlupo/qute-marketplace`
