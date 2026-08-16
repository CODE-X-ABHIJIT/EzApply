import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_email(config, recipient, subject, body, attachment):
    if not config["smtp_user"] or not config["smtp_password"]:
        raise RuntimeError("SMTP_USER/SMTP_PASSWORD are missing. Configure .env first.")

    attachment = Path(attachment)
    if not attachment.exists():
        raise FileNotFoundError(f"Resume not found: {attachment}")

    msg = EmailMessage()
    msg["From"] = f"{config['from_name']} <{config['smtp_user']}>"
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    mime, _ = mimetypes.guess_type(attachment.name)
    maintype, subtype = (mime or "application/octet-stream").split("/", 1)

    with attachment.open("rb") as f:
        msg.add_attachment(
            f.read(), maintype=maintype, subtype=subtype, filename=attachment.name
        )

    with smtplib.SMTP(config["smtp_host"], config["smtp_port"], timeout=30) as smtp:
        smtp.starttls()
        smtp.login(config["smtp_user"], config["smtp_password"])
        smtp.send_message(msg)
