#!/usr/bin/env python3
"""
Generate a Beacon Brief newsletter issue and prepend it to docs/index.md.

Reads:
  - Recent git log (past 7 days)
  - BEACON_RELEASES section from docs/index.md
  - scripts/weekly-notes.md (if present — updated Wednesday by Amit)

Uses Claude Haiku to write the newsletter, then:
  1. Prepends to the BEACON_BRIEF_START/END section in docs/index.md
  2. Runs archive-briefs.py to rebalance visible/archived issues

Exit codes:
  0 = brief generated and written
  1 = skipped (e.g. already ran this week)
  2 = error
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

PROJECT_DIR = Path(__file__).parent.parent
INDEX        = PROJECT_DIR / "docs" / "index.md"
WEEKLY_NOTES = PROJECT_DIR / "scripts" / "weekly-notes.md"
ARCHIVE_SCRIPT = PROJECT_DIR / "scripts" / "archive-briefs.py"

MARKER_START    = "<!-- BEACON_BRIEF_START -->"
MARKER_END      = "<!-- BEACON_BRIEF_END -->"
RELEASES_START  = "<!-- BEACON_RELEASES_START -->"
RELEASES_END    = "<!-- BEACON_RELEASES_END -->"


# ── Date helpers ──────────────────────────────────────────────────────────────

def get_week_range() -> tuple[str, str, str]:
    """Return (mon_str, sun_str, label) for the current week."""
    today = datetime.now(timezone.utc)
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    mon_str = monday.strftime("%-d %b %Y")
    sun_str = sunday.strftime("%-d %b %Y")
    # Short label e.g. "7–13 Apr 2026"
    label = f"{monday.day}–{sun_str}"
    return mon_str, sun_str, label


# ── Source material ───────────────────────────────────────────────────────────

def get_git_log() -> str:
    result = subprocess.run(
        ["git", "-C", str(PROJECT_DIR), "log", "--oneline", "--since=7 days ago"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() or "No commits this week."


def get_releases_section() -> str:
    content = INDEX.read_text()
    start = content.find(RELEASES_START)
    end   = content.find(RELEASES_END)
    if start == -1 or end == -1:
        return ""
    return content[start + len(RELEASES_START):end].strip()


def get_weekly_notes() -> str:
    if WEEKLY_NOTES.exists():
        text = WEEKLY_NOTES.read_text().strip()
        return text if text else ""
    return ""


# ── Claude API ────────────────────────────────────────────────────────────────

def _claude(prompt: str, max_tokens: int = 900) -> str | None:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("[error] ANTHROPIC_API_KEY not set", file=sys.stderr)
        return None
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": max_tokens,
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
            return data["content"][0]["text"].strip()
    except (URLError, Exception) as e:
        print(f"[warn] Claude API error: {e}", file=sys.stderr)
        return None


BRIEF_PROMPT = """\
You are writing the Beacon Brief — a weekly newsletter for product designers at Dialpad.
Beacon is a prototyping tool built by their tech lead Josh. Designers use it with Claude Code to build and test UI.

Write in plain, human English. Like a colleague catching up a teammate after a week away.
Short sentences. No em dashes. No corporate language. No filler phrases like "it is worth noting".
Be specific. Name the command or feature. Explain what it actually does.

Week: {week_range}

What shipped in Beacon this week:
{releases}
{notes_section}
Recent repo commits (for context on what changed in the docs/site):
{git_log}

Write the newsletter in this exact format. If a section has nothing real to say, write one honest sentence. Do not pad.

### Week of {week_range}

#### What actually changed
[Specific commands, features, or data model changes that shipped. Name them. Explain what they do or unlock.]

#### The bigger shift
[A pattern across what shipped, or a change in how Beacon works. Write as an observation. No attribution to any person or meeting.]

#### Where things are still messy
[What is in progress, unresolved, or known to be incomplete right now.]

#### What's coming next
[What is likely next based on the material. Write as an observation about where things are heading.]

#### Try this
[One concrete thing to try in Beacon this week. Be specific. Make it feel like a tip from someone who already did it.]

#### Quick notes
- [Short bullet]
- [Short bullet]
- [Short bullet]

#### One thing to remember
[One sentence. The most important thing to carry into the week.]

Return only the newsletter text, starting with ### Week of..."""


def generate_brief(week_range: str, releases: str, git_log: str, notes: str) -> str | None:
    notes_section = f"\nAmit's notes from this week:\n{notes}\n" if notes else ""
    prompt = BRIEF_PROMPT.format(
        week_range=week_range,
        releases=releases or "No new Beacon releases this week.",
        git_log=git_log,
        notes_section=notes_section,
    )
    return _claude(prompt)


# ── File update ───────────────────────────────────────────────────────────────

def prepend_to_brief(content: str, issue: str) -> str:
    start = content.find(MARKER_START)
    end   = content.find(MARKER_END)
    if start == -1 or end == -1:
        print("[error] BEACON_BRIEF markers not found in index.md", file=sys.stderr)
        return content
    existing = content[start + len(MARKER_START):end].strip()
    new_inner = issue + ("\n\n---\n\n" + existing if existing else "")
    return (
        content[:start]
        + MARKER_START + "\n\n"
        + new_inner + "\n\n"
        + MARKER_END
        + content[end + len(MARKER_END):]
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    _, _, week_range = get_week_range()
    print(f"Generating Beacon Brief for week of {week_range}...")

    releases = get_releases_section()
    git_log  = get_git_log()
    notes    = get_weekly_notes()

    print(f"  Weekly notes: {'found' if notes else 'not found, generating from releases + commits'}")

    issue = generate_brief(week_range, releases, git_log, notes)
    if not issue:
        sys.exit(2)

    print("  Writing to docs/index.md...")
    content     = INDEX.read_text()
    new_content = prepend_to_brief(content, issue)
    INDEX.write_text(new_content)

    print("  Rebalancing archive...")
    result = subprocess.run(["python3", str(ARCHIVE_SCRIPT)], capture_output=True, text=True)
    print(f"  {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"[warn] archive-briefs: {result.stderr.strip()}", file=sys.stderr)

    print(f"Done. Week of {week_range} added.")
    sys.exit(0)


if __name__ == "__main__":
    main()
