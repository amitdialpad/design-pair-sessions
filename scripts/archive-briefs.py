#!/usr/bin/env python3
"""
Rebalance the Beacon Brief section in docs/index.md.

After a new issue is prepended between the BEACON_BRIEF markers, this script:
  1. Parses all issues from the section
  2. Keeps the 4 most recent issues visible
  3. Groups older issues by month, each month in a :::details block
  4. Rewrites the section in-place

Issue format expected:
  **Beacon Brief — [date]**
  [content]

Separated by --- between issues.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
INDEX = PROJECT_DIR / "docs" / "index.md"
MARKER_START = "<!-- BEACON_BRIEF_START -->"
MARKER_END = "<!-- BEACON_BRIEF_END -->"
VISIBLE_COUNT = 4


def parse_date(issue_text: str) -> datetime | None:
    """Extract end date from ### Week of D–D Mon YYYY heading."""
    # Match "Week of 7–13 Apr 2026" — use the end date for sorting
    m = re.search(r"Week of\s+\d{1,2}[–\-]+(\d{1,2}\s+\w+\s+\d{4})", issue_text)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1).strip(), "%d %b %Y")
    except ValueError:
        return None


def group_by_month(issues: list[str]) -> str:
    """Group issues by month into :::details blocks."""
    from collections import defaultdict

    by_month: dict[str, list[str]] = defaultdict(list)
    unkeyed = []

    for issue in issues:
        dt = parse_date(issue)
        if dt:
            key = dt.strftime("%B %Y")  # e.g. "April 2026"
            by_month[key].append((dt, issue))
        else:
            unkeyed.append(issue)

    # Sort months newest first
    sorted_months = sorted(by_month.keys(),
                           key=lambda k: datetime.strptime(k, "%B %Y"),
                           reverse=True)

    blocks = []
    for month in sorted_months:
        entries = sorted(by_month[month], key=lambda x: x[0], reverse=True)
        inner = "\n\n---\n\n".join(e for _, e in entries)
        blocks.append(f":::details View {month}\n\n{inner}\n\n:::")

    if unkeyed:
        inner = "\n\n---\n\n".join(unkeyed)
        blocks.append(f":::details View older issues\n\n{inner}\n\n:::")

    return "\n\n".join(blocks)


def rebalance(content: str) -> str:
    """Rewrite the BEACON_BRIEF section with visible + archived groups."""
    start = content.find(MARKER_START)
    end = content.find(MARKER_END)

    if start == -1 or end == -1:
        print("[error] BEACON_BRIEF markers not found", file=sys.stderr)
        return content

    inner = content[start + len(MARKER_START):end].strip()

    # Split into individual issues on --- separators at the top level
    # (not inside :::details blocks)
    issues = []
    buffer = []
    in_details = False

    for line in inner.splitlines():
        if line.startswith(":::details"):
            in_details = True
        if line.strip() == ":::" and in_details:
            in_details = False
            buffer.append(line)
            continue
        if line.strip() == "---" and not in_details:
            text = "\n".join(buffer).strip()
            if text:
                issues.append(text)
            buffer = []
        else:
            buffer.append(line)

    # Catch last issue (no trailing ---)
    text = "\n".join(buffer).strip()
    if text:
        issues.append(text)

    # Flatten any existing :::details blocks back into individual issues
    flat_issues = []
    for issue in issues:
        if issue.startswith(":::details"):
            # Extract inner content from details block
            inner_match = re.search(r":::details[^\n]*\n\n(.*?)\n\n:::", issue, re.DOTALL)
            if inner_match:
                sub_issues = re.split(r"\n\n---\n\n", inner_match.group(1).strip())
                flat_issues.extend(s.strip() for s in sub_issues if s.strip())
        else:
            flat_issues.append(issue)

    if not flat_issues:
        return content

    # Sort all issues by date, newest first
    def sort_key(issue):
        dt = parse_date(issue)
        return dt if dt else datetime.min

    flat_issues.sort(key=sort_key, reverse=True)

    visible = flat_issues[:VISIBLE_COUNT]
    older = flat_issues[VISIBLE_COUNT:]

    parts = ["\n\n---\n\n".join(visible)]
    if older:
        parts.append(group_by_month(older))

    new_inner = "\n\n".join(parts)
    replacement = f"{MARKER_START}\n\n{new_inner}\n\n{MARKER_END}"

    return (
        content[:start]
        + replacement
        + content[end + len(MARKER_END):]
    )


def main():
    content = INDEX.read_text()
    new_content = rebalance(content)
    if new_content != content:
        INDEX.write_text(new_content)
        print("Beacon Brief section rebalanced.")
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
