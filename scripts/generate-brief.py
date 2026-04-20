#!/usr/bin/env python3
"""
Generate a Beacon Brief newsletter issue and prepend it to docs/index.md.

Reads:
  - Recent git log (past 7 days)
  - BEACON_RELEASES section from docs/index.md
  - scripts/weekly-notes.md (if present — updated Wednesday by Amit)

Uses Claude Haiku to write the newsletter, then:
  1. Prepends to the BEACON_BRIEF_START/END section in docs/index.md
  2. Runs archive-briefs.py to rebalance visible/archived issues

Exit codes:
  0 = brief generated and written
  1 = skipped (e.g. already ran this week)
  2 = error
"""

from __future__ import annotations

import json
import os
import re
import smtplib
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

PROJECT_DIR    = Path(__file__).parent.parent
INDEX          = PROJECT_DIR / "docs" / "index.md"
WEEKLY_NOTES   = PROJECT_DIR / "scripts" / "weekly-notes.md"
ARCHIVE_SCRIPT = PROJECT_DIR / "scripts" / "archive-briefs.py"
RECIPIENTS     = PROJECT_DIR / "scripts" / "brief-recipients.json"
DM_RECIPIENTS  = PROJECT_DIR / "scripts" / "brief-dm-recipients.json"

MARKER_START    = "<!-- BEACON_BRIEF_START -->"
MARKER_END      = "<!-- BEACON_BRIEF_END -->"
RELEASES_START  = "<!-- BEACON_RELEASES_START -->"
RELEASES_END    = "<!-- BEACON_RELEASES_END -->"


# ── Date helpers ──────────────────────────────────────────────────────────────

def get_week_range() -> tuple[str, str, str]:
    """Return (mon_str, sun_str, label) for the week that just ended (Mon–Sun).

    The brief runs on Monday and recaps the previous week.
    On Monday Apr 13 → returns Mon Apr 6 – Sun Apr 12.
    """
    today = datetime.now(timezone.utc)
    # Yesterday is the Sunday that closed the previous week
    sunday = today - timedelta(days=today.weekday() + 1)
    monday = sunday - timedelta(days=6)
    mon_str = monday.strftime("%-d %b %Y")
    sun_str = sunday.strftime("%-d %b %Y")
    # Short label e.g. "6–12 Apr 2026"
    label = f"{monday.day}–{sun_str}"
    return mon_str, sun_str, label


# ── Source material ───────────────────────────────────────────────────────────

def get_git_log() -> str:
    result = subprocess.run(
        ["git", "-C", str(PROJECT_DIR), "log", "--oneline", "--since=7 days ago"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() or "No commits this week."


def get_releases_section() -> str:
    content = INDEX.read_text()
    start = content.find(RELEASES_START)
    end   = content.find(RELEASES_END)
    if start == -1 or end == -1:
        return ""
    return content[start + len(RELEASES_START):end].strip()


def get_weekly_notes() -> str:
    if WEEKLY_NOTES.exists():
        text = WEEKLY_NOTES.read_text().strip()
        return text if text else ""
    return ""


# ── Claude API ────────────────────────────────────────────────────────────────

def _claude(prompt: str, max_tokens: int = 900) -> str | None:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("[error] ANTHROPIC_API_KEY not set", file=sys.stderr)
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


BRIEF_PROMPT = """\
You are writing the Beacon Brief — a weekly newsletter for product designers at Dialpad.
Beacon is a prototyping tool built by their tech lead Josh. Designers use it with Claude Code to build and test UI.

Write in plain, human English. Like a colleague catching up a teammate after a week away.
Short sentences. No em dashes. No corporate language. No filler phrases like "it is worth noting".
Be specific. Name the command or feature. Explain what it actually does.

Week: {week_range}

What shipped in Beacon this week:
{releases}
{notes_section}
Recent repo commits (for context on what changed in the docs/site):
{git_log}

Write the newsletter in this exact format. If a section has nothing real to say, write one honest sentence. Do not pad.

### Week of {week_range}

[Write an opening summary here — no heading, just prose. This is the most important part of the brief. Most designers will read only this and nothing else, so it needs to stand on its own. Cover what actually changed this week and what it means for design work. Be specific — name the features, explain what they do. Write as much as the week demands: a quiet week gets a short paragraph, a big week earns more. No length limit. Plain language, no jargon, no hedging. Someone who reads only this section should leave knowing whether this week was significant, what shipped, and whether any of it affects their current work.]

#### What actually changed
[Specific commands, features, or data model changes that shipped. Name them. Explain what they do or unlock.]

#### The bigger shift
[A pattern across what shipped, or a change in how Beacon works. Write as an observation. No attribution to any person or meeting.]

#### Where things are still messy
[What is in progress, unresolved, or known to be incomplete right now.]

#### What's coming next
[What is likely next based on the material. Write as an observation about where things are heading.]

#### Try this
[One concrete thing to try in Beacon this week. Be specific. Make it feel like a tip from someone who already did it.]

#### Quick notes
- [Short bullet]
- [Short bullet]
- [Short bullet]

#### One thing to remember
[One sentence. The most important thing to carry into the week.]

Return only the newsletter text, starting with ### Week of..."""


def generate_brief(week_range: str, releases: str, git_log: str, notes: str) -> str | None:
    notes_section = f"\nAmit's notes from this week:\n{notes}\n" if notes else ""
    prompt = BRIEF_PROMPT.format(
        week_range=week_range,
        releases=releases or "No new Beacon releases this week.",
        git_log=git_log,
        notes_section=notes_section,
    )
    return _claude(prompt)


# ── File update ───────────────────────────────────────────────────────────────

def prepend_to_brief(content: str, issue: str) -> str:
    start = content.find(MARKER_START)
    end   = content.find(MARKER_END)
    if start == -1 or end == -1:
        print("[error] BEACON_BRIEF markers not found in index.md", file=sys.stderr)
        return content
    existing = content[start + len(MARKER_START):end].strip()
    new_inner = issue + ("\n\n---\n\n" + existing if existing else "")
    return (
        content[:start]
        + MARKER_START + "\n\n"
        + new_inner + "\n\n"
        + MARKER_END
        + content[end + len(MARKER_END):]
    )


# ── Email ─────────────────────────────────────────────────────────────────────

def load_recipients() -> list[str]:
    if RECIPIENTS.exists():
        data = json.loads(RECIPIENTS.read_text())
        return data.get("recipients", [])
    return []


def _inline(text: str) -> str:
    """Convert inline markdown (bold, code) to HTML."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"`([^`]+)`",
        r'<code style="background:#f0ede8;padding:2px 6px;border-radius:3px;'
        r'font-family:Courier New,monospace;font-size:13px;color:#333333">\1</code>',
        text,
    )
    return text


def markdown_to_html(text: str) -> str:
    """
    Convert newsletter markdown to email-safe HTML. All styles inline (Gmail-safe).
    Skips the ### heading line — extracted separately for the header.
    Paragraphs before the first #### heading are treated as the TL;DR opener
    and rendered with a left accent border.
    """
    lines = text.splitlines()
    parts = []
    in_list = False
    past_first_section = False  # flips on first #### heading
    tldr_open = False            # tracks whether the left-border div is open

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
            # Week heading handled by the outer template — skip
        elif line.startswith("#### "):
            close_list()
            if not past_first_section:
                close_tldr()
                past_first_section = True
                # Thin rule separating the TL;DR from the detail sections
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
    """Pull the ### Week of... line out of the issue text."""
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


def send_email(subject: str, plain_text: str, issue: str, recipients: list[str]) -> bool:
    gmail_user = os.environ.get("GMAIL_USER", "").strip()
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    if not gmail_user or not gmail_pass:
        print("[warn] GMAIL_USER or GMAIL_APP_PASSWORD not set — skipping email", file=sys.stderr)
        return False
    if not recipients:
        print("[warn] No recipients found — skipping email", file=sys.stderr)
        return False

    html_full = build_html_email(issue)

    msg             = MIMEMultipart("alternative")
    msg["Subject"]  = subject
    msg["From"]     = f"Beacon Brief <{gmail_user}>"
    msg["To"]       = gmail_user
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_full, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, recipients, msg.as_string())
        print(f"  Email sent to {len(recipients)} recipient(s) (BCC).")
        return True
    except Exception as e:
        print(f"[warn] Email send failed: {e}", file=sys.stderr)
        return False


# ── Dialpad DM ───────────────────────────────────────────────────────────────

def load_dm_recipients() -> list[str]:
    if DM_RECIPIENTS.exists():
        data = json.loads(DM_RECIPIENTS.read_text())
        return data.get("contact_keys", [])
    return []


def send_dialpad_dms(week_range: str, contact_keys: list[str]) -> bool:
    """Send a short DM notification to each contact_key via the Dialpad internal API.

    Auth: DIALPAD_BEARER_TOKEN env var (session token from browser).
    If the token is expired (HTTP 401), logs a warning and skips silently.
    """
    token = os.environ.get("DIALPAD_BEARER_TOKEN", "").strip()
    if not token:
        print("[warn] DIALPAD_BEARER_TOKEN not set — skipping DM", file=sys.stderr)
        return False
    if not contact_keys:
        print("[warn] No DM recipients configured — skipping", file=sys.stderr)
        return False

    site_url = "https://amitdialpad.github.io/design-pair-sessions/"
    text = f"Beacon Brief: week of {week_range} is out. {site_url}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Api-Version": "1",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
    }
    sent, failed = 0, 0
    for contact_key in contact_keys:
        payload = json.dumps({"contact_key": contact_key, "text": text}).encode()
        req = Request(
            "https://dialpad.com/api/feed/message/",
            data=payload,
            headers=headers,
        )
        try:
            with urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    sent += 1
                else:
                    print(f"[warn] DM to {contact_key}: HTTP {resp.status}", file=sys.stderr)
                    failed += 1
        except Exception as e:
            msg = str(e)
            if "401" in msg:
                print("[warn] DIALPAD_BEARER_TOKEN expired — update the GitHub secret", file=sys.stderr)
            else:
                print(f"[warn] DM send failed for {contact_key}: {e}", file=sys.stderr)
            failed += 1

    if sent:
        print(f"  Dialpad DM sent to {sent} recipient(s).")
    return sent > 0


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    _, _, week_range = get_week_range()
    print(f"Generating Beacon Brief for week of {week_range}...")

    # Guard: skip if a brief for this week already exists (line-exact match)
    existing_content = INDEX.read_text()
    if f"\n### Week of {week_range}\n" in existing_content:
        print(f"Brief for week of {week_range} already exists — skipping.")
        sys.exit(1)

    releases = get_releases_section()
    git_log  = get_git_log()
    notes    = get_weekly_notes()

    print(f"  Weekly notes: {'found' if notes else 'not found, generating from releases + commits'}")

    issue = generate_brief(week_range, releases, git_log, notes)
    if not issue:
        sys.exit(2)

    print("  Writing to docs/index.md...")
    content     = INDEX.read_text()
    new_content = prepend_to_brief(content, issue)
    INDEX.write_text(new_content)

    print("  Rebalancing archive...")
    result = subprocess.run(["python3", str(ARCHIVE_SCRIPT)], capture_output=True, text=True)
    print(f"  {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"[warn] archive-briefs: {result.stderr.strip()}", file=sys.stderr)

    # Send email
    print("  Sending email...")
    recipients = load_recipients()
    _, _, week_label = get_week_range()
    subject = f"Beacon Brief: week of {week_label}"
    send_email(subject, issue, issue, recipients)

    # Send Dialpad DMs
    print("  Sending Dialpad DMs...")
    dm_recipients = load_dm_recipients()
    send_dialpad_dms(week_label, dm_recipients)

    print(f"Done. Week of {week_range} added.")
    sys.exit(0)


if __name__ == "__main__":
    main()
