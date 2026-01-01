from fastapi import APIRouter
from datetime import datetime, time
import pytz

from .holidays import HOLIDAYS
from .session_manager import (
    MORNING_START, MORNING_END,
    AFTERNOON_START, AFTERNOON_END
)

router = APIRouter(prefix="/session", tags=["Session"])

IST = pytz.timezone("Asia/Kolkata")

@router.get("/status")
def session_status():
    now = datetime.now(IST)
    today = now.date()
    current_time = now.time()
    weekday = today.weekday()  # 0=Mon, 6=Sun

    # Weekend
    if weekday >= 5:
        return {
            "date": str(today),
            "is_holiday": True,
            "holiday_reason": "Weekend",
            "session": None,
            "session_open": False
        }

    # Holiday
    if today in HOLIDAYS:
        return {
            "date": str(today),
            "is_holiday": True,
            "holiday_reason": "Holiday",
            "session": None,
            "session_open": False
        }

    # Determine session
    if MORNING_START <= current_time <= MORNING_END:
        session = "morning"
        open_at = MORNING_START
        close_at = MORNING_END
    elif AFTERNOON_START <= current_time <= AFTERNOON_END:
        session = "afternoon"
        open_at = AFTERNOON_START
        close_at = AFTERNOON_END
    else:
        return {
            "date": str(today),
            "is_holiday": False,
            "session": None,
            "session_open": False
        }

    return {
        "date": str(today),
        "is_holiday": False,
        "holiday_reason": None,
        "current_time": now.strftime("%I:%M %p"),
        "session": session,
        "session_open": True,
        "opens_at": open_at.strftime("%I:%M %p"),
        "closes_at": close_at.strftime("%I:%M %p")
    }

