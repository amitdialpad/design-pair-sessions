#!/usr/bin/env python3
"""Sync designer-facing Beacon changes from the dialpad/design monorepo."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from beacon_changes import (
    MONOREPO_CUTOVER_AT,
    REPO,
    GitHubError,
    clean_source_markdown,
    enrich_commit,
    fetch_commits,
    new_commits_since,
)

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
STATE_FILE = SCRIPT_DIR / "last-beacon-change.json"
WHATS_NEW = PROJECT_DIR / "docs" / "index.md"
MARKER_START = "<!-- BEACON_RELEASES_START -->"
MARKER_END = "<!-- BEACON_RELEASES_END -->"
VISIBLE_COUNT = 8

_VISIBLE_PREFIXES = (
    "apps/beacon/src/",
    "apps/beacon/public/",
    "apps/beacon/data/",
    "apps/beacon/mock-engine/",
)
_SKIP_FILE_PATTERNS = (".spec.", ".test.", "/tests/", "__tests__")


def _designer_facing_files(change: dict) -> list[str]:
    return [
        name
        for name in change.get("files", [])
        if name.startswith(_VISIBLE_PREFIXES) and not any(pattern in name for pattern in _SKIP_FILE_PATTERNS)
    ]


def summarize_change(change: dict) -> tuple[str, str] | None:
    """Create a conservative entry directly from the PR title and description."""
    if re.match(r"^(docs|chore|test|ci|build)(\([^)]*\))?:", change["title"], flags=re.I):
        return None
    if not _designer_facing_files(change):
        return None

    title = re.sub(r"^(feat|fix|bug|refactor)(\([^)]*\))?:\s*", "", change["title"], flags=re.I)
    title = re.sub(r"^(?:[A-Z]+-\d+|NO-JIRA)\s+", "", title, flags=re.I)
    title = re.sub(r"\s*\(#\d+\)\s*$", "", title).strip()
    if not title:
        return None
    headline = title[0].upper() + title[1:]
    headline = re.sub(r"\bAi\b", "AI", headline)
    headline = re.sub(r"(?i)\bAI receptionist\b", "AI Receptionist", headline)

    notes = clean_source_markdown(change.get("body", ""), limit=1800)
    section = re.search(
        r"(?ims)^##\s+(?:[^\n]*?(?:summary|description))[^\n]*\n+(.*?)(?=^##\s+|\Z)",
        notes,
    )
    body_source = section.group(1).strip() if section else notes
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body_source) if p.strip() and not p.startswith("-")]
    body = " ".join(paragraphs[:2])
    body = re.sub(r"`([^`]+)`", r"\1", body)
    body = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", body)
    body = re.sub(r"\s+", " ", body).strip()
    if len(body) > 700:
        body = body[:697].rstrip() + "..."
    return headline, body


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"repo": REPO, "path": "apps/beacon", "last_commit_sha": None}
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError as error:
        raise GitHubError(f"Invalid state file: {STATE_FILE}") from error


def save_state(latest_commit: dict) -> None:
    state = {
        "repo": REPO,
        "path": "apps/beacon",
        "last_commit_sha": latest_commit["sha"],
        "last_commit_at": latest_commit.get("commit", {}).get("committer", {}).get("date"),
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def format_date(iso_string: str) -> str:
    return datetime.fromisoformat(iso_string.replace("Z", "+00:00")).strftime("%-d %B %Y")


def format_change(change: dict, headline: str, body: str) -> str:
    ref = f"dialpad/design#{change['pr_number']}" if change.get("pr_number") else change["sha"][:8]
    meta = f'<span class="release-meta">[{ref}]({change["link"]}) · {format_date(change["published_at"])}</span>'
    entry = f"<!-- beacon-change:{change['sha']} -->\n\n**{headline}**"
    if body:
        entry += f"\n\n{body}"
    return f"{entry}\n\n{meta}"


def read_existing_entries() -> list[str]:
    content = WHATS_NEW.read_text()
    start = content.find(MARKER_START)
    end = content.find(MARKER_END)
    if start == -1 or end == -1:
        raise GitHubError("Beacon change markers are missing from docs/index.md")
    inner = content[start + len(MARKER_START) : end].strip()
    inner = re.sub(r":::details View older (?:releases|updates)\s*", "", inner, count=1)
    inner = re.sub(r"\s*:::\s*$", "", inner)
    return [entry.strip() for entry in re.split(r"\n\n---\n\n", inner) if entry.strip()]


def build_section(entries: list[str]) -> str:
    visible = entries[:VISIBLE_COUNT]
    older = entries[VISIBLE_COUNT:]
    parts = list(visible)
    if older:
        older_content = "\n\n---\n\n".join(older)
        parts.append(f":::details View older updates\n\n{older_content}\n\n:::")
    return "\n\n---\n\n".join(parts)


def update_whats_new(entries: list[str]) -> None:
    content = WHATS_NEW.read_text()
    replacement = f"{MARKER_START}\n\n{build_section(entries)}\n\n{MARKER_END}"
    updated = re.sub(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        replacement,
        content,
        flags=re.DOTALL,
    )
    if updated == content:
        raise GitHubError("Beacon change section was not updated")
    WHATS_NEW.write_text(updated)


def main() -> None:
    try:
        state = load_state()
        last_sha = state.get("last_commit_sha") if state.get("repo") == REPO else None
        commits = fetch_commits(since=None if last_sha else MONOREPO_CUTOVER_AT)
        if not commits:
            print("No Beacon commits found in the monorepo.")
            sys.exit(1)
        new_commits = new_commits_since(commits, last_sha)
        if not new_commits:
            print(f"No new Beacon changes (latest already synced: {last_sha[:8]}).")
            sys.exit(1)

        changes = [enrich_commit(commit) for commit in new_commits]
        existing_entries = read_existing_entries()
        known_shas = set(re.findall(r"<!-- beacon-change:([0-9a-f]+) -->", "\n".join(existing_entries)))
        new_entries = []
        for change in changes:
            if change["sha"] in known_shas:
                continue
            rewritten = summarize_change(change)
            if rewritten is None:
                print(f"  skipping {change['sha'][:8]} (no designer-facing change)")
                continue
            headline, body = rewritten
            new_entries.append(format_change(change, headline, body))

        if new_entries:
            update_whats_new(new_entries + existing_entries)
            print(f"Updated What's new with {len(new_entries)} monorepo change(s).")
        else:
            print("No new designer-facing entries to add.")

        save_state(commits[0])
        print(f"Done. Latest monorepo Beacon commit: {commits[0]['sha'][:8]}")
    except GitHubError as error:
        print(f"[error] {error}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
