#!/usr/bin/env python3
"""Send a workflow failure notification through the shared Gmail notifier."""

from __future__ import annotations

import sys

from failure_notification import FailureNotificationError, notify_failure


def main() -> int:
    try:
        result = notify_failure()
    except FailureNotificationError as error:
        print(f"[notify] Failed to send email: {error}", file=sys.stderr)
        return 1

    if result.status == "skipped_missing_credentials":
        print("[notify] No Gmail credentials — skipping failure email")
    elif result.status == "duplicate_skipped":
        print(f"[notify] Failure email already sent for {result.local_date} — skipping duplicate")
    else:
        print("[notify] Failure email sent to amit.ayre@dialpad.com")
    return 0


if __name__ == "__main__":
    sys.exit(main())
