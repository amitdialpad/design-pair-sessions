#!/usr/bin/env python3
"""
Resend the most recent Beacon Brief to the current recipients list.

Reads the latest brief from docs/index.md (BEACON_BRIEF_START/END section),
extracts only the most recent issue (up to the first --- separator),
and sends it via Gmail using the same template as generate-brief.py.

Usage:
  python3 scripts/resend-brief.py
  Triggered by .github/workflows/resend-brief.yml (workflow_dispatch only).
"""

from __future__ import annotations

import json
import os
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
INDEX       = PROJECT_DIR / "docs" / "index.md"
RECIPIENTS  = PROJECT_DIR / "scripts" / "brief-recipients.json"

MARKER_START = "<!-- BEACON_BRIEF_START -->"
MARKER_END   = "<!-- BEACON_BRIEF_END -->"


# ── Extract latest brief ──────────────────────────────────────────────────────

def extract_latest_brief() -> str | None:
    content = INDEX.read_text()
    start = content.find(MARKER_START)
    end   = content.find(MARKER_END)
    if start == -1 or end == -1:
        print("[error] BEACON_BRIEF markers not found in index.md", file=sys.stderr)
        return None
    section = content[start + len(MARKER_START):end].strip()
    if not section:
        print("[error] BEACON_BRIEF section is empty", file=sys.stderr)
        return None
    # The latest issue is everything before the first \n---\n separator
    latest = section.split("\n---\n")[0].strip()
    return latest


# ── Recipients ────────────────────────────────────────────────────────────────

def load_recipients() -> list[str]:
    if RECIPIENTS.exists():
        data = json.loads(RECIPIENTS.read_text())
        return data.get("recipients", [])
    return []


# ── Email formatting (mirrors generate-brief.py) ─────────────────────────────

def _inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"`([^`]+)`",
        r'<code style="background:#f0ede8;padding:2px 6px;border-radius:3px;'
        r'font-family:Courier New,monospace;font-size:13px;color:#333333">\1</code>',
        text,
    )
    return text


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    parts = []
    in_list = False
    past_first_section = False
    tldr_open = False

    TLDR_P_STYLE = (
        "font-family:Georgia,serif;font-size:18px;line-height:1.8;"
        "color:#1a1a1a;margin:0 0 20px 0"
    )
    LABEL_STYLE = (
        "font-family:Arial,Helvetica,sans-serif;"
        "font-size:10px;font-weight:700;text-transform:uppercase;"
        "letter-spacing:0.12em;color:#999999;"
        "padding:28px 0 8px;margin:0;display:block"
    )
    P_STYLE = (
        "font-family:Georgia,serif;font-size:16px;line-height:1.7;"
        "color:#333333;margin:0 0 16px 0"
    )
    LI_STYLE = (
        "font-family:Georgia,serif;font-size:16px;line-height:1.7;"
        "color:#333333;margin:0 0 10px 0"
    )

    def close_list():
        nonlocal in_list
        if in_list:
            parts.append('</ul>')
            in_list = False

    def close_tldr():
        nonlocal tldr_open
        if tldr_open:
            parts.append('</div>')
            tldr_open = False

    for line in lines:
        if line.startswith("### "):
            close_list()
        elif line.startswith("#### "):
            close_list()
            if not past_first_section:
                close_tldr()
                past_first_section = True
                parts.append(
                    '<table width="100%" cellpadding="0" cellspacing="0" border="0"'
                    ' style="margin:32px 0 0"><tr>'
                    '<td style="border-top:1px solid #e8e4e0;font-size:0;line-height:0">'
                    '&nbsp;</td></tr></table>'
                )
            label = line[5:]
            parts.append(f'<p style="{LABEL_STYLE}">{label.upper()}</p>')
        elif line.startswith("- "):
            if not in_list:
                parts.append('<ul style="margin:0 0 16px 0;padding-left:20px">')
                in_list = True
            parts.append(f'<li style="{LI_STYLE}">{_inline(line[2:])}</li>')
        elif line.strip() in ("", "---"):
            close_list()
        else:
            close_list()
            if not past_first_section:
                if not tldr_open:
                    parts.append(
                        '<div style="border-left:3px solid #c4922a;'
                        'padding-left:20px;margin:24px 0 4px 0">'
                    )
                    tldr_open = True
                parts.append(f'<p style="{TLDR_P_STYLE}">{_inline(line)}</p>')
            else:
                parts.append(f'<p style="{P_STYLE}">{_inline(line)}</p>')

    close_list()
    close_tldr()
    return "\n".join(parts)


def extract_week_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("### "):
            return line[4:].strip()
    return "This week"


def build_html_email(issue: str) -> str:
    week_heading = extract_week_heading(issue)
    body_html    = markdown_to_html(issue)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body style="margin:0;padding:0;background-color:#ffffff">
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" style="padding:0">

      <table width="600" cellpadding="0" cellspacing="0" border="0"
             style="max-width:600px;width:100%">

        <!-- Header -->
        <tr>
          <td style="padding:48px 48px 8px">
            <p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;
                      font-size:10px;font-weight:700;letter-spacing:0.18em;
                      text-transform:uppercase;color:#c4922a">
              Beacon Brief
            </p>
            <p style="margin:0;font-family:Georgia,serif;font-size:36px;
                      font-weight:700;color:#1a1a1a;line-height:1.15;
                      letter-spacing:-0.01em">
              {week_heading}
            </p>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:24px 48px 0">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr><td style="border-top:1px solid #e8e4e0;font-size:0;line-height:0">&nbsp;</td></tr>
            </table>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:4px 48px 48px">
            {body_html}
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:0 48px 48px">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr><td style="border-top:1px solid #e8e4e0;font-size:0;line-height:0;padding-bottom:20px">&nbsp;</td></tr>
            </table>
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;
                      font-size:12px;color:#999999;line-height:1.6">
              Beacon Brief &mdash; weekly digest for Dialpad designers.&nbsp;
              <a href="https://amitdialpad.github.io/design-pair-sessions/"
                 style="color:#c4922a;text-decoration:none">
                View on the site
              </a>
            </p>
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
</body>
</html>"""


def send_email(subject: str, issue: str, recipients: list[str]) -> bool:
    gmail_user = os.environ.get("GMAIL_USER", "").strip()
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    if not gmail_user or not gmail_pass:
        print("[error] GMAIL_USER or GMAIL_APP_PASSWORD not set", file=sys.stderr)
        return False
    if not recipients:
        print("[error] No recipients found", file=sys.stderr)
        return False

    html_full = build_html_email(issue)

    msg            = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Beacon Brief <{gmail_user}>"
    msg["To"]      = gmail_user
    msg.attach(MIMEText(issue, "plain"))
    msg.attach(MIMEText(html_full, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, recipients, msg.as_string())
        print(f"  Resent to {len(recipients)} recipient(s) (BCC).")
        return True
    except Exception as e:
        print(f"[error] Email send failed: {e}", file=sys.stderr)
        return False


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    issue = extract_latest_brief()
    if not issue:
        sys.exit(1)

    week_heading = extract_week_heading(issue)
    print(f"Resending: {week_heading}")

    recipients = load_recipients()
    print(f"  Recipients: {len(recipients)}")

    subject = f"Beacon Brief: {week_heading}"
    success = send_email(subject, issue, recipients)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
