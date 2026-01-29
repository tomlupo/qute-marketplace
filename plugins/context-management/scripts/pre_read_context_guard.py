#!/usr/bin/env python3
"""
PreToolUse hook for Read tool.
Checks file size and injects context management skill content for large files.
"""

import json
import os
import sys

# Thresholds
LARGE_FILE_LINES = 500
LARGE_FILE_BYTES = 50_000

SKILL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "skills",
    "context-management",
    "SKILL.md",
)


def count_lines(path: str) -> int | None:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (OSError, UnicodeDecodeError):
        return None


def load_skill() -> str | None:
    resolved = os.path.normpath(SKILL_PATH)
    if not os.path.isfile(resolved):
        return None
    try:
        with open(resolved, "r", encoding="utf-8") as f:
            content = f.read()
        # Strip YAML frontmatter
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                content = content[end + 3 :].lstrip("\n")
        return content
    except OSError:
        return None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path or not os.path.isfile(file_path):
        sys.exit(0)

    # Skip non-text files
    _, ext = os.path.splitext(file_path)
    if ext.lower() in {
        ".png", ".jpg", ".jpeg", ".gif", ".pdf",
        ".parquet", ".pkl", ".bin", ".gz", ".zip",
    }:
        sys.exit(0)

    # Check size
    try:
        size_bytes = os.path.getsize(file_path)
    except OSError:
        sys.exit(0)

    if size_bytes < LARGE_FILE_BYTES:
        sys.exit(0)

    line_count = count_lines(file_path)
    if not line_count or line_count <= LARGE_FILE_LINES:
        sys.exit(0)

    # Load and inject the skill
    skill_content = load_skill()

    header = (
        f"CONTEXT GUARD: {os.path.basename(file_path)} is {line_count} lines "
        f"({size_bytes:,} bytes). "
        f"Apply the following context management strategies:\n"
    )

    if skill_content:
        print(header)
        print(skill_content)
    else:
        # Fallback if skill file is missing
        print(
            header
            + "- Use offset/limit to read specific sections instead of the full file\n"
            + "- Extract key points rather than holding full content in context\n"
            + "- Save large outputs to files, show summaries in chat"
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
