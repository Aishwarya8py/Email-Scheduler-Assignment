import os

from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "email_scheduler_db")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "yourgmail@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "your_app_password_here")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
