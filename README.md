# LinkedIn Job Outreach Assistant

A Python CLI that turns LinkedIn hiring posts you manually collect into personalized job-outreach emails.

## V1 workflow

1. Copy LinkedIn post text into `data/posts.txt`.
2. Put your resume at `data/resume.pdf`.
3. Run the scanner.
4. Review extracted recruiter/company/role/email data and match scores.
5. Generate/review drafts.
6. Approve sending interactively.
7. Emails are sent with your resume attached.
8. Outreach is tracked in SQLite to avoid accidental duplicate sends.

This version intentionally does not automate LinkedIn login, search-bar interaction, scraping, CAPTCHA handling, or bulk extraction from LinkedIn pages.

## Setup

Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
cp .env.example .env
```

Edit `.env` with your Gmail address and Gmail App Password.

Put your resume here:

```text
data/resume.pdf
```

Put copied LinkedIn posts here:

```text
data/posts.txt
```

Separate posts with:

```text
================ POST ================
```

## Commands

```bash
python -m outreach scan
python -m outreach list
python -m outreach draft
python -m outreach send 1
python -m outreach approve
```

## Example post

```text
Hiring AWS Cloud Engineers!

We are looking for AWS / Cloud Engineers with 0-2 years of experience.
Interested candidates can contact Rahul Sharma at recruiter@example.com.

Location: Noida
Company: ABC Technologies
```

The matcher scores target roles, relevant keywords, fresher/0-2 experience signals, and senior-level negative signals.

## Gmail

Use a Gmail App Password rather than your normal Gmail password.

The tool sends one email at a time after explicit approval.
# EzApply
