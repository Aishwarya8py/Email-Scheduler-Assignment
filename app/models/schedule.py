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


"""
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class ScheduleCreate(BaseModel):
    email: str
    subject: str = "Weather update for {{city}}"
    body_template: str = "Hello, current temperature in {{city}} is {{temperature}}°C."
    city: str
    latitude: float
    longitude: float
    send_at: str  # local datetime string, e.g. "2025-11-19T10:30:00"
    timezone: str = "Asia/Kolkata"


class ScheduleOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email: str
    subject: str
    body_template: str
    city: str
    latitude: float
    longitude: float
    timezone: str
    send_at_utc: datetime
    status: str
    created_at: datetime

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
"""
