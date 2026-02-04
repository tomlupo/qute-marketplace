# Qute Marketplace

Personal Claude Code plugin marketplace. Install once, get access to all plugins.

## Installation

### From GitHub (recommended)

```bash
claude plugin install github:tomlupo/qute-marketplace
```

This registers the marketplace and installs all internal plugins:

| Plugin | What it does |
|--------|-------------|
| **doc-enforcer** | Reminds when code files accumulate without doc updates |
| **forced-eval** | Forces skill/tool evaluation before jumping to implementation |
| **strategic-compact** | Suggests `/compact` at 50 tool calls, then every 25 |
| **skill-use-logger** | Logs skill invocations to `.claude/skill-use-log.jsonl` |
| **notifications** | Push notifications via ntfy.sh when tasks complete |
| **session-persistence** | Saves session state on exit, reports unfinished work on start |
| **research-workflow** | ML/DS research lifecycle — hypotheses, experiments, findings |

### Adding external plugins

For the full learning stack, clone the repo and fetch externals:

```bash
git clone https://github.com/tomlupo/qute-marketplace.git
cd qute-marketplace
./setup.sh   # fetches externals + rebuilds marketplace
```

---

## Recommended External Plugins

These are curated external plugins that complement the internal utilities.

### homunculus — Learning + Memory

> [github:humanplane/homunculus](https://github.com/humanplane/homunculus)

A living plugin that observes your work, learns instincts, and evolves capabilities over time. Runs silently in the background — no intervention needed.

**What it does automatically:**
- Captures observations on every prompt and tool use (hooks)
- Spawns an observer agent at session start to process pending observations
- Creates instincts from patterns it detects — no approval needed
- Proposes evolution when 5+ instincts cluster in a domain

**Commands:**

| Command | Description |
|---------|-------------|
| `/homunculus:init` | Birth or wake your homunculus in a project |
| `/homunculus:status` | Check instincts, observations, identity |
| `/homunculus:evolve` | Grow new capabilities from clustered instincts |
| `/homunculus:export` | Export instincts for sharing |
| `/homunculus:import` | Import instincts from others |

### compound-engineering — Workflow Automation

> [github:EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)

Full development lifecycle: brainstorm, plan, work, review, document. 19 commands, 15 skills, specialized agents.

**Core workflow loop:**

| Command | Description |
|---------|-------------|
| `/workflows:brainstorm` | Explore ideas and approaches before committing |
| `/workflows:plan` | Turn feature ideas into detailed implementation plans |
| `/workflows:work` | Execute plans with worktrees and task tracking |
| `/workflows:review` | Multi-agent code review before merging |
| `/workflows:compound` | Document learnings to make future work easier |

### How they work together

```
Session start
  session-persist  reports recent sessions with unfinished work
  homunculus       loads identity, spawns observer, processes pending observations
  forced-eval      reminds to check skills/tools before acting

Background (silent, every interaction)
  homunculus       captures prompts + tool use to observations.jsonl
  doc-enforcer     reminds when code edits accumulate without doc updates
  strategic-compact  suggests /compact at 50 tool calls, then every 25
  skill-logger     records skill invocations to skill-use-log.jsonl

Workflow loop
  /workflows:brainstorm  → explore ideas and approaches
  /workflows:plan        → turn ideas into implementation plans
  /workflows:work        → execute with worktrees and task tracking
  /workflows:review      → multi-agent code review before merging
  /workflows:compound    → document learnings for future work

Evolution
  homunculus       clusters observations into instincts automatically
  /homunculus:evolve  → when 5+ instincts cluster, propose new capability

Session end
  session-persist  saves session state to ~/.claude/sessions/
  homunculus       increments session count, observations ready for next start
```

---

## Managing Plugins

### Fetch an external plugin

```bash
python scripts/fetch.py github:username/repo-name
python scripts/build.py
```

The build script auto-detects external marketplace repos (those with `.claude-plugin/marketplace.json`) and scans their `plugins/` subdirectories.

### Create a new internal plugin

```bash
python scripts/create.py my-plugin
# Edit plugins/my-plugin/plugin.json, add commands/skills/hooks
python scripts/build.py
```

### Update external plugins

```bash
python scripts/update.py             # Update all
python scripts/update.py homunculus   # Update specific
python scripts/build.py
```

### Remove a plugin

```bash
rm -rf plugins/plugin-name    # internal
rm -rf external/repo-name     # external
python scripts/build.py
```

### Rebuild after any change

```bash
python scripts/build.py
```

Never hand-edit `.claude-plugin/marketplace.json` — it is overwritten by `build.py`.

---

## Directory Structure

```
qute-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # AUTO-GENERATED by build.py
├── plugins/                      # Internal plugins
│   ├── doc-enforcer/
│   ├── forced-eval/
│   ├── notifications/
│   ├── research-workflow/
│   ├── session-persistence/
│   ├── skill-use-logger/
│   └── strategic-compact/
├── external/                     # Cloned from GitHub (gitignored)
│   ├── compound-engineering-plugin/
│   └── homunculus/
├── scripts/
│   ├── build.py                  # Rebuild marketplace manifest
│   ├── create.py                 # Scaffold new plugin
│   ├── fetch.py                  # Clone from GitHub
│   └── update.py                 # Git pull externals
├── setup.sh                      # Fetch externals + build (run after clone)
└── templates/
    └── plugin-template/
```

## License

MIT
