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

SMTP_USER = os.getenv(
    "SMTP_USER",
    "",
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD",
    "",
)

LINKEDIN_STATE = os.getenv(
    "LINKEDIN_STATE",
    "",
)


# ============================================================
# CONFIG
# ============================================================

def get_config():

    return {
        "smtp_user": SMTP_USER,
        "smtp_password": SMTP_PASSWORD,

        "target_roles": [
            "AWS Cloud Engineer",
            "Cloud Engineer",
            "AWS Engineer",
            "DevOps Engineer",
            "DevOps",
            "Kubernetes Engineer",
            "Site Reliability Engineer",
            "SRE",
        ],

        "experience": [
            "fresher",
            "0-1",
            "0-2",
            "1-2",
            "entry level",
        ],
    }