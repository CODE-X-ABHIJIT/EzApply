import argparse

from .browser import login, read_all

from .config import (
    get_config,
    POSTS_FILE,
    RESUME_FILE,
)

from .database import (
    init_db,
    add_job,
    get_job,
    pending_jobs,
    email_already_sent,
    mark_sent,
    mark_rejected,
)

from .extractor import (
    read_urls,
    extract_post,
)

from .matcher import score_post
from .templates import make_email
from .mailer import send_email


# ============================================================
# LOGIN
# ============================================================

def cmd_login():
    login()


# ============================================================
# SCAN LINKEDIN POSTS
# ============================================================

def cmd_scan(config):
    init_db()

    if not POSTS_FILE.exists():
        print(f"Missing: {POSTS_FILE}")
        return

    urls = read_urls()

    if not urls:
        print("No LinkedIn post URLs found in posts.txt")
        return

    print("\n" + "=" * 72)
    print(f"Found {len(urls)} LinkedIn post URL(s)")
    print("=" * 72)

    # Open/process all URLs using one browser session
    results = read_all(urls)

    added = 0
    skipped = 0
    failed = 0

    for index, result in enumerate(results, start=1):

        post_url = result["url"]
        post_text = result["text"]

        print("\n" + "-" * 72)
        print(f"[{index}/{len(results)}]")
        print(f"URL: {post_url}")
        print("-" * 72)

        # ----------------------------------------------------
        # Browser error
        # ----------------------------------------------------

        if result["error"]:
            failed += 1

            print(
                f"ERROR: Could not read post\n"
                f"{result['error']}"
            )

            continue

        # ----------------------------------------------------
        # Empty post
        # ----------------------------------------------------

        if not post_text.strip():
            skipped += 1

            print(
                "SKIP: No visible post content detected."
            )

            continue

        print("Post content detected.")

        # ----------------------------------------------------
        # Extract information
        # ----------------------------------------------------

        job = extract_post(post_text)

        # ----------------------------------------------------
        # Match job against target criteria
        # ----------------------------------------------------

        match = score_post(
            job,
            config,
        )

        job["match_score"] = match["score"]

        job["matched_keywords"] = ", ".join(
            match["matched_keywords"]
        )

        # ----------------------------------------------------
        # Generate cold email
        # ----------------------------------------------------

        job["subject"], job["body"] = make_email(
            job,
            config,
        )

        # Store LinkedIn URL
        job["url"] = post_url

        # ----------------------------------------------------
        # No email found
        # ----------------------------------------------------

        if not job["email"]:

            skipped += 1

            print(
                "SKIP: No email address found "
                "in the post."
            )

            continue

        # ----------------------------------------------------
        # Save job
        # ----------------------------------------------------

        row_id = add_job(job)

        if row_id:

            added += 1

            print(
                f"Added #{row_id}: "
                f"{job['email']} | "
                f"{job['role'] or 'Unknown role'} | "
                f"match={job['match_score']}%"
            )

        else:

            print(
                "Already exists in database."
            )

    # ========================================================
    # SCAN SUMMARY
    # ========================================================

    print("\n" + "=" * 72)
    print("SCAN COMPLETED")
    print("=" * 72)

    print(f"URLs processed : {len(results)}")
    print(f"New jobs       : {added}")
    print(f"Skipped        : {skipped}")
    print(f"Failed         : {failed}")

    print("=" * 72)


# ============================================================
# LIST PENDING JOBS
# ============================================================

def cmd_list():

    init_db()

    rows = pending_jobs()

    if not rows:
        print("No pending jobs.")
        return

    print("\n" + "=" * 72)
    print("PENDING JOBS")
    print("=" * 72)

    for row in rows:

        print(
            f"#{row['id']} | "
            f"{row['match_score']:>3}% | "
            f"{row['email']} | "
            f"{row['role'] or 'Unknown role'} | "
            f"{row['company'] or 'Unknown company'}"
        )

    print("=" * 72)


# ============================================================
# PRINT EMAIL
# ============================================================

def print_job(row):

    print("\n" + "=" * 72)

    print(f"ID:        {row['id']}")
    print(f"Match:     {row['match_score']}%")
    print(f"Email:     {row['email']}")
    print(
        f"Recruiter: "
        f"{row['recruiter_name'] or 'Unknown'}"
    )
    print(
        f"Company:   "
        f"{row['company'] or 'Unknown'}"
    )
    print(
        f"Role:      "
        f"{row['role'] or 'Unknown'}"
    )
    print(
        f"Location:  "
        f"{row['location'] or 'Unknown'}"
    )
    print(
        f"Keywords:  "
        f"{row['matched_keywords']}"
    )
    print(
        f"Subject:   "
        f"{row['subject']}"
    )

    print("\nEMAIL BODY\n")

    print(row["body"])

    print("=" * 72)


# ============================================================
# SEND SINGLE EMAIL
# ============================================================

def cmd_send(config, job_id):

    init_db()

    row = get_job(job_id)

    if not row:

        print("Job not found.")
        return

    if email_already_sent(row["email"]):

        print(
            f"Already sent to "
            f"{row['email']}."
        )

        return

    print_job(row)

    confirmation = input(
        "\nSend this email with resume? [y/N]: "
    ).strip().lower()

    if confirmation != "y":

        print("Not sent.")
        return

    try:

        send_email(
            config,
            row["email"],
            row["subject"],
            row["body"],
            RESUME_FILE,
        )

        mark_sent(job_id)

        print(
            "Email sent and recorded."
        )

    except Exception as exc:

        print(
            f"Send failed: {exc}"
        )


# ============================================================
# SEND ALL PENDING EMAILS
# ============================================================

def cmd_approve(config):

    init_db()

    rows = pending_jobs()

    if not rows:

        print("No pending jobs.")
        return

    # --------------------------------------------------------
    # Find eligible emails
    # --------------------------------------------------------

    eligible = []

    seen_emails = set()

    for row in rows:

        email = row["email"]

        if not email:
            continue

        if email_already_sent(email):
            continue

        # Prevent sending multiple emails
        # to the same address in this batch
        email_key = email.lower().strip()

        if email_key in seen_emails:
            continue

        seen_emails.add(email_key)

        eligible.append(row)

    # --------------------------------------------------------
    # Nothing to send
    # --------------------------------------------------------

    if not eligible:

        print(
            "No eligible emails to send."
        )

        return

    # --------------------------------------------------------
    # Show batch
    # --------------------------------------------------------

    print("\n" + "=" * 72)
    print(
        f"READY TO SEND: "
        f"{len(eligible)} EMAIL(S)"
    )
    print("=" * 72)

    for row in eligible:

        print(
            f"#{row['id']} | "
            f"{row['email']} | "
            f"{row['role'] or 'Unknown role'} | "
            f"{row['company'] or 'Unknown company'} | "
            f"match={row['match_score']}%"
        )

    print("=" * 72)

    # --------------------------------------------------------
    # Single confirmation
    # --------------------------------------------------------

    confirmation = input(
        f"\nSend ALL {len(eligible)} emails "
        f"with resume? [y/N]: "
    ).strip().lower()

    if confirmation != "y":

        print(
            "Nothing sent."
        )

        return

    # --------------------------------------------------------
    # Send batch
    # --------------------------------------------------------

    sent = 0
    failed = 0

    print(
        "\nStarting email delivery...\n"
    )

    for row in eligible:

        try:

            send_email(
                config,
                row["email"],
                row["subject"],
                row["body"],
                RESUME_FILE,
            )

            mark_sent(row["id"])

            sent += 1

            print(
                f"[SENT] "
                f"#{row['id']} -> "
                f"{row['email']}"
            )

        except Exception as exc:

            failed += 1

            print(
                f"[FAILED] "
                f"#{row['id']} -> "
                f"{row['email']} | "
                f"{exc}"
            )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n" + "=" * 72)
    print("EMAIL DELIVERY COMPLETE")
    print("=" * 72)

    print(f"Sent   : {sent}")
    print(f"Failed : {failed}")
    print(f"Total  : {len(eligible)}")

    print("=" * 72)


# ============================================================
# MAIN CLI
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "LinkedIn Job Outreach Assistant"
        )
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # --------------------------------------------------------
    # Login
    # --------------------------------------------------------

    sub.add_parser(
        "login",
        help=(
            "Open browser and login "
            "to LinkedIn"
        ),
    )

    # --------------------------------------------------------
    # Scan
    # --------------------------------------------------------

    sub.add_parser(
        "scan",
        help=(
            "Automatically open all LinkedIn "
            "URLs and extract job information"
        ),
    )

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    sub.add_parser(
        "list",
        help="List pending jobs",
    )

    # --------------------------------------------------------
    # Draft
    # --------------------------------------------------------

    sub.add_parser(
        "draft",
        help="Show generated email drafts",
    )

    # --------------------------------------------------------
    # Single send
    # --------------------------------------------------------

    send = sub.add_parser(
        "send",
        help="Send one specific email",
    )

    send.add_argument(
        "id",
        type=int,
    )

    # --------------------------------------------------------
    # Batch send
    # --------------------------------------------------------

    sub.add_parser(
        "approve",
        help=(
            "Send all eligible pending emails "
            "after one confirmation"
        ),
    )

    args = parser.parse_args()

    config = get_config()

    # ========================================================
    # COMMAND ROUTING
    # ========================================================

    if args.command == "login":

        cmd_login()

    elif args.command == "scan":

        cmd_scan(config)

    elif args.command == "list":

        cmd_list()

    elif args.command == "draft":

        init_db()

        rows = pending_jobs()

        if not rows:

            print(
                "No pending jobs."
            )

            return

        for row in rows:

            print_job(row)

    elif args.command == "send":

        cmd_send(
            config,
            args.id,
        )

    elif args.command == "approve":

        cmd_approve(config)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()