#!/usr/bin/env python3
"""
Fetch beacon-app releases via GitHub Atom feed and update the
<!-- BEACON_RELEASES_START/END --> block in docs/whats-new.md.

No authentication required — uses the public releases Atom feed,
same approach as sync-claude-feed.sh uses for the Claude RSS feed.

Exit codes:
  0 = new releases found, whats-new.md updated
  1 = no new releases (skip commit)
  2 = error (feed unavailable, private repo, markers missing, etc.)
"""

import html as html_lib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

FEED_URL = "https://github.com/dialpad/beacon-app/releases.atom"
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
STATE_FILE = SCRIPT_DIR / "last-beacon-release.json"
WHATS_NEW = PROJECT_DIR / "docs" / "whats-new.md"
MARKER_START = "<!-- BEACON_RELEASES_START -->"
MARKER_END = "<!-- BEACON_RELEASES_END -->"
VISIBLE_COUNT = 4

NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch_atom() -> str | None:
    try:
        req = Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except URLError as e:
        print(f"[error] Could not fetch Atom feed: {e}", file=sys.stderr)
        return None


def html_to_md(raw: str) -> str:
    """Convert GitHub-rendered HTML back to readable markdown."""
    text = html_lib.unescape(raw)

    # Code blocks — handle before other tags
    text = re.sub(
        r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
        lambda m: "\n```\n" + html_lib.unescape(m.group(1)).strip() + "\n```\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)

    # Headers
    for level in range(6, 0, -1):
        text = re.sub(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            lambda m, l=level: "\n" + "#" * l + " " + m.group(1).strip() + "\n",
            text,
            flags=re.DOTALL,
        )

    # Emphasis
    text = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", text, flags=re.DOTALL)
    text = re.sub(r"<i[^>]*>(.*?)</i>", r"*\1*", text, flags=re.DOTALL)

    # Links
    text = re.sub(
        r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL
    )

    # Horizontal rule
    text = re.sub(r"<hr\s*/?>", "\n---\n", text)

    # Lists
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"\n- \1", text, flags=re.DOTALL)
    text = re.sub(r"</?[uo]l[^>]*>", "", text)

    # Paragraphs and line breaks
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\1\n", text, flags=re.DOTALL)

    # Strip remaining tags
    text = re.sub(r"<[^>]+>", "", text)

    # Normalise whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_entries(xml_text: str) -> list | None:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"[error] Could not parse Atom XML: {e}", file=sys.stderr)
        return None

    entries = []
    for entry in root.findall("atom:entry", NS):
        entry_id = entry.findtext("atom:id", default="", namespaces=NS)
        title = entry.findtext("atom:title", default="", namespaces=NS).strip()
        updated = entry.findtext("atom:updated", default="", namespaces=NS).strip()
        link_el = entry.find("atom:link", NS)
        link = link_el.get("href", "") if link_el is not None else ""
        content_el = entry.find("atom:content", NS)
        content_html = (content_el.text or "") if content_el is not None else ""

        entries.append(
            {
                "id": entry_id,
                "title": title,
                "updated": updated,
                "link": link,
                "body": html_to_md(content_html) if content_html.strip() else "",
            }
        )

    return entries  # Atom feeds are newest-first


def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_release_id": "", "last_release_title": None}


def save_state(entries: list) -> None:
    latest = entries[0]
    state = {
        "last_release_id": latest["id"],
        "last_release_title": latest["title"],
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def format_date(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.strftime("%-d %B %Y")


def format_entry(entry: dict) -> str:
    date = format_date(entry["updated"])
    title = entry["title"]
    body = entry["body"]
    link = entry["link"]

    lines = [f"**[{title}]({link}) — {date}**"]
    if body:
        lines += ["", body]
    lines += ["", "---"]
    return "\n".join(lines)


def build_section(entries: list) -> str:
    visible = entries[:VISIBLE_COUNT]
    older = entries[VISIBLE_COUNT:]

    parts = [format_entry(e) for e in visible]

    if older:
        inner = "\n\n".join(format_entry(e) for e in older)
        parts.append(f":::details View older releases\n\n{inner}\n\n:::")

    return "\n\n".join(parts)


def update_whats_new(section_content: str) -> bool:
    content = WHATS_NEW.read_text()

    if MARKER_START not in content or MARKER_END not in content:
        print(f"[error] Markers not found in docs/whats-new.md.", file=sys.stderr)
        return False

    replacement = f"{MARKER_START}\n\n{section_content}\n\n{MARKER_END}"
    new_content = re.sub(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        replacement,
        content,
        flags=re.DOTALL,
    )
    WHATS_NEW.write_text(new_content)
    return True


def main():
    xml_text = fetch_atom()
    if xml_text is None:
        sys.exit(2)

    # Reject HTML responses (login page redirect for private repos)
    if "<feed" not in xml_text[:1000] and "<?xml" not in xml_text[:100]:
        print(
            "[error] Response is not an Atom feed — repo may be private or URL changed.",
            file=sys.stderr,
        )
        sys.exit(2)

    entries = parse_entries(xml_text)
    if not entries:
        print("No entries in feed.")
        sys.exit(1)

    state = load_state()
    last_id = state.get("last_release_id", "")
    latest_id = entries[0]["id"]

    if latest_id == last_id:
        print(f"No new releases (latest already synced: {state.get('last_release_title')}).")
        sys.exit(1)

    ids = [e["id"] for e in entries]
    new_count = ids.index(last_id) if last_id in ids else len(entries)
    print(f"Found {new_count} new release(s). Updating docs/whats-new.md...")

    section = build_section(entries)

    if not update_whats_new(section):
        sys.exit(2)

    save_state(entries)
    print(f"Done. Latest: {entries[0]['title']} ({format_date(entries[0]['updated'])})")
    sys.exit(0)


if __name__ == "__main__":
    main()
