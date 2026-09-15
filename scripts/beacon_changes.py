#!/usr/bin/env python3
"""Read Beacon changes from the dialpad/design monorepo via the GitHub CLI."""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from urllib.parse import urlencode

REPO = "dialpad/design"
BEACON_PATH = "apps/beacon"
MONOREPO_CUTOVER_AT = "2026-08-26T00:00:00Z"
DESIGNER_FACING_PREFIXES = (
    "apps/beacon/src/",
    "apps/beacon/public/",
    "apps/beacon/data/",
    "apps/beacon/mock-engine/",
)
SKIP_FILE_PATTERNS = (".spec.", ".test.", "/tests/", "__tests__")


class GitHubError(RuntimeError):
    """Raised when GitHub source data cannot be read safely."""


def gh_api(endpoint: str) -> object:
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise GitHubError(result.stderr.strip() or f"GitHub API failed for {endpoint}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise GitHubError(f"GitHub returned invalid JSON for {endpoint}") from error


def fetch_commits(
    *,
    since: datetime | str | None = None,
    until: datetime | str | None = None,
    per_page: int = 100,
) -> list[dict]:
    """Return newest-first commits on main that touched apps/beacon."""
    params: dict[str, str | int] = {
        "sha": "main",
        "path": BEACON_PATH,
        "per_page": per_page,
    }
    if since is not None:
        params["since"] = since.isoformat().replace("+00:00", "Z") if isinstance(since, datetime) else since
    if until is not None:
        params["until"] = until.isoformat().replace("+00:00", "Z") if isinstance(until, datetime) else until

    data = gh_api(f"repos/{REPO}/commits?{urlencode(params)}")
    if not isinstance(data, list):
        raise GitHubError("GitHub commits response was not a list")
    return data


def pull_request_number(commit: dict) -> int | None:
    message = commit.get("commit", {}).get("message", "")
    match = re.search(r"\(#(\d+)\)\s*$", message.splitlines()[0] if message else "")
    return int(match.group(1)) if match else None


def enrich_commit(commit: dict) -> dict:
    """Add PR copy and changed files to a GitHub commit payload."""
    sha = commit.get("sha", "")
    commit_data = commit.get("commit", {})
    message = commit_data.get("message", "")
    title = message.splitlines()[0] if message else sha[:8]
    published_at = commit_data.get("committer", {}).get("date") or commit_data.get("author", {}).get("date")
    pr_number = pull_request_number(commit)

    if pr_number is not None:
        pr = gh_api(f"repos/{REPO}/pulls/{pr_number}")
        files = gh_api(f"repos/{REPO}/pulls/{pr_number}/files?per_page=100")
        if not isinstance(pr, dict) or not isinstance(files, list):
            raise GitHubError(f"Unexpected PR response for #{pr_number}")
        title = pr.get("title") or title
        body = pr.get("body") or ""
        published_at = pr.get("merged_at") or published_at
        link = pr.get("html_url") or f"https://github.com/{REPO}/pull/{pr_number}"
        filenames = [item.get("filename", "") for item in files if isinstance(item, dict)]
    else:
        detail = gh_api(f"repos/{REPO}/commits/{sha}")
        if not isinstance(detail, dict):
            raise GitHubError(f"Unexpected commit response for {sha}")
        body = "\n".join(message.splitlines()[1:]).strip()
        link = commit.get("html_url") or f"https://github.com/{REPO}/commit/{sha}"
        filenames = [item.get("filename", "") for item in detail.get("files", []) if isinstance(item, dict)]

    return {
        "sha": sha,
        "title": title.strip(),
        "body": body.strip(),
        "published_at": published_at,
        "pr_number": pr_number,
        "link": link,
        "files": [name for name in filenames if name],
    }


def new_commits_since(commits: list[dict], last_sha: str | None) -> list[dict]:
    """Return newest-first commits until the saved marker, validating the marker."""
    if not last_sha:
        return commits

    new_commits: list[dict] = []
    for commit in commits:
        if commit.get("sha") == last_sha:
            return new_commits
        new_commits.append(commit)
    raise GitHubError(
        "Saved Beacon commit was not found in the latest GitHub results. "
        "Increase the fetch window before advancing state."
    )


def clean_source_markdown(text: str, limit: int = 2600) -> str:
    """Remove PR-template noise while retaining source claims for the writer."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^]]*]\([^)]*\)", "", text)
    text = re.sub(r"<img\b[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\[[^]]+\]:\s+\S+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:limit].rstrip()


def designer_facing_files(change: dict) -> list[str]:
    """Return changed files that can affect the Beacon experience or its demo data."""
    return [
        name
        for name in change.get("files", [])
        if name.startswith(DESIGNER_FACING_PREFIXES)
        and not any(pattern in name for pattern in SKIP_FILE_PATTERNS)
    ]


def is_designer_facing(change: dict) -> bool:
    """Exclude documentation, chores, CI, and test-only changes from team updates."""
    if re.match(r"^(docs|chore|test|ci|build)(\([^)]*\))?:", change.get("title", ""), flags=re.I):
        return False
    return bool(designer_facing_files(change))
