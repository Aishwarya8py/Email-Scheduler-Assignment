# app/models/schedule.py
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    email: str
    subject: str = "Weather update for {{city}}"
    body_template: str = "Hello, current temperature in {{city}} is {{temperature}}°C."
    city: str
    latitude: float
    longitude: float
    send_at: str  # local datetime string, e.g. "2025-11-19T10:30:00"
    timezone: str = "Asia/Kolkata"


