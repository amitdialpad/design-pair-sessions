#!/bin/bash
# Compares current beacon-app .claude/ state against stored manifest
# Outputs changes to docs/whats-new.md
# Exit code: 0 = changes found, 1 = no changes, 2 = error

set -e

REPO="dialpad/beacon-app"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MANIFEST="$SCRIPT_DIR/manifest.json"
NEW_MANIFEST="$SCRIPT_DIR/manifest.new.json"
WHATS_NEW="$PROJECT_DIR/docs/whats-new.md"
TODAY=$(date -u +%Y-%m-%d)

if [ ! -f "$MANIFEST" ]; then
  echo "No manifest found. Run generate-manifest.sh first."
  exit 2
fi

# Fetch current state
echo "Fetching current .claude/ state from $REPO..."

gh api "repos/$REPO/git/trees/main?recursive=1" --jq '
  .tree[]
  | select(.path | startswith(".claude/"))
  | select(.type == "blob")
  | "\(.path)\t\(.sha)"
' > /tmp/beacon-current.tsv 2>/dev/null

if [ ! -s /tmp/beacon-current.tsv ]; then
  echo "Error: Could not fetch current state"
  exit 2
fi

# Extract old state from manifest
cat "$MANIFEST" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for f in data.get('files', []):
    print(f'{f[\"path\"]}\t{f[\"sha\"]}')
" > /tmp/beacon-old.tsv 2>/dev/null

# Compare
ADDED=$(comm -13 <(cut -f1 /tmp/beacon-old.tsv | sort) <(cut -f1 /tmp/beacon-current.tsv | sort))
REMOVED=$(comm -23 <(cut -f1 /tmp/beacon-old.tsv | sort) <(cut -f1 /tmp/beacon-current.tsv | sort))

# For modified: same path, different sha
MODIFIED=""
while IFS=$'\t' read -r path sha; do
  OLD_SHA=$(grep "^$path	" /tmp/beacon-old.tsv 2>/dev/null | cut -f2)
  if [ -n "$OLD_SHA" ] && [ "$OLD_SHA" != "$sha" ]; then
    MODIFIED="$MODIFIED$path\n"
  fi
done < /tmp/beacon-current.tsv

# Check if anything changed
if [ -z "$ADDED" ] && [ -z "$REMOVED" ] && [ -z "$MODIFIED" ]; then
  echo "No changes detected."
  exit 1
fi

# Categorize changes for human-readable output
categorize() {
  local path="$1"
  case "$path" in
    .claude/commands/*) echo "command" ;;
    .claude/skills/*) echo "skill" ;;
    .claude/agents/*) echo "agent" ;;
    .claude/hooks/*) echo "hook" ;;
    .claude/rules/*) echo "rule" ;;
    *) echo "config" ;;
  esac
}

friendly_name() {
  local path="$1"
  # Extract the meaningful name from the path
  echo "$path" | sed 's|.claude/||' | sed 's|/SKILL.md||' | sed 's|/instructions.md||' | sed 's|\.md$||'
}

# Build the whats-new entry
ENTRY="## $TODAY\n\n"
HAS_CONTENT=false

if [ -n "$ADDED" ]; then
  ENTRY+="### Added\n\n"
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    TYPE=$(categorize "$path")
    NAME=$(friendly_name "$path")
    ENTRY+="- **$TYPE**: \`$NAME\`\n"
    HAS_CONTENT=true
  done <<< "$ADDED"
  ENTRY+="\n"
fi

if [ -n "$MODIFIED" ]; then
  ENTRY+="### Modified\n\n"
  echo -e "$MODIFIED" | while IFS= read -r path; do
    [ -z "$path" ] && continue
    TYPE=$(categorize "$path")
    NAME=$(friendly_name "$path")
    ENTRY+="- **$TYPE**: \`$NAME\`\n"
    HAS_CONTENT=true
  done
  # Re-read since subshell
  ENTRY+=$(echo -e "$MODIFIED" | while IFS= read -r path; do
    [ -z "$path" ] && continue
    TYPE=$(categorize "$path")
    NAME=$(friendly_name "$path")
    echo "- **$TYPE**: \`$NAME\`"
  done)
  ENTRY+="\n\n"
fi

if [ -n "$REMOVED" ]; then
  ENTRY+="### Removed\n\n"
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    TYPE=$(categorize "$path")
    NAME=$(friendly_name "$path")
    ENTRY+="- **$TYPE**: \`$NAME\`\n"
    HAS_CONTENT=true
  done <<< "$REMOVED"
  ENTRY+="\n"
fi

ENTRY+="---\n\n"

# Prepend to whats-new.md (keep history)
if [ -f "$WHATS_NEW" ]; then
  EXISTING=$(tail -n +5 "$WHATS_NEW")  # Skip the header
else
  EXISTING=""
fi

cat > "$WHATS_NEW" << EOF
# What's new in Beacon

Changes detected in [beacon-app/.claude/](https://github.com/dialpad/beacon-app/tree/main/.claude). Updated daily. When changes appear here, the [toolkit](/toolkit) page may need updating.

$(echo -e "$ENTRY")$EXISTING
EOF

# Update manifest
bash "$SCRIPT_DIR/generate-manifest.sh"

echo "Changes detected and written to docs/whats-new.md"
echo "Added: $(echo "$ADDED" | grep -c . || echo 0)"
echo "Modified: $(echo -e "$MODIFIED" | grep -c . || echo 0)"
echo "Removed: $(echo "$REMOVED" | grep -c . || echo 0)"
exit 0
