# app/services/scheduler.py

from datetime import datetime, timezone
from typing import Any

from ..db import schedules_col, logs_col
from ..utils.time_utils import now_utc
from .weather import fetch_weather
# from .email_sender import send_email  # not used in console mode


def render_template(template: str, ctx: dict) -> str:
   
    result = template
    for k, v in ctx.items():
        result = result.replace("{{" + k + "}}", str(v))
    return result


def _parse_send_at_utc(value: Any) -> datetime | None:
   
    if isinstance(value, datetime):
        
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None

    return None


async def process_due_schedules():
   
    now = now_utc()
    print("[scheduler] checking pending schedules at", now.isoformat())

   
    pending_cursor = schedules_col.find({"status": "pending"})
    pending_schedules = await pending_cursor.to_list(length=500)

    print(f"[scheduler] total pending schedules: {len(pending_schedules)}")

    due_schedules: list[dict] = []

    for sch in pending_schedules:
        send_at_raw = sch.get("send_at_utc")
        send_at = _parse_send_at_utc(send_at_raw)

        print(
            f"[scheduler] schedule {str(sch.get('_id'))} "
            f"send_at_utc={send_at_raw} -> parsed={send_at}"
        )

        if send_at is None:
           
            continue

        if send_at <= now:
            due_schedules.append(sch)

    print(f"[scheduler] due schedules after time filter: {len(due_schedules)}")

    for sch in due_schedules:
        await _send_one_schedule_console(sch)


async def _send_one_schedule_console(schedule_doc: dict):
   
    try:
        
        weather = fetch_weather(schedule_doc["latitude"], schedule_doc["longitude"])
        ctx = {
            "city": schedule_doc["city"],
            "temperature": weather["temperature"],
            "windspeed": weather["windspeed"],
            "time": weather["time"],
        }

        # 2) Fill subject/body templates
        subject = render_template(schedule_doc["subject"], ctx)
        body = render_template(schedule_doc["body_template"], ctx)

        # 3) "Send" to console
        print("=== EMAIL (console mode) ===")
        print("To:     ", schedule_doc["email"])
        print("Subject:", subject)
        print("Body:\n", body)
        print("============================")

        # 4) Log success
        await logs_col.insert_one({
            "schedule_id": schedule_doc["_id"],
            "sent_at_utc": now_utc(),
            "success": True,
            "error": None,
            "raw_content": {"subject": subject, "body": body},
        })

        # 5) Mark schedule as sent
        await schedules_col.update_one(
            {"_id": schedule_doc["_id"]},
            {"$set": {"status": "sent"}}
        )

    except Exception as e:
        print("[scheduler] error while processing schedule:", e)

        await logs_col.insert_one({
            "schedule_id": schedule_doc["_id"],
            "sent_at_utc": now_utc(),
            "success": False,
            "error": str(e),
            "raw_content": None,
        })

        await schedules_col.update_one(
            {"_id": schedule_doc["_id"]},
            {"$set": {"status": "failed"}}
        )

