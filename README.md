# EzApply — Automated LinkedIn Job Outreach

EzApply is an automation tool that helps streamline the job application outreach process.

It searches LinkedIn job/hiring posts, collects relevant post URLs, reads the post content using an authenticated LinkedIn session, extracts recruiter email addresses, matches jobs against your target roles and experience, generates personalized cold emails, attaches your resume, and sends the emails automatically.

The project can run **locally** or through **GitHub Actions** on a scheduled basis.

---

## 🚀 Features

* 🔎 Automated LinkedIn hiring-post search
* 🔗 Automatically collects LinkedIn post URLs
* 📝 Stores post URLs in `posts.txt`
* 🔐 Uses a saved LinkedIn authentication state
* 🌐 Reads LinkedIn posts without manually opening every URL
* 📧 Extracts recruiter/HR email addresses from posts
* 🎯 Matches posts against configured roles and experience
* 📊 Calculates a job match score
* 🧑‍💼 Extracts recruiter, company, role and location information
* ✉️ Generates personalized cold emails
* 📎 Automatically attaches resume
* 📤 Sends multiple emails automatically
* 🗃️ Tracks jobs and email status using SQLite
* ♻️ Prevents sending duplicate emails
* ⚙️ Supports completely automated execution
* ☁️ Supports GitHub Actions
* ⏰ Supports scheduled execution
* 🔑 Uses GitHub Secrets for credentials
* 💻 Works locally using Python virtual environment

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       LinkedIn      │
                         │   Hiring Posts      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ linkedin_search.py  │
                         │                     │
                         │ Search hiring posts │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     posts.txt       │
                         │                     │
                         │ LinkedIn Post URLs  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Playwright       │
                         │                     │
                         │ LinkedIn session    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Post Extraction   │
                         │                     │
                         │ Post content        │
                         │ Email addresses     │
                         │ Role                │
                         │ Recruiter            │
                         │ Company              │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Matcher        │
                         │                     │
                         │ Role matching       │
                         │ Experience matching │
                         │ Match score         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Email Generator   │
                         │                     │
                         │ Subject             │
                         │ Cold email          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Mailer        │
                         │                     │
                         │ Gmail SMTP          │
                         │ Resume attachment   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Recruiter      │
                         └─────────────────────┘

                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    outreach.db      │
                         │                     │
                         │ Jobs                │
                         │ Emails              │
                         │ Sent status         │
                         └─────────────────────┘
```

---

# 📂 Project Structure

```text
EzApply/
│
├── outreach/
│   │
│   ├── __init__.py
│   ├── __main__.py
│   │
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
│   │
│   ├── posts.txt
│   ├── Abhijit_Sahu_CV.pdf
│   └── outreach.db
│
├── linkedin_search.py
├── auto_outreach.py
├── requirements.txt
├── .gitignore
└── .github/
    └── workflows/
        └── outreach.yml
```

---

# 🔄 Complete Workflow

EzApply follows this workflow:

```text
LinkedIn Search
      ↓
Find Hiring Posts
      ↓
Extract Post URLs
      ↓
posts.txt
      ↓
Read LinkedIn Posts
      ↓
Extract Post Content
      ↓
Find Email Addresses
      ↓
Match Job
      ↓
Generate Cold Email
      ↓
Attach Resume
      ↓
Send Email
      ↓
Store Result in SQLite
```

---

# 🔎 1. LinkedIn Job Search

`linkedin_search.py` is responsible for searching LinkedIn for relevant hiring posts.

Typical search targets include:

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

The search can also target experience levels such as:

```text
Fresher
0-1 years
0-2 years
1-2 years
Entry Level
```

The resulting LinkedIn post URLs are stored in:

```text
data/posts.txt
```

Example:

```text
https://www.linkedin.com/posts/example-hiring-devops-123456
https://www.linkedin.com/posts/example-cloud-engineer-789012
```

The actual post content does **not** need to be manually copied.

---

# 📝 2. `posts.txt`

`posts.txt` acts as the input queue for LinkedIn hiring posts.

Example:

```text
https://www.linkedin.com/posts/recruiter-example-hiring-devops-123
https://www.linkedin.com/posts/example-cloud-engineer-456
https://www.linkedin.com/posts/example-aws-hiring-789
```

EzApply reads these URLs and processes them automatically.

---

# 🔐 3. LinkedIn Authentication

EzApply uses Playwright to access LinkedIn.

Instead of storing your LinkedIn password in the project, EzApply uses a saved authentication state:

```text
LINKEDIN_STATE
```

Locally, this can be represented by:

```text
data/linkedin_state.json
```

For GitHub Actions, the authentication state is stored as a GitHub Secret:

```text
LINKEDIN_STATE
```

The workflow reconstructs the state file during execution.

```text
GitHub Secret
     ↓
LINKEDIN_STATE
     ↓
data/linkedin_state.json
     ↓
Playwright
     ↓
LinkedIn
```

This allows the automation to reuse the authenticated LinkedIn session.

---

# 🌐 4. Reading LinkedIn Posts

EzApply uses Playwright to open the LinkedIn URLs internally.

Instead of manually opening:

```text
Post 1
Post 2
Post 3
Post 4
...
```

the program processes all URLs automatically.

Example:

```text
Found 4 LinkedIn post URL(s)

[1/4] Reading: https://www.linkedin.com/...
[2/4] Reading: https://www.linkedin.com/...
[3/4] Reading: https://www.linkedin.com/...
[4/4] Reading: https://www.linkedin.com/...
```

The post content is then passed to the extractor.

---

# 📧 5. Email Extraction

EzApply searches the post content for email addresses.

For example, if a post contains:

```text
Hiring for DevOps Engineer.

Interested candidates can share their resume at:

khushi.malhotra@testingxperts.com
```

EzApply extracts:

```text
khushi.malhotra@testingxperts.com
```

If no email is found:

```text
SKIP: No email address found in the post.
```

This prevents unnecessary processing of posts without recruiter contact information.

---

# 🎯 6. Job Matching

The matcher compares the LinkedIn post against your configured target roles.

Example configuration:

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

EzApply calculates a match score.

Example:

```text
#1 | 81% | recruiter@example.com | DevOps Engineer
#2 | 75% | hr@example.com        | DevOps Engineer
```

This makes it easier to prioritize relevant opportunities.

---

# 🧑‍💼 7. Job Information Extraction

EzApply attempts to extract information such as:

```text
Recruiter
Company
Role
Location
Email
Experience
```

Example:

```text
Email:      recruiter@example.com
Role:       DevOps Engineer
Company:    Example Technologies
Location:   Bangalore
Experience: 0-2 years
```

When information is unavailable:

```text
Company: Unknown company
Recruiter: Unknown
```

---

# ✉️ 8. Cold Email Generation

EzApply automatically generates an email based on the extracted job information.

Example structure:

```text
Hi Hiring Manager,

I came across your LinkedIn post regarding the DevOps Engineer
opportunity at your organization.

I am interested in the role and have hands-on experience working
with AWS infrastructure, Kubernetes, Docker, Linux and related
cloud/infrastructure technologies.

My resume is attached for your consideration. I would be glad
to discuss how my experience could fit the opportunity.

Thanks and regards,
Abhijit Sahu
Noida
```

The subject is generated automatically:

```text
Application for DevOps Engineer – Abhijit Sahu
```

---

# 📎 9. Resume Attachment

The resume is stored inside:

```text
data/Abhijit_Sahu_CV.pdf
```

EzApply automatically attaches the resume to each outgoing email.

Before sending, the program verifies that the file exists.

If the resume is missing:

```text
Resume not found
```

---

# 📤 10. Email Sending

EzApply uses SMTP to send emails.

The mailer:

1. Creates an email
2. Adds recipient
3. Adds subject
4. Adds generated body
5. Attaches resume
6. Connects to SMTP
7. Authenticates
8. Sends email
9. Records the result

The application can send multiple eligible emails in one run.

Example:

```text
READY TO SEND: 2 EMAIL(S)

#1 | recruiter1@example.com | DevOps Engineer
#2 | recruiter2@example.com | DevOps Engineer

Starting email delivery...

[SENT] #1 -> recruiter1@example.com
[SENT] #2 -> recruiter2@example.com
```

---

# 🗃️ 11. SQLite Database

EzApply uses SQLite for job tracking.

Database:

```text
data/outreach.db
```

The database stores information such as:

```text
Job ID
Email
Role
Company
Location
Match Score
Subject
Email Body
Status
```

This allows EzApply to track previously processed jobs.

---

# ♻️ Duplicate Protection

Before sending an email, EzApply checks whether an email address has already received an email.

For example:

```text
recruiter@example.com
```

If that recruiter has already been contacted, EzApply skips the email.

This helps prevent repeatedly sending the same cold email.

---

# 📋 Viewing Jobs

Run:

```bash
python -m outreach list
```

Example:

```text
========================================================================
PENDING JOBS
========================================================================

#1 | 81% | recruiter1@example.com | DevOps Engineer | Unknown company
#2 | 75% | recruiter2@example.com | DevOps Engineer | Unknown company
```

---

# 🧪 Manual Scanning

To scan all URLs in `posts.txt`:

```bash
python -m outreach scan
```

Example:

```text
Found 4 LinkedIn post URL(s)

[1/4] Reading: https://www.linkedin.com/...
[2/4] Reading: https://www.linkedin.com/...
[3/4] Reading: https://www.linkedin.com/...
[4/4] Reading: https://www.linkedin.com/...
```

---

# 📧 Automated Outreach

The complete process can be executed using:

```bash
python auto_outreach.py
```

The automation can perform:

```text
Scan
 ↓
Extract
 ↓
Match
 ↓
Generate email
 ↓
List jobs
 ↓
Send eligible emails
```

This removes the need to manually execute every individual command.

---

# 🔑 Environment Variables

EzApply uses environment variables for sensitive information.

Required variables:

```text
GMAIL_USER
GMAIL_PASS
LINKEDIN_STATE
```

Candidate information can also be configured through the application configuration.

Example:

```text
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-app-password
LINKEDIN_STATE=...
```

**Never commit passwords, app passwords, authentication state, or other secrets to GitHub.**

---

# 📧 Gmail SMTP

EzApply sends mail through Gmail SMTP.

Typical Gmail SMTP configuration:

```text
SMTP Host: smtp.gmail.com
SMTP Port: 587
```

The application uses:

```text
STARTTLS
```

before authenticating.

For Gmail, use an **App Password** rather than your normal Gmail password when required by your account configuration.

---

# 🔒 GitHub Secrets

For GitHub Actions, configure:

```text
GMAIL_USER
GMAIL_PASS
LINKEDIN_STATE
```

under:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

The workflow passes them to the application as environment variables.

---

# ☁️ GitHub Actions

EzApply can run without your local machine being online by using GitHub Actions.

Example workflow:

```text
GitHub Actions
      │
      ├── Checkout repository
      │
      ├── Install Python
      │
      ├── Install dependencies
      │
      ├── Restore LinkedIn authentication
      │
      ├── Run EzApply
      │
      └── Send emails
```

---

# ⏰ Scheduled Automation

GitHub Actions can execute EzApply automatically using cron.

For example:

```yaml
schedule:
  - cron: "0 */6 * * *"
```

This runs approximately every six hours.

The schedule can be changed according to your requirements.

For example, every hour:

```yaml
schedule:
  - cron: "0 * * * *"
```

---

# 🤖 Fully Automated Mode

The intended automated workflow is:

```text
                    Every N Hours
                         │
                         ▼
                LinkedIn Search
                         │
                         ▼
                 Find Hiring Posts
                         │
                         ▼
                   posts.txt
                         │
                         ▼
                 Read All Posts
                         │
                         ▼
                 Extract Emails
                         │
                         ▼
                  Match Jobs
                         │
                         ▼
                Generate Emails
                         │
                         ▼
                  Attach Resume
                         │
                         ▼
                 Check Database
                         │
                    ┌────┴────┐
                    │         │
                  Already    New
                   Sent       │
                    │         ▼
                   Skip     Send
                              │
                              ▼
                         Save Status
```

---

# 🧰 Technologies Used

| Technology                | Purpose                     |
| ------------------------- | --------------------------- |
| Python                    | Main programming language   |
| Playwright                | LinkedIn browser automation |
| SQLite                    | Job/email tracking          |
| SMTP                      | Email delivery              |
| Gmail                     | Email provider              |
| GitHub Actions            | Scheduled automation        |
| Regex                     | Email/content extraction    |
| Python dotenv/environment | Configuration and secrets   |
| PDF                       | Resume attachment           |

---

# 📦 Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd EzApply
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
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

For Linux/CI environments:

```bash
python -m playwright install --with-deps chromium
```

---

# ⚙️ Local Configuration

Set your environment variables.

Example:

```bash
export GMAIL_USER="your-email@gmail.com"
export GMAIL_PASS="your-app-password"
```

Configure the LinkedIn authentication state according to the project's Playwright setup.

Make sure the resume exists:

```text
data/Abhijit_Sahu_CV.pdf
```

And add LinkedIn URLs to:

```text
data/posts.txt
```

---

# ▶️ Running EzApply

### Scan posts

```bash
python -m outreach scan
```

### View jobs

```bash
python -m outreach list
```

### Generate/view drafts

```bash
python -m outreach draft
```

### Send a specific job

```bash
python -m outreach send <id>
```

### Run automated outreach

```bash
python auto_outreach.py
```

---

# 📊 Example Execution

```text
========================================================================
Found 4 LinkedIn post URL(s)
========================================================================

[1/4] Reading: https://www.linkedin.com/...
[2/4] Reading: https://www.linkedin.com/...
[3/4] Reading: https://www.linkedin.com/...
[4/4] Reading: https://www.linkedin.com/...

------------------------------------------------------------------------
[1/4]
Post content detected.
Added #1: recruiter@example.com | DevOps Engineer | match=81%

------------------------------------------------------------------------
[2/4]
Post content detected.
SKIP: No email address found in the post.

------------------------------------------------------------------------
[3/4]
Post content detected.
Added #2: hr@example.com | DevOps Engineer | match=75%

========================================================================
SCAN COMPLETED
========================================================================

URLs processed : 4
New jobs       : 2
Skipped        : 1
Failed         : 0

========================================================================
READY TO SEND: 2 EMAIL(S)
========================================================================

#1 | recruiter@example.com | DevOps Engineer | match=81%
#2 | hr@example.com | DevOps Engineer | match=75%

Starting email delivery...

[SENT] #1 -> recruiter@example.com
[SENT] #2 -> hr@example.com

========================================================================
EMAIL DELIVERY COMPLETE
========================================================================

Sent   : 2
Failed : 0
Total  : 2
```

---

# 🛡️ Security

The following files/data should **not** be committed to GitHub:

```text
.env
data/linkedin_state.json
browser_profile/
*.db
*.sqlite
*.sqlite3
```

Recommended `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Environment
.env

# Playwright
browser_profile/

# LinkedIn authentication
data/linkedin_state.json

# Database
data/*.db
data/*.sqlite
data/*.sqlite3

# Temporary files
*.log
```

Use GitHub Secrets for:

```text
GMAIL_USER
GMAIL_PASS
LINKEDIN_STATE
```

---

# 🧠 Design Philosophy

EzApply separates the job application process into independent stages:

```text
Search
  ↓
Extraction
  ↓
Matching
  ↓
Generation
  ↓
Delivery
  ↓
Tracking
```

This makes the project easier to maintain and extend.

For example, the search mechanism can be changed without changing the email system.

Similarly, the email provider can be changed without rewriting the LinkedIn extraction logic.

---

# 🔮 Future Improvements

Potential future features include:

* Multiple LinkedIn search queries
* Better company extraction
* Recruiter name detection
* Job title normalization
* Job location detection
* Duplicate post detection
* Email open tracking
* Application status tracking
* Follow-up email scheduling
* Gmail API integration
* Multiple resume support
* Job-specific resume selection
* AI-based job matching
* AI-generated personalized outreach
* Application dashboard
* CSV/Excel export
* Analytics dashboard
* Recruiter response tracking
* Job history
* Blacklisted companies
* Minimum match-score filtering
* Rate limiting
* Retry handling
* GitHub Actions artifacts for reports

---

# ⚠️ Responsible Usage

EzApply is intended to reduce repetitive job-search and outreach work.

Use it responsibly:

* Respect LinkedIn's terms and applicable policies.
* Avoid excessive requests.
* Avoid sending large volumes of unsolicited emails.
* Use accurate information in your resume and outreach.
* Respect recruiter preferences and opt-outs.
* Keep credentials and authentication sessions private.
* Use reasonable scheduling and rate limits.

---

# 📌 Project Summary

**EzApply** automates the repetitive parts of LinkedIn-based job outreach.

```text
🔎 Find jobs
   ↓
🔗 Collect LinkedIn posts
   ↓
📝 Read posts automatically
   ↓
📧 Find recruiter emails
   ↓
🎯 Match relevant jobs
   ↓
✉️ Generate personalized outreach
   ↓
📎 Attach resume
   ↓
📤 Send emails
   ↓
🗃️ Track everything
   ↓
⏰ Repeat automatically
```

The goal is simple:

> **Spend less time searching, copying recruiter emails, preparing emails, and tracking applications — and more time preparing for the opportunities you find.**

---

## 👨‍💻 Author

**Abhijit Sahu**

**EzApply — Automated Job Search & Outreach Automation**
