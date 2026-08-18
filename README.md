````markdown
# 🚀 EzApply

**EzApply** is a Python-based job outreach automation tool that helps automate the process of finding suitable LinkedIn job posts, extracting recruiter email addresses, matching jobs against your target roles, and sending personalized cold emails with your resume.

> **Current status:** LinkedIn job searching is currently manual. You paste LinkedIn post URLs into `posts.txt`. Automatic LinkedIn search is planned for a future version.

---

## ✨ Features

- 🔗 Read LinkedIn job post URLs from `posts.txt`
- 🌐 Open LinkedIn posts using Playwright and `LINKEDIN_STATE`
- 📝 Extract job-post content automatically
- 📧 Detect recruiter email addresses from posts
- 🎯 Match jobs against configured Cloud/DevOps roles
- 📊 Calculate a job match score
- ✉️ Generate personalized cold emails
- 📎 Attach resume automatically
- 📤 Send multiple applications in one run
- 🗃️ Store jobs and email status in SQLite
- 🔐 Use GitHub Secrets for credentials
- ⚙️ Run automatically using GitHub Actions
- 🖥️ Supports local execution and CI/CD execution

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
````

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

Currently, LinkedIn searching is performed **manually**.

Add LinkedIn post URLs to:

```text
data/posts.txt
```

Example:

```text
https://www.linkedin.com/posts/example-devops-hiring-123456
https://www.linkedin.com/posts/example-aws-engineer-789012
```

EzApply then reads these URLs and opens the posts internally using Playwright.

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

EzApply uses a Playwright authentication state instead of storing your LinkedIn username/password.

```text
LINKEDIN_STATE
```

The state is stored locally as:

```text
data/linkedin_state.json
```

For GitHub Actions, it is stored as a GitHub Secret.

```text
LINKEDIN_STATE
```

The workflow restores the state before running EzApply.

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

Experience keywords include:

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

EzApply generates a personalized email based on the extracted job information.

Example structure:

```text
Hi Hiring Manager,

I came across your LinkedIn post regarding the DevOps Engineer opportunity.

I am interested in the role and have hands-on experience working with
AWS infrastructure, Kubernetes, Docker, Linux and related technologies.

My resume is attached for your consideration.

Thanks and regards,
Abhijit Sahu
```

The resume is automatically attached:

```text
data/Abhijit_Sahu_CV.pdf
```

---

## 🗃️ SQLite Database

EzApply stores job information and email status in:

```text
data/outreach.db
```

The database helps prevent duplicate emails and keeps track of processed jobs.

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

### Scan

Read URLs from `posts.txt` and extract job information:

```bash
python -m outreach scan
```

### List

Show pending jobs:

```bash
python -m outreach list
```

### Draft

Display generated emails:

```bash
python -m outreach draft
```

### Send One

Send a specific job:

```bash
python -m outreach send <id>
```

### Approve / Bulk Send

Send all eligible pending emails:

```bash
python -m outreach approve
```

---

## 🤖 Automated Execution

The complete workflow can be triggered through:

```bash
python auto_outreach.py
```

The automation performs:

```text
Scan
 ↓
Extract jobs
 ↓
Match jobs
 ↓
Store in database
 ↓
Generate emails
 ↓
Send eligible emails
```

---

## ☁️ GitHub Actions

EzApply can run periodically using GitHub Actions.

Example schedule:

```yaml
on:
  schedule:
    - cron: "0 */6 * * *"

  workflow_dispatch:
```

Required GitHub Secrets:

```text
GMAIL_USER
GMAIL_PASS
LINKEDIN_STATE
```

These values are injected into the workflow as environment variables.

---

## 🔑 Gmail Configuration

EzApply uses Gmail SMTP.

Required environment variables:

```text
GMAIL_USER
GMAIL_PASS
```

For Gmail, `GMAIL_PASS` should be an **App Password**, not your normal Gmail password, when required by your account's security configuration.

---

## 📦 Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright:

```bash
python -m playwright install chromium
```

---

## 🖥️ Local Usage

1. Authenticate LinkedIn:

```bash
python -m outreach login
```

2. Add LinkedIn post URLs to:

```text
data/posts.txt
```

3. Run:

```bash
python auto_outreach.py
```

EzApply will process the URLs and send eligible outreach emails.

---

## 🔒 Security

Never commit these files or credentials:

```text
.env
data/linkedin_state.json
data/outreach.db
```

Recommended `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc

.env

data/outreach.db
data/linkedin_state.json
browser_profile/

.idea/
.vscode/
```

Store sensitive values using:

* Local environment variables / `.env`
* GitHub Actions Secrets

---

## 🧩 Tech Stack

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| Python         | Core application            |
| Playwright     | LinkedIn browser automation |
| SQLite         | Job & outreach storage      |
| SMTP           | Email delivery              |
| Gmail          | Email provider              |
| GitHub Actions | Scheduled automation        |
| Regex          | Email/job extraction        |

---

## 🛣️ Roadmap

### ✅ Implemented

* [x] LinkedIn post URL input
* [x] LinkedIn authentication state
* [x] Post content extraction
* [x] Email extraction
* [x] Job matching
* [x] Match scoring
* [x] Email generation
* [x] Resume attachment
* [x] SQLite tracking
* [x] Bulk email sending
* [x] GitHub Actions integration
* [x] GitHub Secrets support

### 🚧 Planned

* [ ] Automatic LinkedIn job search
* [ ] Automatic collection of relevant post URLs
* [ ] Duplicate URL detection
* [ ] Better company/recruiter extraction
* [ ] Improved job ranking
* [ ] Outreach statistics/dashboard

---

## ⚠️ Notes

EzApply is designed for personal job-search assistance. LinkedIn access and automation should be used responsibly and in accordance with LinkedIn's applicable terms and policies.

---

## 👨‍💻 Author

**Abhijit Sahu**

Cloud / DevOps focused automation project built with Python, Playwright, SQLite, SMTP and GitHub Actions.

