#!/usr/bin/env python3
"""
Fetch beacon-app GitHub releases via API, rewrite them for designers using
Claude, and update the <!-- BEACON_RELEASES_START/END --> block in docs/whats-new.md.

Required secrets:
  BEACON_PAT       — GitHub PAT with read access to dialpad/beacon-app
  ANTHROPIC_API_KEY — (optional) enables human-readable rewriting via Claude

Exit codes:
  0 = new releases found, whats-new.md updated
  1 = no new releases (skip commit)
  2 = error (API failure, markers missing, etc.)
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO = "dialpad/beacon-app"
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
STATE_FILE = SCRIPT_DIR / "last-beacon-release.json"
WHATS_NEW = PROJECT_DIR / "docs" / "whats-new.md"
MARKER_START = "<!-- BEACON_RELEASES_START -->"
MARKER_END = "<!-- BEACON_RELEASES_END -->"
VISIBLE_COUNT = 4

HUMANIZE_PROMPT = """\
You are updating a changelog page for product designers at Dialpad who use \
a tool called Beacon — an AI-assisted design system app built by their tech lead Josh.

Convert these GitHub release notes into a plain-English update entry that \
designers would find useful. Focus on what actually changed for users of the \
tool, not implementation details. Skip PR numbers, Jira ticket IDs \
(like DDT-1234 or NO-JIRA), and GitHub usernames (@hynes-dialpad etc).

Write 1–3 short paragraphs. Be specific about what the feature or change \
actually does or enables. Use the same concise, human style as these examples:

- "New `/debug-trace` command: adds debug logs to the code you point at, \
outputs runtime state to the console. Use it when you're going in circles on a bug."
- "BeaconComposer recipe is live with dedicated content slots and rich text \
rendering in conversation rows."
- "`/breadboard` command significantly enhanced with better chunking, navigation \
wiring rules, and support for multi-system diagrams."
- "New Contact Center schema: contact centers, memberships, settings, managed \
phone numbers, operator skills, operating hour profiles. The data layer is built. \
UI is next. Ask Josh if you want to start it."
- "New licenses/SKU data layer in Beacon. `billingPlanUsage` replaced with \
time-filtered usage — so usage data now reflects a real date window, not a snapshot."

If the release contains only internal refactors, dependency bumps, or changes \
with no visible impact for designers, respond with exactly: SKIP

Release {tag}:
{notes}"""


def fetch_releases(per_page: int = 10) -> list | None:
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/releases?per_page={per_page}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[error] gh api failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    try:
        data = json.loads(result.stdout)
        if isinstance(data, dict) and "message" in data:
            print(f"[error] GitHub API: {data['message']}", file=sys.stderr)
            return None
        return data
    except json.JSONDecodeError:
        print("[error] Could not parse releases JSON", file=sys.stderr)
        return None


def humanize_release(tag: str, raw_notes: str) -> str | None:
    """
    Use Claude to rewrite technical release notes for designers.
    Returns rewritten text, empty string (SKIP), or None (use raw notes as fallback).
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return None  # no key — caller will use raw notes

    prompt = HUMANIZE_PROMPT.format(tag=tag, notes=raw_notes.strip())
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}],
    }

    req = Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            text = data["content"][0]["text"].strip()
            return "" if text == "SKIP" else text
    except (URLError, Exception) as e:
        print(f"[warn] Claude API call failed for {tag}: {e}", file=sys.stderr)
        return None  # fallback to raw notes


def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_release_id": 0, "last_release_tag": None}


def save_state(releases: list) -> None:
    latest = max(releases, key=lambda r: r["published_at"])
    state = {
        "last_release_id": latest["id"],
        "last_release_tag": latest["tag_name"],
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def format_date(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.strftime("%-d %B %Y")


def format_release(release: dict) -> str | None:
    tag = release["tag_name"]
    name = (release.get("name") or tag).strip()
    date = format_date(release["published_at"])
    raw_body = (release.get("body") or "").strip().replace("\r\n", "\n")
    link = f"https://github.com/{REPO}/releases/tag/{tag}"

    # Try to get a designer-readable version
    rewritten = humanize_release(tag, raw_body) if raw_body else None

    if rewritten is None:
        # No API key or API failed — use raw notes
        body = raw_body
    elif rewritten == "":
        # Claude said SKIP — internal change, not worth surfacing
        print(f"  skipping {tag} (internal change)")
        return None
    else:
        body = rewritten

    lines = [f"**[{name}]({link}) — {date}**"]
    if body:
        lines += ["", body]
    lines += ["", "---"]
    return "\n".join(lines)


def build_section(releases: list) -> str:
    releases = sorted(releases, key=lambda r: r["published_at"], reverse=True)

    formatted = []
    for r in releases:
        entry = format_release(r)
        if entry is not None:
            formatted.append(entry)

    if not formatted:
        return ""

    visible = formatted[:VISIBLE_COUNT]
    older = formatted[VISIBLE_COUNT:]

    parts = list(visible)
    if older:
        inner = "\n\n".join(older)
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
    releases = fetch_releases(per_page=10)
    if releases is None:
        sys.exit(2)

    releases = [r for r in releases if not r["draft"] and not r["prerelease"]]
    if not releases:
        print("No published releases found.")
        sys.exit(1)

    state = load_state()
    last_id = state.get("last_release_id", 0)
    latest_id = max(r["id"] for r in releases)

    if latest_id <= last_id:
        print(f"No new releases (latest already synced: {state.get('last_release_tag')}).")
        sys.exit(1)

    new_count = sum(1 for r in releases if r["id"] > last_id)
    api_mode = "Claude rewrite" if os.environ.get("ANTHROPIC_API_KEY") else "raw notes"
    print(f"Found {new_count} new release(s). Processing with {api_mode}...")

    section = build_section(releases)

    if not section:
        print("All new releases were internal — nothing to surface.")
        sys.exit(1)

    if not update_whats_new(section):
        sys.exit(2)

    save_state(releases)
    latest = max(releases, key=lambda r: r["published_at"])
    print(f"Done. Latest: {latest['tag_name']} ({format_date(latest['published_at'])})")
    sys.exit(0)


if __name__ == "__main__":
    main()
