#!/bin/bash
# Fetches the latest 5 items from feed_claude.xml and updates the
# <!-- CLAUDE_FEED_START --> ... <!-- CLAUDE_FEED_END --> block in whats-new.md

set -e

FEED_URL="https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_claude.xml"
TARGET="docs/whats-new.md"
FEED_TMP=$(mktemp)

# Download feed
curl -sf "$FEED_URL" -o "$FEED_TMP"
if [ ! -s "$FEED_TMP" ]; then
  echo "Feed fetch failed or empty — skipping update"
  rm -f "$FEED_TMP"
  exit 0
fi

# Parse and replace using Python
python3 - "$FEED_TMP" "$TARGET" <<'PYEOF'
import sys, re, xml.etree.ElementTree as ET
from datetime import datetime

feed_file = sys.argv[1]
target    = sys.argv[2]

with open(feed_file) as f:
    root = ET.fromstring(f.read())

items = root.findall('.//item')[:5]
lines = []
for item in items:
    title = (item.findtext('title') or '').strip()
    link  = (item.findtext('link')  or '').strip()
    pub   = (item.findtext('pubDate') or '').strip()
    try:
        dt = datetime.strptime(pub, '%a, %d %b %Y %H:%M:%S %z')
        date_str = dt.strftime('%b %-d, %Y')
    except Exception:
        date_str = pub
    lines.append(f'- **[{title}]({link})** — {date_str}')

updated = datetime.utcnow().strftime('%B %-d, %Y')
new_block = (
    '<!-- CLAUDE_FEED_START -->\n'
    + '\n'.join(lines)
    + f'\n\n*Updated {updated}*\n'
    + '<!-- CLAUDE_FEED_END -->'
)

with open(target) as f:
    content = f.read()

content = re.sub(
    r'<!-- CLAUDE_FEED_START -->.*?<!-- CLAUDE_FEED_END -->',
    new_block,
    content,
    flags=re.DOTALL
)

with open(target, 'w') as f:
    f.write(content)

print(f'Claude feed updated with {len(lines)} items')
PYEOF

rm -f "$FEED_TMP"
