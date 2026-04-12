#!/bin/bash
# Fetches the latest 5 items from feed_claude.xml, pulls og:description from
# each post, and updates the <!-- CLAUDE_FEED_START/END --> block in whats-new.md

set -e

FEED_URL="https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_claude.xml"
TARGET="docs/index.md"
FEED_TMP=$(mktemp)

# Download feed
curl -sf "$FEED_URL" -o "$FEED_TMP"
if [ ! -s "$FEED_TMP" ]; then
  echo "Feed fetch failed or empty — skipping update"
  rm -f "$FEED_TMP"
  exit 0
fi

# Parse, fetch descriptions, and replace block using Python
python3 - "$FEED_TMP" "$TARGET" <<'PYEOF'
import sys, re, html, xml.etree.ElementTree as ET
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

def fetch_description(url):
    """Fetch og:description or meta description from a blog post."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as resp:
            page = resp.read(32768).decode('utf-8', errors='ignore')
        # Try og:description and meta description in both attribute orders
        patterns = [
            r'property=["\']og:description["\'][^>]+content=["\']([^"\']{10,})["\']',
            r'content=["\']([^"\']{10,})["\'][^>]+property=["\']og:description["\']',
            r'name=["\']description["\'][^>]+content=["\']([^"\']{10,})["\']',
            r'content=["\']([^"\']{10,})["\'][^>]+name=["\']description["\']',
        ]
        for pattern in patterns:
            m = re.search(pattern, page, re.IGNORECASE)
            if m:
                return html.unescape(m.group(1)).strip()
    except (URLError, Exception):
        pass
    return ''

feed_file = sys.argv[1]
target    = sys.argv[2]

with open(feed_file) as f:
    root = ET.fromstring(f.read())

VISIBLE = 4
items = root.findall('.//item')[:9]
blocks = []

for item in items:
    title    = (item.findtext('title')   or '').strip()
    link     = (item.findtext('link')    or '').strip()
    category = (item.findtext('category') or '').strip()
    pub      = (item.findtext('pubDate') or '').strip()

    try:
        dt = datetime.strptime(pub, '%a, %d %b %Y %H:%M:%S %z')
        date_str = dt.strftime('%b %-d, %Y')
    except Exception:
        date_str = pub

    desc = fetch_description(link)

    # Build newspaper-style block
    meta = date_str
    if category:
        meta += f' · {category}'

    block = f'**[{title}]({link})**<br><small>{meta}</small>'
    if desc:
        block += f'\n\n{desc}'

    blocks.append(block)
    print(f'  fetched: {title[:60]}', flush=True)

updated = datetime.utcnow().strftime('%B %-d, %Y')
separator = '\n\n---\n\n'

visible_blocks = blocks[:VISIBLE]
older_blocks = blocks[VISIBLE:]

body = separator.join(visible_blocks)

if older_blocks:
    body += '\n\n:::details View past updates\n\n'
    body += separator.join(older_blocks)
    body += '\n\n:::'

new_block = (
    '<!-- CLAUDE_FEED_START -->\n'
    + body
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

print(f'Claude feed updated with {len(blocks)} items')
PYEOF

rm -f "$FEED_TMP"
