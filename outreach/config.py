import os
from pathlib import Path

BROWSER_PROFILE = Path("browser_profile")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
POSTS_FILE = DATA_DIR / "posts.txt"
RESUME_FILE = DATA_DIR / "Abhijit_Sahu_CV.pdf"
DB_FILE = DATA_DIR / "outreach.db"


def load_env_file():
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def csv_env(name, default=""):
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


def get_config():
    load_env_file()
    return {
        "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "smtp_user": os.getenv("SMTP_USER", ""),
        "smtp_password": os.getenv("SMTP_PASSWORD", ""),
        "from_name": os.getenv("FROM_NAME", "Abhijit Sahu"),
        "candidate_name": os.getenv("CANDIDATE_NAME", "Abhijit Sahu"),
        "candidate_email": os.getenv("CANDIDATE_EMAIL", ""),
        "candidate_phone": os.getenv("CANDIDATE_PHONE", ""),
        "candidate_location": os.getenv("CANDIDATE_LOCATION", "India"),
        "target_roles": csv_env(
            "TARGET_ROLES",
            "AWS Cloud Engineer,Cloud Engineer,DevOps Engineer,DevOps,"
            "Site Reliability Engineer,Kubernetes Engineer",
        ),
        "target_keywords": csv_env(
            "TARGET_KEYWORDS",
            "AWS,Kubernetes,Docker,Terraform,Linux,DevOps,Cloud,EC2,EKS,"
            "IAM,VPC,CI/CD,Prometheus,Grafana",
        ),
    }
