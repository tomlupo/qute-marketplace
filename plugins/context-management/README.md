# Context Management Plugin

Automatic context budget management for Claude Code. Injects strategies when reading large files via a PreToolUse hook.

## How It Works

**Hook (automatic):** When Claude reads a file >500 lines / >50KB, the PreToolUse hook fires and injects the full context management strategies into the conversation. Claude sees the strategies exactly when it needs them.

**Skill (manual):** Available as `/context-management` for explicit invocation during long sessions.

```
Read(large_file.py)  ->  PreToolUse hook fires
                     ->  Checks: >500 lines AND >50KB
                     ->  Loads SKILL.md content
                     ->  Injects strategies into context
                     ->  Claude applies them to the read
```

## What Gets Injected

Core strategies:
- **Search before read** - find relevant content before loading files
- **Progressive disclosure** - headers -> sample -> targeted sections
- **File-based output** - save large results to files, show summaries
- **Context checkpoints** - monitor usage, warn before limits

## Configuration

Thresholds are defined in `scripts/pre_read_context_guard.py`:

| Threshold | Default | Purpose |
|-----------|---------|---------|
| `LARGE_FILE_LINES` | 500 | Minimum lines to trigger |
| `LARGE_FILE_BYTES` | 50,000 | Minimum bytes to trigger |

Both conditions must be met. Binary files (.png, .pdf, .parquet, etc.) are skipped.

## Plugin Structure

```
context-management/
├── plugin.json
├── README.md
├── hooks/
│   └── hooks.json          # PreToolUse on Read
├── scripts/
│   └── pre_read_context_guard.py  # Size check + skill injection
└── skills/
    └── context-management/
        └── SKILL.md         # Strategies (single source of truth)
```

## License

MIT
