
import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")  # your Gmail address
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("aishwaryadas834@gmail.com", SMTP_USER)
USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"


def send_email(to_email: str, subject: str, body: str) -> None:
    """
    Send an email via SMTP (e.g. Gmail).
    """
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP_USER / SMTP_PASS not configured in .env")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        if USE_TLS:
            server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
