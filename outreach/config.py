import os
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

POSTS_FILE = DATA_DIR / "posts.txt"

RESUME_FILE = DATA_DIR / "Abhijit_Sahu_CV.pdf"

DB_FILE = DATA_DIR / "outreach.db"

LINKEDIN_STATE_FILE = DATA_DIR / "linkedin_state.json"


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

GMAIL_USER = os.getenv(
    "GMAIL_USER",
    "",
)

GMAIL_PASS = os.getenv(
    "GMAIL_PASS",
    "",
)

# Aliases used by mailer.py
SMTP_USER = GMAIL_USER
SMTP_PASSWORD = GMAIL_PASS

LINKEDIN_STATE = os.getenv(
    "LINKEDIN_STATE",
    "",
)


# ============================================================
# CONFIG
# ============================================================

def get_config():

    target_roles = [
        "AWS Cloud Engineer",
        "Cloud Engineer",
        "AWS Engineer",
        "DevOps Engineer",
        "DevOps",
        "Kubernetes Engineer",
        "Site Reliability Engineer",
        "SRE",
    ]

    target_keywords = [
        "AWS",
        "Cloud",
        "DevOps",
        "Kubernetes",
        "Docker",
        "Terraform",
        "CI/CD",
        "Jenkins",
        "GitHub Actions",
        "Linux",
        "OpenShift",
        "Ansible",
        "Python",
    ]

    return {
        # ====================================================
        # SMTP
        # ====================================================

        "smtp_user": GMAIL_USER,
        "smtp_password": GMAIL_PASS,

        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,

        "from_name": "Abhijit Sahu",


        # ====================================================
        # CANDIDATE
        # ====================================================

        "candidate_name": "Abhijit Sahu",
        "candidate_location": "Noida, India",
        "candidate_phone": "",
        "candidate_email": GMAIL_USER,


        # ====================================================
        # JOB MATCHING
        # ====================================================

        "target_roles": target_roles,
        "target_keywords": target_keywords,

        "experience": [
            "fresher",
            "0-1",
            "0-2",
            "1-2",
            "entry level",
        ],
    }