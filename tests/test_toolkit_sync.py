import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('sync_toolkit', Path(__file__).resolve().parents[1] / 'scripts/sync-toolkit.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class ToolkitSyncTests(unittest.TestCase):
    def test_detects_shared_and_app_tools_without_adapters_or_evals(self):
        paths = ['.agents/skills/prototype-builder/SKILL.md', 'apps/studio/.agents/skills/prototype-create/SKILL.md', 'apps/beacon/.agents/skills/pr-prep.local.md', '.codex/agents/skeptic-reviewer.toml', '.claude/agents/skeptic-reviewer.md', '.agents/resources/rules/vue.md', '.claude/skills/prototype-builder/SKILL.md', '.agents/skills/pr-prep/evals/prompts.csv']
        tree = {'tree': [{'path': p, 'sha': 'a', 'type': 'blob'} for p in paths]}
        self.assertEqual({f['path'] for f in sync.select_files(tree)}, set(paths[:6]))

    def test_missing_truncated_or_empty_inventory_fails_closed(self):
        for tree in ({}, {'tree': [], 'truncated': True}, {'tree': []}):
            with self.assertRaises(ValueError):
                sync.select_files(tree)

    def test_detects_content_changes_and_requires_explicit_migration(self):
        old = {'repo': sync.REPO, 'files': [{'path': 'keep', 'sha': 'a'}, {'path': 'remove', 'sha': 'a'}]}
        new = [{'path': 'keep', 'sha': 'b'}, {'path': 'add', 'sha': 'a'}]
        self.assertEqual(sync.changes(old, new), {'Added': ['add'], 'Modified': ['keep'], 'Removed': ['remove']})
        with self.assertRaises(ValueError):
            sync.changes({**old, 'repo': 'dialpad/beacon-app'}, new)


if __name__ == '__main__':
    unittest.main()
