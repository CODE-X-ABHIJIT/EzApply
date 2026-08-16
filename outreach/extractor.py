import hashlib
import re

EMAIL_RE = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.I,
)

EXPERIENCE_RE = re.compile(
    r"\b(?:fresher|freshers|entry[- ]level|\d+\s*[-–]\s*\d+\s*(?:years?|yrs?)|\d+\+?\s*(?:years?|yrs?))\b",
    re.I,
)

ROLE_HINTS = [
    "AWS Cloud Engineer",
    "Cloud Engineer",
    "AWS Engineer",
    "DevOps Engineer",
    "DevOps",
    "Kubernetes Engineer",
    "Site Reliability Engineer",
    "SRE",
]


def first_match(pattern, text):
    match = re.search(pattern, text, re.I)
    return match.group(1).strip() if match else ""


def extract_post(post_text):
    post_text = post_text.strip()

    emails = list(dict.fromkeys(
        EMAIL_RE.findall(post_text)
    ))

    role = next(
        (
            hint
            for hint in ROLE_HINTS
            if re.search(re.escape(hint), post_text, re.I)
        ),
        "",
    )

    company = first_match(
        r"(?:company|organization|org)\s*[:\-]\s*([^\n|]+)",
        post_text,
    )

    location = first_match(
        r"(?:location|based in|job location)\s*[:\-]\s*([^\n|]+)",
        post_text,
    )

    recruiter = first_match(
        r"(?:recruiter|contact|hiring manager|hr)\s*[:\-]\s*([^\n|]+)",
        post_text,
    )

    experience = ", ".join(
        dict.fromkeys(
            EXPERIENCE_RE.findall(post_text)
        )
    )

    return {
        "post_text": post_text,
        "post_hash": hashlib.sha256(
            post_text.encode()
        ).hexdigest(),

        "email": emails[0] if emails else "",
        "all_emails": emails,

        "recruiter_name": recruiter,
        "company": company,
        "role": role,
        "location": location,
        "experience": experience,
    }


def read_urls():
    """
    Read LinkedIn post URLs from posts.txt.

    One URL per line.
    """
    from .config import POSTS_FILE

    if not POSTS_FILE.exists():
        return []

    urls = []

    for line in POSTS_FILE.read_text(
        encoding="utf-8"
    ).splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if line.startswith("http"):
            urls.append(line)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(urls))