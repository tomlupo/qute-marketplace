# Documentation Guide Plugin

On-demand documentation standards and directory structure guidelines for Claude Code.

## How It Works

**Skill (manual):** Available as `/documentation` for explicit invocation when creating or organizing documentation.

## What's Covered

- Document length targets and style guidelines
- Directory structure (`docs/` subdirectories and their purposes)
- Reference hierarchy (which docs link to which)
- Writing best practices and common documentation patterns
- Template locations

## When to Use

Invoke `/documentation` when:
- Creating new documentation files
- Organizing or restructuring docs
- Deciding where a document belongs
- Writing dataset docs, setup guides, or reference material

## Plugin Structure

```
documentation-guide/
├── plugin.json
├── README.md
└── skills/
    └── documentation/
        └── SKILL.md         # Full guidelines
```

## License

MIT
