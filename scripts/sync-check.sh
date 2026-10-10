#!/bin/bash
# Record current Design toolkit changes on their own page.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/sync-toolkit.py"
