#!/usr/bin/env bash
# Fetch recommended external plugins and rebuild the marketplace.
# Run after cloning: ./setup.sh

set -e
cd "$(dirname "$0")"

echo "=== Fetching external plugins ==="

fetch_if_missing() {
    local repo="$1"
    local name="${repo##*/}"
    if [ -d "external/$name" ]; then
        echo "  $name already exists, skipping (use scripts/update.py to update)"
    else
        python3 scripts/fetch.py "github:$repo"
    fi
}

fetch_if_missing "humanplane/homunculus"
fetch_if_missing "EveryInc/compound-engineering-plugin"

echo ""
echo "=== Building marketplace ==="
python3 scripts/build.py
