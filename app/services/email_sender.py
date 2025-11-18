import smtplib
from email.message import EmailMessage

from ..config import FROM_EMAIL, SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER


def send_email(to_email: str, subject: str, body: str):
    
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
