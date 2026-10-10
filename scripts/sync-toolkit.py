#!/usr/bin/env python3
"""Record Design toolkit changes without rewriting the homepage."""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'dialpad/design'
MANIFEST = ROOT / 'scripts/manifest.json'
CHANGELOG = ROOT / 'docs/whats-new.md'
HEADER = '''# Toolkit changes

Detected changes to shared and app-specific skills, agent profiles, and rules in the
[Design repo](https://github.com/dialpad/design). This is a file change log, not a
claim that a new feature has shipped. Use `skill-search` for the current inventory.

The [toolkit guide](/toolkit) and [prototyping guide](/prototyping) explain how to use them.

'''


def select_files(tree: dict) -> list[dict]:
    if tree.get('truncated') or not isinstance(tree.get('tree'), list):
        raise ValueError('Missing or truncated Design repository tree')
    patterns = (
        r'(?:apps/[^/]+/)?\.agents/skills/[^/]+/SKILL\.md',
        r'apps/[^/]+/\.agents/skills/[^/]+\.local\.md',
        r'(?:apps/[^/]+/)?\.agents/resources/rules/[^/]+\.md',
        r'(?:apps/[^/]+/)?\.claude/agents/.+\.md',
        r'(?:apps/[^/]+/)?\.codex/agents/.+\.toml',
    )
    files = [
        {'path': item['path'], 'sha': item['sha']}
        for item in tree['tree']
        if item.get('type') == 'blob'
        and any(re.fullmatch(pattern, item['path']) for pattern in patterns)
    ]
    if not files:
        raise ValueError('No Design toolkit files found')
    return sorted(files, key=lambda item: item['path'])


def changes(old: dict, new: list[dict]) -> dict[str, list[str]]:
    if old.get('repo') != REPO:
        raise ValueError('Manifest requires a fresh Design baseline')
    before = {item['path']: item['sha'] for item in old['files']}
    after = {item['path']: item['sha'] for item in new}
    return {
        'Added': sorted(after.keys() - before.keys()),
        'Modified': sorted(p for p in after.keys() & before.keys() if after[p] != before[p]),
        'Removed': sorted(before.keys() - after.keys()),
    }


def render_entry(diff: dict[str, list[str]], date: str) -> str:
    sections = [f'## {date}\n\n']
    for kind, paths in diff.items():
        if paths:
            sections.append(f'### {kind}\n\n')
            sections.extend(f'- `{path}`\n' for path in paths)
            sections.append('\n')
    return ''.join(sections) + '---\n\n'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    result = subprocess.run(
        ['gh', 'api', f'repos/{REPO}/git/trees/main?recursive=1'],
        check=True, capture_output=True, text=True,
    )
    files = select_files(json.loads(result.stdout))
    now = datetime.now(timezone.utc)
    changed = False
    if not args.baseline:
        diff = changes(json.loads(MANIFEST.read_text()), files)
        changed = any(diff.values())
        if changed:
            existing = CHANGELOG.read_text()
            if not existing.startswith(HEADER):
                raise ValueError('Toolkit change log header is missing')
            CHANGELOG.write_text(HEADER + render_entry(diff, now.strftime('%Y-%m-%d')) + existing[len(HEADER):])
    if args.baseline or changed:
        MANIFEST.write_text(json.dumps({'repo': REPO, 'generated': now.isoformat(), 'files': files}, indent=2) + '\n')
    if output := os.environ.get('GITHUB_OUTPUT'):
        with open(output, 'a') as stream:
            stream.write(f'changed={str(changed).lower()}\n')
    print('Toolkit changes recorded.' if changed else 'Toolkit baseline saved.' if args.baseline else 'No toolkit changes.')


if __name__ == '__main__':
    main()
