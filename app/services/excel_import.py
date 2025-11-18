# app/services/excel_import.py
import pandas as pd

from app.db import schedules_col
from app.utils.time_utils import now_utc, to_utc


async def import_schedules_from_excel(file_bytes: bytes) -> list[str]:
   
    df = pd.read_excel(file_bytes)
    inserted_ids = []

    for _, row in df.iterrows():
        send_at_str = str(row["send_at"])
        tz = row.get("timezone", "Asia/Kolkata")

        doc = {
            "email": row["email"],
            "subject": "Weather update for {{city}}",
            "body_template": "Hello, current temperature in {{city}} is {{temperature}}°C.",
            "city": row["city"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "timezone": tz,
            "send_at_utc": to_utc(send_at_str, tz),
            "status": "pending",
            "created_at": now_utc(),
        }

        result = await schedules_col.insert_one(doc)
        inserted_ids.append(str(result.inserted_id))

    return inserted_ids
