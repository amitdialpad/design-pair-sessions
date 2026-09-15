#!/usr/bin/env python3
"""
Generate a Beacon Brief newsletter issue and prepend it to docs/index.md.

Reads:
  - Beacon commits and pull requests merged to dialpad/design during the prior week
  - scripts/weekly-notes.md (if present — updated Wednesday by Amit)

Builds the newsletter directly from those source records, then:
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
from urllib.request import Request, urlopen

from beacon_changes import GitHubError, clean_source_markdown, enrich_commit, fetch_commits

PROJECT_DIR    = Path(__file__).parent.parent
INDEX          = PROJECT_DIR / "docs" / "index.md"
WEEKLY_NOTES   = PROJECT_DIR / "scripts" / "weekly-notes.md"
ARCHIVE_SCRIPT = PROJECT_DIR / "scripts" / "archive-briefs.py"
RECIPIENTS     = PROJECT_DIR / "scripts" / "brief-recipients.json"
DM_RECIPIENTS  = PROJECT_DIR / "scripts" / "brief-dm-recipients.json"

MARKER_START = "<!-- BEACON_BRIEF_START -->"
MARKER_END = "<!-- BEACON_BRIEF_END -->"


# ── Date helpers ──────────────────────────────────────────────────────────────

def get_week_context(now: datetime | None = None) -> tuple[datetime, datetime, str]:
    """Return the UTC boundaries and label for the prior Monday-Sunday week.

    The brief runs on Monday and recaps the previous week.
    On Monday Apr 13, returns Apr 6 through Apr 12.
    """
    current = now or datetime.now(timezone.utc)
    sunday_date = (current - timedelta(days=current.weekday() + 1)).date()
    monday_date = sunday_date - timedelta(days=6)
    monday = datetime.combine(monday_date, datetime.min.time(), tzinfo=timezone.utc)
    sunday = datetime.combine(sunday_date, datetime.max.time(), tzinfo=timezone.utc)

    if monday.year != sunday.year:
        label = f"{monday.strftime('%-d %b %Y')}–{sunday.strftime('%-d %b %Y')}"
    elif monday.month != sunday.month:
        label = f"{monday.strftime('%-d %b')}–{sunday.strftime('%-d %b %Y')}"
    else:
        label = f"{monday.day}–{sunday.strftime('%-d %b %Y')}"
    return monday, sunday, label


# ── Source material ───────────────────────────────────────────────────────────

def get_beacon_changes(monday: datetime, sunday: datetime) -> list[dict]:
    """Fetch exact prior-week monorepo source material or stop the send."""
    commits = fetch_commits(since=monday, until=sunday)
    return [enrich_commit(commit) for commit in commits]


def get_weekly_notes() -> str:
    if WEEKLY_NOTES.exists():
        text = WEEKLY_NOTES.read_text().strip()
        return text if text else ""
    return ""


# ── Source-grounded writing ──────────────────────────────────────────────────

def _display_title(change: dict) -> str:
    title = re.sub(r"^(feat|fix|bug|refactor|docs|chore)(\([^)]*\))?:\s*", "", change["title"], flags=re.I)
    title = re.sub(r"^(?:[A-Z]+-\d+|NO-JIRA)\s+", "", title, flags=re.I)
    title = re.sub(r"\s*\(#\d+\)\s*$", "", title).strip()
    title = title[0].upper() + title[1:] if title else "Beacon change"
    title = re.sub(r"\bAi\b", "AI", title)
    return re.sub(r"(?i)\bAI receptionist\b", "AI Receptionist", title)


def _section(body: str, names: str) -> str:
    clean = clean_source_markdown(body, limit=6000)
    match = re.search(rf"(?ims)^##\s+[^\n]*?(?:{names})[^\n]*\n+(.*?)(?=^##\s+|\Z)", clean)
    return match.group(1).strip() if match else ""


def _summary(change: dict) -> str:
    source = _section(change.get("body", ""), "summary|description")
    if not source:
        source = clean_source_markdown(change.get("body", ""), limit=1800)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", source) if p.strip() and not p.startswith("-")]
    summary = " ".join(paragraphs[:2])
    summary = re.sub(r"`([^`]+)`", r"\1", summary)
    summary = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", summary)
    summary = re.sub(r"\s+", " ", summary).strip()
    return summary[:897].rstrip() + "..." if len(summary) > 900 else summary


def _review_step(changes: list[dict]) -> str:
    for change in changes:
        review = _section(change.get("body", ""), "for reviewers|review")
        source = review or clean_source_markdown(change.get("body", ""), limit=6000)
        match = re.search(r"(?m)^- \[[ xX]\]\s+(.+)$", source)
        if match:
            return match.group(1).strip()
    return "Open the changed Beacon area and compare it with the linked merged PR before using it in a prototype."


def _next_steps(changes: list[dict]) -> str:
    steps = []
    for change in changes:
        section = _section(change.get("body", ""), "next steps?")
        plain = re.sub(r"\s+", " ", section).strip()
        if plain and not re.match(r"(?i)^none\b", plain):
            steps.append(plain)
    return " ".join(steps) if steps else "No follow-on work was explicitly announced in this week's merged Beacon changes."


def generate_brief(week_range: str, changes: list[dict], notes: str) -> str:
    if changes:
        titles = [_display_title(change) for change in changes]
        if len(changes) == 1:
            opening = f"{titles[0]} was the only change merged into Beacon this week. {_summary(changes[0])}"
        else:
            opening = (
                f"{len(changes)} changes merged into Beacon this week: "
                + "; ".join(title.lower() for title in titles)
                + ". The details below come directly from the merged monorepo PRs."
            )
        change_lines = []
        for change, title in zip(changes, titles):
            reference = f"dialpad/design#{change['pr_number']}" if change.get("pr_number") else change["sha"][:8]
            change_lines.append(f"- **[{title}]({change['link']})** ({reference}). {_summary(change)}")
        actual_changes = "\n".join(change_lines)
        bigger_shift = (
            f"This was a focused week with {len(changes)} merged Beacon change"
            f"{'s' if len(changes) != 1 else ''}. No broader pattern is claimed beyond those source records."
        )
        messy = "No unresolved issue was explicitly documented in this week's merged Beacon changes."
        remember = f"The week's Beacon record is {', '.join(title.lower() for title in titles)}."
    else:
        opening = "No changes touching `apps/beacon` merged into the `dialpad/design` monorepo this week."
        actual_changes = "No Beacon changes were merged during this Monday-to-Sunday window."
        bigger_shift = "There is no change pattern to infer from an empty merge record."
        messy = "No new unresolved issue was recorded because no Beacon change merged this week."
        remember = "No Beacon change merged this week."

    if notes:
        opening += f" Amit's notes add: {re.sub(r'\s+', ' ', notes).strip()}"

    quick_notes = [
        "Source: merged commits and pull requests touching `apps/beacon` in `dialpad/design`.",
        "Window: Monday 00:00 through Sunday 23:59 UTC.",
        "A migration is reported as a migration, not as a new product release.",
    ]
    return f"""### Week of {week_range}

{opening}

#### What actually changed

{actual_changes}

#### The bigger shift

{bigger_shift}

#### Where things are still messy

{messy}

#### What's coming next

{_next_steps(changes)}

#### Try this

{_review_step(changes)}

#### Quick notes

{chr(10).join(f'- {note}' for note in quick_notes)}

#### One thing to remember

{remember}"""


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
    text = re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", r'<a href="\2" style="color:#8a651d">\1</a>', text)
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
    monday, sunday, week_range = get_week_context()
    print(f"Generating Beacon Brief for week of {week_range}...")

    # Guard: skip if a brief for this week already exists (line-exact match)
    existing_content = INDEX.read_text()
    if f"\n### Week of {week_range}\n" in existing_content:
        print(f"Brief for week of {week_range} already exists — skipping.")
        sys.exit(1)

    try:
        changes = get_beacon_changes(monday, sunday)
    except GitHubError as error:
        print(f"[error] Could not read dialpad/design Beacon changes: {error}", file=sys.stderr)
        sys.exit(2)
    notes = get_weekly_notes()

    print(f"  Weekly notes: {'found' if notes else 'not found, generating from monorepo changes'}")

    issue = generate_brief(week_range, changes, notes)
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
    subject = f"Beacon Brief: week of {week_range}"
    send_email(subject, issue, issue, recipients)

    # Send Dialpad DMs
    print("  Sending Dialpad DMs...")
    dm_recipients = load_dm_recipients()
    send_dialpad_dms(week_range, dm_recipients)

    print(f"Done. Week of {week_range} added.")
    sys.exit(0)


if __name__ == "__main__":
    main()
