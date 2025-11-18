# app/utils/time_utils.py

from datetime import datetime
from zoneinfo import ZoneInfo


def now_utc() -> datetime:
    """
    Get current time in UTC as an aware datetime.
    """
    return datetime.now(tz=ZoneInfo("UTC"))


def to_utc(send_at_str: str, tz_name: str) -> datetime:
    """
    Convert a local datetime string and timezone to a UTC datetime.

    Example:
      send_at_str = "2025-11-18T16:10:00"
      tz_name     = "Asia/Kolkata"
    """
    local_zone = ZoneInfo(tz_name)
    # parse "YYYY-MM-DDTHH:MM:SS" -> naive datetime
    local_naive = datetime.fromisoformat(send_at_str)
    # attach local timezone
    local_dt = local_naive.replace(tzinfo=local_zone)
    # convert to UTC
    return local_dt.astimezone(ZoneInfo("UTC"))
