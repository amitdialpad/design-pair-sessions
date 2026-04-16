#!/usr/bin/env python3
from __future__ import annotations
"""
Fetch beacon-app GitHub releases via API, rewrite them for designers using
Claude, detect documentation changes, and update the site content.

What this does on each run:
  1. Fetches latest releases from dialpad/beacon-app
  2. For new releases: fetches PR descriptions for richer context
  3. Rewrites release notes into plain English for designers (whats-new.md)
  4. Detects command/skill/agent renames or additions → patches toolkit.md,
     process.md, cheat-sheet.md automatically
  5. Commits all changed files and triggers a deploy

Required secrets:
  BEACON_PAT            — GitHub PAT with read access to dialpad/beacon-app
  ANTHROPIC_API_KEY     — Claude API key for rewriting and doc patching

Exit codes:
  0 = changes found, files updated
  1 = no new releases
  2 = error
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
WHATS_NEW = PROJECT_DIR / "docs" / "index.md"
MARKER_START = "<!-- BEACON_RELEASES_START -->"
MARKER_END = "<!-- BEACON_RELEASES_END -->"
VISIBLE_COUNT = 8

# Files to scan and patch for command/skill/agent changes
DOC_FILES = [
    "toolkit.md",
    "process.md",
    "cheat-sheet.md",
    "sessions/session-1.md",
    "sessions/session-2.md",
    "sessions/session-3.md",
]

HUMANIZE_PROMPT = """\
You are writing changelog entries for product designers at Dialpad who use \
a tool called Beacon — an AI-assisted design system app built by their tech lead Josh.
{components_section}
Write a two-part structured entry:

HEADLINE: A short phrase (5–8 words max) naming what actually changed. \
Write it like a newspaper headline — specific, no filler, no "now" or "update". \
Good examples: "Power Dialer campaign context in the callbar", \
"AI summary pill gets animated states and share", \
"Contact Center navigation scaffold live", \
"Credits & usage billing page redesigned"

BODY: 1–2 sentences. Say what this means for someone using the tool. \
Use the changed component names above as location clues — e.g. "CallbarPanel.vue" \
means the callbar, "ContactsView.vue" means the Contacts section, \
"LeftSidebarExpandedMenu.vue" means the left nav. Be specific. \
Skip PR numbers, Jira IDs (DDT-1234, NO-JIRA), GitHub usernames \
(@hynes-dialpad etc). If there is an invitation to ask Josh, include it naturally. \
Never use em dashes (—). Break clauses with a period instead.

If the release contains only internal refactors, dependency bumps, or changes \
with no visible impact for designers, respond with exactly: SKIP

Return only HEADLINE and BODY lines — no extra commentary.

Release {tag}:
{notes}"""

DOC_PATCH_PROMPT = """\
You are maintaining documentation for a tool called Beacon used by product designers.

Analyze these merged pull requests and identify any changes to slash commands, \
skills, or agents that need to be reflected in the documentation.

Look for things like:
- Commands renamed (e.g. /feature-dev and /feature-start merged into /feature-team)
- Commands added or removed
- Skills renamed or removed
- Agents renamed or removed

Return a JSON array of changes. Each item must be one of:
  {{"type": "rename", "old": "/old-name", "new": "/new-name"}}
  {{"type": "remove", "name": "/name"}}
  {{"type": "add",    "name": "/name", "description": "what it does"}}

Rules:
- Only include changes explicitly stated in the PRs
- For renames, include one entry per old name (e.g. two entries if two commands merge into one)
- Return [] if no documentation-relevant changes found
- Return ONLY valid JSON, nothing else

Pull requests:
{pr_content}"""


# ── GitHub API helpers ────────────────────────────────────────────────────────

def fetch_releases(per_page: int = 10) -> list | None:
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/releases?per_page={per_page}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"[error] gh api releases failed: {result.stderr.strip()}", file=sys.stderr)
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


def fetch_pr_bodies(release: dict) -> str:
    """
    Fetch full PR descriptions for all PRs linked in a release body.
    Returns a combined string of title + body for each PR.
    """
    body = (release.get("body") or "").strip()
    pr_urls = re.findall(r"https://github\.com/\S+/pull/\d+", body)

    parts = []
    for url in pr_urls[:6]:  # cap at 6 PRs per release
        m = re.search(r"github\.com/(.+)/pull/(\d+)", url)
        if not m:
            continue
        repo, num = m.group(1), m.group(2)
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}/pulls/{num}",
             "--jq", '{"title": .title, "body": (.body // "")}'],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                pr = json.loads(result.stdout)
                title = pr.get("title", "").strip()
                pr_body = pr.get("body", "").strip()
                parts.append(f"PR #{num}: {title}\n\n{pr_body}" if pr_body else f"PR #{num}: {title}")
            except json.JSONDecodeError:
                pass

    return "\n\n---\n\n".join(parts)


# Source dirs and patterns that indicate a visible UI change
_COMPONENT_DIRS = ("src/components/", "src/composables/", "src/views/", "src/config/")
_SKIP_PATTERNS = (".spec.", ".test.", "__tests__")


def fetch_changed_files(tag: str, base_tag: str) -> list[tuple[str, str]]:
    """
    Returns (filename, status) pairs for UI-relevant files changed between
    base_tag and tag. Uses GitHub's compare API. Returns [] on any error.
    Capped at 25 files to keep prompt size manageable.
    """
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/compare/{base_tag}...{tag}",
         "--jq", "[.files[] | {name: .filename, status: .status}]"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []

    try:
        files = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    relevant = []
    for f in files:
        name = f.get("name", "")
        status = f.get("status", "modified")
        if not any(name.startswith(d) for d in _COMPONENT_DIRS):
            continue
        if any(p in name for p in _SKIP_PATTERNS):
            continue
        relevant.append((name.split("/")[-1], status))

    return relevant[:25]


# ── Claude API helpers ────────────────────────────────────────────────────────

def _claude(prompt: str, max_tokens: int = 400) -> str | None:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
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


def humanize_release(
    tag: str,
    notes: str,
    changed_files: list[tuple[str, str]] | None = None,
) -> tuple[str, str] | str | None:
    """
    Rewrite raw release notes for designers.
    Returns (headline, body) tuple, "" (skip), or None (API error — fallback to raw).
    changed_files: list of (filename, status) pairs from fetch_changed_files().
    """
    if changed_files:
        lines = "\n".join(f"  - {name} ({status})" for name, status in changed_files)
        components_section = f"\nChanged components in this release:\n{lines}\n"
    else:
        components_section = ""

    result = _claude(HUMANIZE_PROMPT.format(
        tag=tag,
        notes=notes.strip(),
        components_section=components_section,
    ), max_tokens=500)
    if result is None:
        return None
    if result.strip() == "SKIP":
        return ""

    headline = ""
    body_parts: list[str] = []
    in_body = False
    for line in result.strip().splitlines():
        if line.startswith("HEADLINE:"):
            headline = line[len("HEADLINE:"):].strip()
        elif line.startswith("BODY:"):
            body_parts.append(line[len("BODY:"):].strip())
            in_body = True
        elif in_body and line.strip():
            body_parts.append(line.strip())

    body = " ".join(body_parts).strip()
    return (headline, body) if headline else None


def extract_doc_patches(new_releases: list) -> list[dict]:
    """
    Identify command/skill/agent changes in new releases by reading PR bodies.
    Returns list of {type, old/new/name} patch descriptors.
    """
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return []

    pr_content_parts = []
    for release in sorted(new_releases, key=lambda r: r["published_at"]):
        pr_bodies = fetch_pr_bodies(release)
        if pr_bodies:
            pr_content_parts.append(f"=== {release['tag_name']} ===\n{pr_bodies}")

    if not pr_content_parts:
        return []

    pr_content = "\n\n".join(pr_content_parts)
    result = _claude(DOC_PATCH_PROMPT.format(pr_content=pr_content), max_tokens=600)
    if not result:
        return []

    # Strip markdown code fences if Claude wrapped the JSON
    result = re.sub(r"^```(?:json)?\s*", "", result)
    result = re.sub(r"\s*```$", "", result)

    try:
        patches = json.loads(result)
        return patches if isinstance(patches, list) else []
    except json.JSONDecodeError:
        print(f"[warn] Could not parse doc patches JSON: {result[:200]}", file=sys.stderr)
        return []


# ── Doc patching ──────────────────────────────────────────────────────────────

def apply_doc_patches(patches: list[dict]) -> list[Path]:
    """
    Apply rename patches to doc files. Logs add/remove for manual follow-up.
    Returns list of file paths that were modified.
    """
    if not patches:
        return []

    modified = []

    for patch in patches:
        ptype = patch.get("type", "")

        if ptype == "rename":
            old = patch.get("old", "").strip()
            new = patch.get("new", "").strip()
            if not old or not new or old == new:
                continue

            found_in = []
            for filename in DOC_FILES:
                filepath = PROJECT_DIR / "docs" / filename
                if not filepath.exists():
                    continue
                content = filepath.read_text()
                if old in content:
                    filepath.write_text(content.replace(old, new))
                    found_in.append(filename)
                    if filepath not in modified:
                        modified.append(filepath)

            if found_in:
                print(f"  [docs] renamed '{old}' → '{new}' in: {', '.join(found_in)}")
            else:
                print(f"  [docs] rename '{old}' → '{new}' — not found in docs (may already be updated)")

        elif ptype == "add":
            name = patch.get("name", "").strip()
            desc = patch.get("description", "").strip()
            print(f"  [docs] new item '{name}' detected — add to toolkit.md manually: {desc}")

        elif ptype == "remove":
            name = patch.get("name", "").strip()
            print(f"  [docs] '{name}' was removed — review docs for references manually")

    return modified


# ── State ─────────────────────────────────────────────────────────────────────

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


# ── Formatting ────────────────────────────────────────────────────────────────

def format_date(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.strftime("%-d %B %Y")


def format_release(release: dict, prev_tag: str | None = None) -> str | None:
    tag = release["tag_name"]
    name = (release.get("name") or tag).strip()
    date = format_date(release["published_at"])
    raw_body = (release.get("body") or "").strip().replace("\r\n", "\n")
    link = f"https://github.com/{REPO}/releases/tag/{tag}"

    changed_files = fetch_changed_files(tag, prev_tag) if prev_tag else []
    if changed_files:
        print(f"  {tag}: {len(changed_files)} UI file(s) changed")

    rewritten = humanize_release(tag, raw_body, changed_files) if raw_body else None

    if rewritten is None:
        # API unavailable — fall back to raw notes with tag as headline
        headline = name
        body = raw_body
    elif rewritten == "":
        print(f"  skipping {tag} (internal change, not surfaced in whats-new)")
        return None
    else:
        headline, body = rewritten

    if not headline:
        return None

    formatted = f"**{headline}**"
    if body:
        formatted += f"\n\n{body}"

    meta = f'<span class="release-meta">[{tag}]({link}) · {date}</span>'
    return f"{formatted}\n\n{meta}"


def build_section(releases: list) -> str:
    releases = sorted(releases, key=lambda r: r["published_at"], reverse=True)
    formatted = []
    for i, release in enumerate(releases):
        # The previous release (older) is the next item in the newest-first list
        prev_tag = releases[i + 1]["tag_name"] if i + 1 < len(releases) else None
        entry = format_release(release, prev_tag)
        if entry is not None:
            formatted.append(entry)

    if not formatted:
        return ""

    visible = formatted[:VISIBLE_COUNT]
    older = formatted[VISIBLE_COUNT:]
    parts = list(visible)
    if older:
        inner = "\n\n---\n\n".join(older)
        parts.append(f":::details View older releases\n\n{inner}\n\n:::")
    return "\n\n---\n\n".join(parts)


def update_whats_new(section_content: str) -> bool:
    content = WHATS_NEW.read_text()
    if MARKER_START not in content or MARKER_END not in content:
        print(f"[error] Markers not found in docs/whats-new.md.", file=sys.stderr)
        return False
    replacement = f"{MARKER_START}\n\n{section_content}\n\n{MARKER_END}"
    new_content = re.sub(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        replacement, content, flags=re.DOTALL,
    )
    WHATS_NEW.write_text(new_content)
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    releases = fetch_releases(per_page=30)
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

    new_releases = [r for r in releases if r["id"] > last_id]
    api_mode = "Claude rewrite" if os.environ.get("ANTHROPIC_API_KEY") else "raw notes"
    print(f"Found {len(new_releases)} new release(s). Processing with {api_mode}...")

    # 1. Update whats-new.md
    section = build_section(releases)
    if not section:
        print("All new releases were internal — nothing to surface.")
        sys.exit(1)
    if not update_whats_new(section):
        sys.exit(2)
    print("  whats-new.md updated")

    # 2. Patch docs for command/skill/agent changes
    print("Checking for documentation changes in new release PRs...")
    patches = extract_doc_patches(new_releases)
    if patches:
        print(f"  found {len(patches)} patch(es) — applying to docs...")
        apply_doc_patches(patches)
    else:
        print("  no documentation changes detected")

    save_state(releases)
    latest = max(releases, key=lambda r: r["published_at"])
    print(f"Done. Latest: {latest['tag_name']} ({format_date(latest['published_at'])})")
    sys.exit(0)


if __name__ == "__main__":
    main()
