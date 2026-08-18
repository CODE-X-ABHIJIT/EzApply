````markdown
# 🚀 EzApply

**EzApply** is a Python-based job outreach automation tool that helps automate the process of finding suitable LinkedIn job posts, extracting recruiter email addresses, matching jobs against target roles, and sending personalized cold emails with a resume.

> **Current Status:** LinkedIn job searching is currently manual. LinkedIn post URLs are added to `posts.txt`. Automatic LinkedIn search is planned for a future version.

---

## ✨ Features

- 🔗 Read LinkedIn job post URLs from `posts.txt`
- 🌐 Open LinkedIn posts using Playwright and `LINKEDIN_STATE`
- 📝 Extract LinkedIn post content automatically
- 📧 Detect recruiter email addresses from posts
- 🎯 Match jobs against configured Cloud/DevOps roles
- 📊 Calculate a job match score
- ✉️ Generate personalized cold emails
- 📎 Attach resume automatically
- 📤 Send multiple applications in one run
- 🗃️ Store jobs and email status in SQLite
- 🔐 Use GitHub Secrets for credentials
- ⚙️ Run automatically using GitHub Actions
- 🖥️ Support both local and CI/CD execution

---

## 🏗️ Project Structure

```text
EzApply/
│
├── outreach/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── browser.py
│   ├── config.py
│   ├── database.py
│   ├── extractor.py
│   ├── matcher.py
│   ├── mailer.py
│   └── templates.py
│
├── data/
│   ├── posts.txt
│   ├── Abhijit_Sahu_CV.pdf
│   ├── outreach.db
│   └── linkedin_state.json
│
├── .github/
│   └── workflows/
│       └── outreach.yml
│
├── auto_outreach.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Workflow

```text
                    LinkedIn Job Posts
                           │
                           ▼
                       posts.txt
                           │
                           ▼
                       Playwright
                           │
                           ▼
                  Extract Post Content
                           │
                           ▼
                Extract Email + Job Details
                           │
                           ▼
                      Job Matcher
                           │
                           ▼
                       Match Score
                           │
                           ▼
                    Email Generator
                           │
                           ▼
                     SQLite Database
                           │
                           ▼
                       Gmail SMTP
                           │
                           ▼
                   Recruiter + Resume
```

---

## 📌 Current Job Collection Method

Currently, LinkedIn job searching is performed **manually**.

Add LinkedIn post URLs to:

```text
data/posts.txt
```

Example:

```text
https://www.linkedin.com/posts/example-devops-hiring-123456
https://www.linkedin.com/posts/example-aws-engineer-789012
```

EzApply reads these URLs and opens the posts internally using Playwright.

### Automatic LinkedIn Search

Automatic searching for keywords such as:

```text
AWS Cloud Engineer
Cloud Engineer
DevOps Engineer
Kubernetes Engineer
SRE
```

is **planned but not implemented yet**.

---

## 🔐 LinkedIn Authentication

EzApply uses Playwright's authentication state instead of storing LinkedIn username/password credentials.

The authentication state is represented by:

```text
LINKEDIN_STATE
```

### Local

The state is stored as:

```text
data/linkedin_state.json
```

### GitHub Actions

The authentication state is stored securely as a GitHub Secret:

```text
LINKEDIN_STATE
```

The GitHub Actions workflow restores this state before running EzApply.

---

## 🎯 Target Roles

The current matching configuration includes:

```text
AWS Cloud Engineer
Cloud Engineer
AWS Engineer
DevOps Engineer
DevOps
Kubernetes Engineer
Site Reliability Engineer
SRE
```

### Experience Keywords

```text
fresher
0-1
0-2
1-2
entry level
```

The matcher generates a percentage-based score for every detected job.

Example:

```text
#1 | 81% | recruiter@example.com | DevOps Engineer
#2 | 75% | recruiter@example.com | DevOps Engineer
```

---

## 📧 Email Automation

EzApply generates a personalized cold email using the extracted job information.

Example:

```text
Hi Hiring Manager,

I came across your LinkedIn post regarding the DevOps Engineer opportunity.

I am interested in the role and have hands-on experience working with
AWS infrastructure, Kubernetes, Docker, Linux and related technologies.

My resume is attached for your consideration.

Thanks and regards,
Abhijit Sahu
```

The resume is automatically attached from:

```text
data/Abhijit_Sahu_CV.pdf
```

---

## 🗃️ SQLite Database

EzApply stores job information and email status in:

```text
data/outreach.db
```

The database is used to:

- Track discovered jobs
- Store recruiter email addresses
- Store match scores
- Track email status
- Prevent duplicate outreach

Typical information includes:

```text
Job ID
Recruiter Email
Role
Company
Location
Match Score
LinkedIn URL
Email Status
```

---

## ⚙️ Commands

### Login

Authenticate LinkedIn locally:

```bash
python -m outreach login
```

---

### Scan

Read URLs from `posts.txt` and extract job information:

```bash
python -m outreach scan
```

---

### List

Display pending jobs:

```bash
python -m outreach list
```

---

### Draft

Display generated email drafts:

```bash
python -m outreach draft
```

---

### Send One

Send an email for a specific job:

```bash
python -m outreach send <id>
```

Example:

```bash
python -m outreach send 5
```

---

### Bulk Send

Send all eligible pending emails:

```bash
python -m outreach approve
```

EzApply processes all eligible jobs in one run instead of requiring approval for every individual email.

---

## 🤖 Automated Execution

The complete outreach process can be triggered using:

```bash
python auto_outreach.py
```

The automation performs:

```text
Scan
  ↓
Extract Jobs
  ↓
Match Jobs
  ↓
Store in Database
  ↓
Generate Emails
  ↓
Send Eligible Emails
```

---

## ☁️ GitHub Actions

EzApply can be executed automatically using GitHub Actions.

Example schedule:

```yaml
on:
  schedule:
    - cron: "0 */6 * * *"

  workflow_dispatch:
```

This allows the workflow to run periodically while also supporting manual execution.

### Required GitHub Secrets

```text
GMAIL_USER
GMAIL_PASS
LINKEDIN_STATE
```

These secrets are injected into the workflow as environment variables.

---

## 🔑 Gmail Configuration

EzApply uses Gmail SMTP for email delivery.

Required environment variables:

```text
GMAIL_USER
GMAIL_PASS
```

For Gmail accounts using 2-Step Verification, `GMAIL_PASS` should normally be a Gmail **App Password** rather than the regular account password.

---

## 📦 Installation

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

Linux / WSL:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Chromium

```bash
python -m playwright install chromium
```

---

## 🖥️ Local Usage

### Step 1 — Authenticate LinkedIn

```bash
python -m outreach login
```

This creates the LinkedIn authentication state.

---

### Step 2 — Add LinkedIn Posts

Add LinkedIn post URLs to:

```text
data/posts.txt
```

Example:

```text
https://www.linkedin.com/posts/example-post-123456
https://www.linkedin.com/posts/example-post-789012
```

---

### Step 3 — Run EzApply

```bash
python auto_outreach.py
```

EzApply will:

1. Read the LinkedIn URLs
2. Open the posts
3. Extract post content
4. Find recruiter emails
5. Match jobs
6. Store eligible jobs
7. Generate emails
8. Attach the resume
9. Send eligible emails

---

## 🔒 Security

Do **not** commit sensitive credentials or authentication data.

Recommended `.gitignore`:

```gitignore
# Python
.venv/
__pycache__/
*.pyc

# Environment
.env

# Database
data/outreach.db

# LinkedIn authentication
data/linkedin_state.json
browser_profile/

# IDE
.idea/
.vscode/
```

Store sensitive information using:

- Local environment variables / `.env`
- GitHub Actions Secrets

---

## 🧩 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Playwright | LinkedIn browser automation |
| SQLite | Job and outreach storage |
| SMTP | Email delivery |
| Gmail | Email provider |
| GitHub Actions | Scheduled execution |
| Regex | Email and job extraction |

---

## 🛣️ Roadmap

### ✅ Implemented

- [x] LinkedIn post URL input
- [x] LinkedIn authentication state
- [x] Post content extraction
- [x] Email extraction
- [x] Job matching
- [x] Match scoring
- [x] Email generation
- [x] Resume attachment
- [x] SQLite tracking
- [x] Bulk email sending
- [x] GitHub Actions integration
- [x] GitHub Secrets support
- [x] Local execution
- [x] CI/CD execution

### 🚧 Planned

- [ ] Automatic LinkedIn job search
- [ ] Automatic collection of relevant post URLs
- [ ] Automatic keyword-based search
- [ ] Duplicate URL detection
- [ ] Better company/recruiter extraction
- [ ] Improved job ranking
- [ ] Outreach statistics/dashboard

---

## ⚠️ Notes

EzApply is designed for personal job-search assistance.

LinkedIn automation should be used responsibly and in accordance with LinkedIn's applicable terms and policies.

The current version **does not automatically search LinkedIn**. Job post URLs are manually added to `data/posts.txt`.

---

## 👨‍💻 Author

**Abhijit Sahu**

A Python-based job outreach automation project using:

```text
Python
Playwright
SQLite
SMTP
Gmail
GitHub Actions
```
````
