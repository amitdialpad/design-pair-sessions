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

if not user or not password:
    print("[notify] No Gmail credentials — skipping failure email")
    sys.exit(0)

subject = f"Beacon sync failed: {workflow}"
body = (
    f"The '{workflow}' workflow failed on amitdialpad/design-pair-sessions.\n\n"
    f"This means the site or Beacon app may not have received today's update.\n\n"
    f"View the failed run:\n{run_url}\n\n"
    f"Common fixes:\n"
    f"  - BEACON_PAT expired → rotate at github.com/settings/tokens and update the secret\n"
    f"  - Anthropic API error → check usage at console.anthropic.com\n"
    f"  - GitHub API rate limit → re-run the workflow in a few minutes\n"
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
