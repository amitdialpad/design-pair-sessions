#!/usr/bin/env python3
"""
Send a failure notification email when a GitHub Actions workflow fails.

Usage (in a workflow step):
  python3 scripts/notify-failure.py

Required env vars (set via GitHub Actions secrets):
  GMAIL_USER          — sender Gmail address
  GMAIL_APP_PASSWORD  — Gmail App Password (not account password)
  WORKFLOW_NAME       — ${{ github.workflow }}
  RUN_URL             — ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
"""

import os
import smtplib
import sys
from email.mime.text import MIMEText

RECIPIENT = "amit.ayre@dialpad.com"

user = os.environ.get("GMAIL_USER", "").strip()
password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
workflow = os.environ.get("WORKFLOW_NAME", "Unknown workflow")
run_url = os.environ.get("RUN_URL", "")
subject_prefix = os.environ.get("FAILURE_SUBJECT_PREFIX", "Beacon sync failed")
description = os.environ.get(
    "FAILURE_DESCRIPTION",
    "This means the site or Beacon app may not have received today's update.",
)
common_fixes = os.environ.get(
    "FAILURE_COMMON_FIXES",
    "  - BEACON_PAT expired → rotate at github.com/settings/tokens and update the secret\n"
    "  - Anthropic API error → check usage at console.anthropic.com\n"
    "  - GitHub API rate limit → re-run the workflow in a few minutes",
)

if not user or not password:
    print("[notify] No Gmail credentials — skipping failure email")
    sys.exit(0)

subject = f"{subject_prefix}: {workflow}"
body = (
    f"The '{workflow}' workflow failed on amitdialpad/design-pair-sessions.\n\n"
    f"{description}\n\n"
    f"View the failed run:\n{run_url}\n\n"
    f"Common fixes:\n"
    f"{common_fixes}\n"
)

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = user
msg["To"] = RECIPIENT

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user, password)
        server.send_message(msg)
    print(f"[notify] Failure email sent to {RECIPIENT}")
except Exception as e:
    print(f"[notify] Failed to send email: {e}", file=sys.stderr)
    sys.exit(1)
