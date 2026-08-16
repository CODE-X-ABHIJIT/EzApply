def make_email(job, config):
    name = job["recruiter_name"] or "Hiring Manager"
    role = job["role"] or "Cloud / DevOps opportunity"
    company = job["company"] or "your organization"

    subject = f"Application for {role} – {config['candidate_name']}"

    body = f"""Hi {name},

I came across your LinkedIn post regarding the {role} opportunity at {company}.

I am interested in the role and have hands-on experience working with AWS infrastructure, Kubernetes, Docker, Linux and related cloud/infrastructure technologies.

My resume is attached for your consideration. I would be glad to discuss how my experience could fit the opportunity.

Thanks and regards,
{config['candidate_name']}
{config['candidate_location']}
"""

    if config["candidate_phone"]:
        body += f"{config['candidate_phone']}\n"
    if config["candidate_email"]:
        body += f"{config['candidate_email']}\n"

    return subject, body
