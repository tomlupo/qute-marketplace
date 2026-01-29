# Datasets Guide Plugin

On-demand dataset management guidelines for Claude Code. Provides directory structure, data flow patterns, naming conventions, and quality practices.

## How It Works

**Skill (manual):** Available as `/datasets` for explicit invocation when creating or working with datasets.

## What's Covered

- Directory structure (`data/raw/`, `data/intermediate/`, `data/processed/`)
- Data flow principles (raw is immutable, processed must be reproducible)
- Naming conventions for datasets and files
- Format selection guidance (CSV, Parquet, JSON, Feather)
- Data collection and scraping best practices
- Quality validation and documentation requirements

## When to Use

Invoke `/datasets` when:
- Creating a new dataset or data pipeline
- Setting up data collection / scraping
- Choosing storage formats
- Documenting dataset quality

## Plugin Structure

```
datasets-guide/
├── plugin.json
├── README.md
└── skills/
    └── datasets/
        └── SKILL.md         # Full guidelines
```

## License

MIT
