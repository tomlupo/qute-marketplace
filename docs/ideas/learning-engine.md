# learning-engine Plugin

New internal plugin at `plugins/learning-engine/` that replaces homunculus with three improvements: deterministic observation analysis, cross-project learning, and ntfy.sh notifications when patterns are ready for skill creation.

## Architecture

```
HOOKS (100% reliable, <100ms, always exit 0)
  UserPromptSubmit → observe_prompt.py → ~/.claude/learning/observations.jsonl
  PostToolUse      → observe_tool.py   → ~/.claude/learning/observations.jsonl
  Stop             → session_end.py    → detect_patterns.py → patterns.json
                                       → notify_patterns.py → ntfy.sh (if threshold met)

COMMANDS (user-initiated, LLM-powered)
  /learning-engine:status   → show state, observations, patterns, instincts
  /learning-engine:patterns → show raw algorithmic pattern output
  /learning-engine:analyze  → LLM creates instinct .md files from patterns
  /learning-engine:evolve   → LLM creates skill, deployed to ~/.claude/skills/learned-{domain}/
  /learning-engine:reset    → archive/clear data
```

## Key Improvements Over Homunculus

| Problem | Homunculus | learning-engine |
|---------|-----------|-----------------|
| Analysis reliability | session-memory skill (~50-80%) spawns observer agent | Stop hook runs Python detect_patterns.py (100%) |
| Cross-project | Per-project `.claude/homunculus/` | Global `~/.claude/learning/`, observations tagged with project |
| Skill deployment | Writes to `.claude/homunculus/evolved/` (not discoverable) | Writes to `~/.claude/skills/learned-{domain}/` (auto-discovered) |
| Notification | Relies on skill greeting message | ntfy.sh push notification on clustering |
| Pattern detection | LLM (Haiku agent, expensive) | Algorithmic Python (Counter, n-grams, free) |

## Plugin Structure

```
plugins/learning-engine/
├── plugin.json
├── config/
│   └── learning.json           # Thresholds, domain keywords, notification settings
├── hooks/
│   └── hooks.json              # UserPromptSubmit, PostToolUse, Stop
├── scripts/
│   ├── observe_prompt.py       # Hook: capture user prompts
│   ├── observe_tool.py         # Hook: capture tool usage (structured)
│   ├── session_end.py          # Hook: orchestrate analysis + notification
│   ├── detect_patterns.py      # Core: algorithmic pattern detection (5 algorithms)
│   └── notify_patterns.py      # Send ntfy.sh notification via notifications plugin
├── commands/
│   ├── status.md
│   ├── patterns.md
│   ├── analyze.md
│   ├── evolve.md
│   └── reset.md
└── README.md
```

## Global Storage

```
~/.claude/learning/
├── observations.jsonl          # Raw observations, tagged with project
├── patterns.json               # Algorithmic detection output
├── state.json                  # Session counts, project list, timestamps
├── instincts/                  # Instinct .md files (created by /analyze)
└── archive/                    # Archived observations
```

## Detection Algorithms (detect_patterns.py)

All pure Python, no LLM needed:

1. **Tool frequency counts** — Counter per tool, per project and globally
2. **Tool sequence n-grams** — 2-gram and 3-gram sequences, threshold: 5+ occurrences
3. **Error-fix pairs** — Tool failure → recovery action within next 3 observations, threshold: 3+
4. **File patterns** — Frequently edited files, co-editing sequences
5. **Domain clustering** — Map patterns to domains via keyword matching (config-driven), flag when 5+ patterns cluster

## Observation Format

```jsonl
{"timestamp":"...","type":"prompt","project":"/abs/path","project_name":"repo","session_id":"...","prompt":"truncated..."}
{"timestamp":"...","type":"tool","project":"/abs/path","project_name":"repo","session_id":"...","tool":"Bash","input_summary":"pytest tests/","success":true,"files":["src/main.py"]}
```

## Notification Flow

1. Stop hook → detect_patterns.py updates patterns.json
2. session_end.py checks if `evolution_ready` domains changed
3. If new domain ready → notify_patterns.py imports `send_notification()` from `plugins/notifications/scripts/notify.py`
4. Sends: "Learning: 7 testing patterns across 3 projects. Run /learning-engine:evolve testing"
5. Records notification timestamp to avoid repeat alerts (24h cooldown)

## Implementation Order

1. `plugin.json` + `config/learning.json` + `hooks/hooks.json`
2. `scripts/observe_prompt.py` (simplest hook, establishes format)
3. `scripts/observe_tool.py` (richest data capture)
4. `scripts/detect_patterns.py` (core engine, most complex)
5. `scripts/notify_patterns.py` (ntfy.sh integration)
6. `scripts/session_end.py` (orchestrator)
7. Commands: status, patterns, analyze, evolve, reset
8. `README.md`
9. `python scripts/build.py` to rebuild marketplace
10. Test: run a session, verify observations.jsonl populated

## Reference Files

- `plugins/notifications/scripts/notify.py` — reuse `send_notification()` for ntfy.sh
- `plugins/skill-use-logger/scripts/log_skill_use.py` — PostToolUse hook pattern (stdin JSON, JSONL append)
- `plugins/session-persistence/scripts/session_end.py` — Stop hook pattern, `~/.claude/` global storage
- `external/homunculus/plugins/homunculus/agents/observer.md` — pattern detection categories reference

## Verification

- [ ] Run a short Claude session, verify `~/.claude/learning/observations.jsonl` has entries
- [ ] Run `detect_patterns.py` against observations, verify `patterns.json` created
- [ ] Manually trigger `/learning-engine:status` to confirm display works
- [ ] Manually trigger `/learning-engine:patterns` to see detected patterns
- [ ] Verify `python scripts/build.py` succeeds and marketplace.json includes learning-engine
- [ ] Confirm ntfy.sh notification arrives when thresholds are met (may need to lower thresholds for testing)
