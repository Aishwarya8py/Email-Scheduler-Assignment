# app/api/routes_schedules.py
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, UploadFile

from ..db import schedules_col
from ..models.schedule import ScheduleCreate
from ..services.excel_import import import_schedules_from_excel
from ..utils.time_utils import now_utc, to_utc

router = APIRouter()


def serialize_schedule(doc: dict) -> dict:
    """
    Convert MongoDB document to JSON-safe dict:
    - _id -> string
    """
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    return doc


@router.post("")
async def create_schedule(payload: ScheduleCreate):
    send_at_utc = to_utc(payload.send_at, payload.timezone)

    doc = {
        "email": payload.email,
        "subject": payload.subject,
        "body_template": payload.body_template,
        "city": payload.city,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "timezone": payload.timezone,
        "send_at_utc": send_at_utc,
        "status": "pending",
        "created_at": now_utc(),
    }

    result = await schedules_col.insert_one(doc)
    saved = await schedules_col.find_one({"_id": result.inserted_id})
    return serialize_schedule(saved)


@router.get("")
async def list_schedules():
    cursor = schedules_col.find({}).sort("created_at", -1)
    schedules = await cursor.to_list(length=100)
    return [serialize_schedule(s) for s in schedules]


@router.get("/{schedule_id}")
async def get_schedule(schedule_id: str):
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule id")

    schedule = await schedules_col.find_one({"_id": ObjectId(schedule_id)})
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return serialize_schedule(schedule)


@router.delete("/{schedule_id}")
async def cancel_schedule(schedule_id: str):
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule id")

    result = await schedules_col.update_one(
        {"_id": ObjectId(schedule_id)}, {"$set": {"status": "cancelled"}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return {"message": "Schedule cancelled"}


@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    content = await file.read()
    inserted = await import_schedules_from_excel(content)
    return {"inserted": inserted}


"""
# app/api/routes_schedules.py
from typing import List

from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.utils.time_utils import now_utc, to_utc

from ..db import schedules_col
from ..models.schedule import ScheduleCreate, ScheduleOut
from ..services.excel_import import import_schedules_from_excel

router = APIRouter()


@router.post("", response_model=ScheduleOut)
async def create_schedule(payload: ScheduleCreate):
    send_at_utc = to_utc(payload.send_at, payload.timezone)

    doc = {
        "email": payload.email,
        "subject": payload.subject,
        "body_template": payload.body_template,
        "city": payload.city,
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "timezone": payload.timezone,
        "send_at_utc": send_at_utc,
        "status": "pending",
        "created_at": now_utc(),
    }

    result = await schedules_col.insert_one(doc)
    saved = await schedules_col.find_one({"_id": result.inserted_id})
    return saved


@router.get("", response_model=List[ScheduleOut])
async def list_schedules():
    cursor = schedules_col.find({}).sort("created_at", -1)
    schedules = await cursor.to_list(length=100)
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleOut)
async def get_schedule(schedule_id: str):
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule id")

    schedule = await schedules_col.find_one({"_id": ObjectId(schedule_id)})
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.delete("/{schedule_id}")
async def cancel_schedule(schedule_id: str):
    if not ObjectId.is_valid(schedule_id):
        raise HTTPException(status_code=400, detail="Invalid schedule id")

    result = await schedules_col.update_one(
        {"_id": ObjectId(schedule_id)}, {"$set": {"status": "cancelled"}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return {"message": "Schedule cancelled"}


@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    content = await file.read()
    inserted = await import_schedules_from_excel(content)
    return {"inserted": inserted}
"""
