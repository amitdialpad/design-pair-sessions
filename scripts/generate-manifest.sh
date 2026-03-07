#!/bin/bash
# Generates a manifest of beacon-app's .claude/ directory from GitHub API
# Output: scripts/manifest.json

set -e

REPO="dialpad/beacon-app"
OUTPUT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_FILE="$OUTPUT_DIR/manifest.json"

echo "Fetching .claude/ directory tree from $REPO..."

# Get full recursive tree of .claude/ directory
TREE=$(gh api "repos/$REPO/git/trees/main?recursive=1" --jq '
  .tree[]
  | select(.path | startswith(".claude/"))
  | select(.type == "blob")
  | {path: .path, sha: .sha, size: .size}
' 2>/dev/null)

if [ -z "$TREE" ]; then
  echo "Error: Could not fetch tree from $REPO"
  exit 1
fi

# Build JSON manifest with timestamp
echo "{" > "$OUTPUT_FILE"
echo "  \"repo\": \"$REPO\"," >> "$OUTPUT_FILE"
echo "  \"generated\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$OUTPUT_FILE"
echo "  \"files\": [" >> "$OUTPUT_FILE"

# Convert tree output to JSON array
FIRST=true
echo "$TREE" | while IFS= read -r line; do
  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo "," >> "$OUTPUT_FILE"
  fi
  printf "    %s" "$line" >> "$OUTPUT_FILE"
done

echo "" >> "$OUTPUT_FILE"
echo "  ]" >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

FILE_COUNT=$(echo "$TREE" | wc -l | tr -d ' ')
echo "Manifest written to $OUTPUT_FILE ($FILE_COUNT files)"
