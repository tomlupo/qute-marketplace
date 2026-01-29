# qute-marketplace

Personal Claude Code plugin marketplace. Single install gives access to all plugins.

## Project Structure

```
qute-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # AUTO-GENERATED — do not edit directly
├── plugins/                    # Internal plugins (source of truth)
│   ├── context-management/     # Hook: context budget on Read
│   ├── datasets-guide/         # Skill: dataset conventions
│   ├── documentation-guide/    # Skill: doc standards
│   ├── forced-eval/            # Hook: force tool evaluation before implementation
│   ├── llm-council/            # Commands: multi-model consensus
│   ├── llm-external-review/    # Commands: external LLM code review
│   ├── notifications/          # Commands + hook: ntfy.sh push notifications
│   ├── research-workflow/      # Commands: ML/DS research lifecycle
│   └── workflow-plugin/        # Commands + hooks: session/task management
├── external/                   # Plugins cloned from GitHub (gitignored)
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
  "hooks": "hooks/hooks.json"
}
```

Standard directories inside a plugin:

| Directory    | Purpose                              |
|------------- |--------------------------------------|
| `commands/`  | Markdown files defining slash commands |
| `skills/`    | `SKILL.md` files with domain knowledge |
| `hooks/`     | `hooks.json` for lifecycle hooks     |
| `scripts/`   | Python/shell scripts invoked by hooks |
| `config/`    | JSON configuration files             |
| `templates/` | File templates for scaffolding       |

## Plugin Types

**Hook-only** (invisible, no user commands): `forced-eval`, `context-management`
**Skill-only** (knowledge injection): `datasets-guide`, `documentation-guide`
**Command-based** (user-invokable): `llm-council`, `llm-external-review`, `notifications`
**Workflow** (commands + skills + hooks): `workflow-plugin`, `research-workflow`

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

| Hook                | When                        | Used By                          |
|---------------------|-----------------------------|----------------------------------|
| `SessionStart`      | Session begins              | workflow-plugin                  |
| `UserPromptSubmit`  | Before processing prompt    | forced-eval, workflow-plugin     |
| `PreToolUse`        | Before tool execution       | context-management, llm-council  |
| `PostToolUse`       | After tool execution        | notifications, workflow-plugin   |
| `PreCompact`        | Before context compaction   | workflow-plugin                  |

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
- All plugins must have a `plugin.json` at their root
- Run `build.py` after any structural change

## Current Plugin Registry (9 plugins)

| Plugin               | Category | Components               |
|----------------------|----------|--------------------------|
| context-management   | utility  | skill, hook, script      |
| datasets-guide       | utility  | skill                    |
| documentation-guide  | utility  | skill                    |
| forced-eval          | utility  | hook, script             |
| llm-council          | utility  | commands, skill, hook    |
| llm-external-review  | utility  | commands, skill          |
| notifications        | utility  | commands, hook, scripts  |
| research-workflow    | utility  | commands, skill          |
| workflow-plugin      | utility  | commands, skills, hooks  |

## Common Tasks

- **Add a plugin**: create in `plugins/`, run `build.py`, commit
- **Remove a plugin**: delete directory, run `build.py`, commit
- **Update hooks format**: `build.py` auto-converts old → new format
- **Install marketplace**: `claude plugin install github:tomlupo/qute-marketplace`
