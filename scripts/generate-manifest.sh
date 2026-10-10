#!/bin/bash
# Explicitly seed a Design baseline without logging the migration as changes.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/sync-toolkit.py" --baseline
