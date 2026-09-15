from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import beacon_changes

brief_spec = importlib.util.spec_from_file_location("generate_brief", ROOT / "scripts" / "generate-brief.py")
assert brief_spec and brief_spec.loader
generate_brief = importlib.util.module_from_spec(brief_spec)
brief_spec.loader.exec_module(generate_brief)

archive_spec = importlib.util.spec_from_file_location("archive_briefs", ROOT / "scripts" / "archive-briefs.py")
assert archive_spec and archive_spec.loader
archive_briefs = importlib.util.module_from_spec(archive_spec)
archive_spec.loader.exec_module(archive_briefs)


class BeaconChangesTests(unittest.TestCase):
    def test_extracts_squash_merge_pull_request_number(self):
        commit = {"commit": {"message": "feat: add a thing (#123)"}}
        self.assertEqual(beacon_changes.pull_request_number(commit), 123)

    def test_returns_only_commits_newer_than_saved_marker(self):
        commits = [{"sha": "newest"}, {"sha": "middle"}, {"sha": "saved"}, {"sha": "old"}]
        self.assertEqual(
            beacon_changes.new_commits_since(commits, "saved"),
            [{"sha": "newest"}, {"sha": "middle"}],
        )

    def test_missing_saved_marker_fails_closed(self):
        with self.assertRaises(beacon_changes.GitHubError):
            beacon_changes.new_commits_since([{"sha": "newest"}], "missing")

    def test_docs_only_change_is_not_designer_facing(self):
        change = {
            "title": "docs: align Beacon test guidance (#116)",
            "files": ["apps/beacon/docs/development/testing.md"],
        }
        self.assertFalse(beacon_changes.is_designer_facing(change))

    def test_feature_source_change_is_designer_facing(self):
        change = {
            "title": "feat: add cross-tab read state (#114)",
            "files": ["apps/beacon/src/services/readAttentionSync.ts"],
        }
        self.assertTrue(beacon_changes.is_designer_facing(change))


class BeaconBriefTests(unittest.TestCase):
    def test_week_label_handles_month_boundary(self):
        monday, sunday, label = generate_brief.get_week_context(
            datetime(2026, 9, 7, 4, 30, tzinfo=timezone.utc)
        )
        self.assertEqual(label, "31 Aug–6 Sep 2026")
        self.assertEqual(monday.isoformat(), "2026-08-31T00:00:00+00:00")
        self.assertEqual(sunday.isoformat(), "2026-09-06T23:59:59.999999+00:00")

    def test_archive_parser_handles_month_boundary(self):
        parsed = archive_briefs.parse_date("### Week of 31 Aug–6 Sep 2026")
        self.assertEqual(parsed, datetime(2026, 9, 6))

    def test_brief_uses_only_supplied_change_and_source_link(self):
        change = {
            "sha": "abc123",
            "title": "feat: DDT-2234 converge read attention across tabs (#114)",
            "body": """## Summary

Unread state stayed stale in another tab. This synchronizes it for the same user and company.

## For Reviewers

- [ ] Open two tabs and mark a conversation unread.
""",
            "pr_number": 114,
            "link": "https://github.com/dialpad/design/pull/114",
        }
        issue = generate_brief.generate_brief("7–13 Sep 2026", [change], "")
        self.assertIn("Converge read attention across tabs was the only change", issue)
        self.assertIn("https://github.com/dialpad/design/pull/114", issue)
        self.assertIn("Open two tabs and mark a conversation unread.", issue)
        self.assertNotIn("Josh", issue)
        self.assertNotIn("probably", issue)

    def test_recipient_validation_rejects_duplicates_and_malformed_addresses(self):
        with self.assertRaises(ValueError):
            generate_brief.validate_recipients(["person@example.com", "person@example.com"])
        with self.assertRaises(ValueError):
            generate_brief.validate_recipients(["not-an-email"])

    def test_smtp_refusal_is_a_send_failure(self):
        smtp = MagicMock()
        smtp.__enter__.return_value.sendmail.return_value = {"refused@example.com": (550, b"rejected")}
        with patch.dict(
            generate_brief.os.environ,
            {"GMAIL_USER": "sender@example.com", "GMAIL_APP_PASSWORD": "secret"},
            clear=False,
        ), patch.object(generate_brief.smtplib, "SMTP", return_value=smtp):
            sent = generate_brief.send_email(
                "Beacon Brief: week of 14–20 Sep 2026",
                "plain",
                "### Week of 14–20 Sep 2026\n\nBody",
                ["refused@example.com"],
            )
        self.assertFalse(sent)


if __name__ == "__main__":
    unittest.main()
