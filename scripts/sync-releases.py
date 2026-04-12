#!/usr/bin/env python3
"""
Fetch beacon-app GitHub releases and update the <!-- BEACON_RELEASES_START/END -->
block in docs/whats-new.md.

Exit codes:
  0 = new release(s) found, whats-new.md updated
  1 = no new releases (skip commit)
  2 = error (API failure, missing markers, etc.)
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "dialpad/beacon-app"
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
STATE_FILE = SCRIPT_DIR / "last-beacon-release.json"
WHATS_NEW = PROJECT_DIR / "docs" / "whats-new.md"
MARKER_START = "<!-- BEACON_RELEASES_START -->"
MARKER_END = "<!-- BEACON_RELEASES_END -->"
VISIBLE_COUNT = 4  # releases shown before the :::details block


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


def format_release(release: dict) -> str:
    tag = release["tag_name"]
    name = (release.get("name") or tag).strip()
    date = format_date(release["published_at"])
    body = (release.get("body") or "").strip()

    # Normalize Windows line endings from GitHub
    body = body.replace("\r\n", "\n").replace("\r", "\n")

    lines = [f"**{name} — {date}**"]
    if body:
        lines += ["", body]
    lines += ["", "---"]
    return "\n".join(lines)


def build_section(releases: list) -> str:
    """Build the full block to insert between the markers (newest first)."""
    releases = sorted(releases, key=lambda r: r["published_at"], reverse=True)

    visible = releases[:VISIBLE_COUNT]
    older = releases[VISIBLE_COUNT:]

    parts = [format_release(r) for r in visible]

    if older:
        inner = "\n\n".join(format_release(r) for r in older)
        parts.append(f":::details View older releases\n\n{inner}\n\n:::")

    return "\n\n".join(parts)


def update_whats_new(section_content: str) -> bool:
    content = WHATS_NEW.read_text()

    if MARKER_START not in content or MARKER_END not in content:
        print(
            f"[error] Markers not found in docs/whats-new.md.\n"
            f"  Add {MARKER_START} and {MARKER_END} to the Beacon section.",
            file=sys.stderr,
        )
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
    all_releases = fetch_releases(per_page=10)

    if all_releases is None:
        sys.exit(2)

    # Only published, non-draft, non-prerelease
    releases = [r for r in all_releases if not r["draft"] and not r["prerelease"]]

    if not releases:
        print("No published releases found.")
        sys.exit(1)

    state = load_state()
    last_id = state["last_release_id"]
    latest_id = max(r["id"] for r in releases)

    if latest_id <= last_id:
        print(f"No new releases (latest already synced: {state['last_release_tag']}).")
        sys.exit(1)

    new_count = sum(1 for r in releases if r["id"] > last_id)
    print(f"Found {new_count} new release(s). Updating docs/whats-new.md...")

    section = build_section(releases)

    if not update_whats_new(section):
        sys.exit(2)

    save_state(releases)
    latest = max(releases, key=lambda r: r["published_at"])
    print(f"Done. Latest: {latest['tag_name']} ({format_date(latest['published_at'])})")
    sys.exit(0)


if __name__ == "__main__":
    main()
