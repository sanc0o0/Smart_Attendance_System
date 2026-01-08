from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import AttendanceSession
from ..session_manager import resolve_session, is_holiday
from ..session_manager import (
    MORNING_START, MORNING_END,
    AFTERNOON_START, AFTERNOON_END
)
from ..holidays import HOLIDAYS
import pytz

router = APIRouter(prefix="/session", tags=["Session"])

IST = pytz.timezone("Asia/Kolkata")

@router.get("/status")
def session_status(db: Session = Depends(get_db)):
    now = datetime.now(IST)
    today = now.date()
    current_time = now.time()
    weekday = today.weekday()  # 0=Mon, 6=Sun

    response = {
        "date": str(today),
        "current_time": now.strftime("%I:%M %p"),
        "is_holiday": False,
        "holiday_reason": None,
        "session": None,
        "session_open": False,
        "opens_at": None,
        "closes_at": None,
        "manual_override": False,
    }

    # ─────────────────────────────
    # 1️ WEEKEND CHECK
    # ─────────────────────────────
    if weekday >= 5:
        response.update({
            "is_holiday": True,
            "holiday_reason": "Weekend"
        })
        return response

    # ─────────────────────────────
    # 2️ HOLIDAY CHECK (DB + FALLBACK)
    # ─────────────────────────────
    is_holi, reason = is_holiday(db, today)
    if not is_holi and today in HOLIDAYS:
        is_holi, reason = True, "Holiday"

    if is_holi:
        session_row = db.query(AttendanceSession).filter(
            AttendanceSession.date == today
        ).first()

        response.update({
            "is_holiday": True,
            "holiday_reason": reason,
            "manual_override": (
                session_row.manually_opened or session_row.manually_closed
            ) if session_row else False
        })
        return response

    # ─────────────────────────────
    # 3️ SESSION RESOLUTION (DB FIRST)
    # ─────────────────────────────
    session, error = resolve_session(db, today, current_time)

    if error or session is None:
        return response

    # DB resolved session → open
    response.update({
        "session": session,
        "session_open": True
    })

    # ─────────────────────────────
    # 4️ FALLBACK TIME WINDOW INFO
    # ─────────────────────────────
    if session == "morning":
        response.update({
            "opens_at": MORNING_START.strftime("%I:%M %p"),
            "closes_at": MORNING_END.strftime("%I:%M %p")
        })
    elif session == "afternoon":
        response.update({
            "opens_at": AFTERNOON_START.strftime("%I:%M %p"),
            "closes_at": AFTERNOON_END.strftime("%I:%M %p")
        })

    return response


@router.post("/open")
def force_open_session(date: str, session: str, db: Session = Depends(get_db)):
    session_row = db.query(AttendanceSession).filter(
        AttendanceSession.date == date,
        AttendanceSession.session == session
    ).first()

    if not session_row:
        session_row = AttendanceSession(
            date=date,
            session=session,
            is_open=True,
            opened_at=datetime.now(IST).time(),
            manually_opened=True
        )
        db.add(session_row)
    else:
        session_row.is_open = True
        session_row.manually_opened = True
        session_row.manually_closed = False

    db.commit()
    return {"status": "opened"}


@router.post("/close")
def force_close_session(date: str, session: str, db: Session = Depends(get_db)):
    session_row = db.query(AttendanceSession).filter(
        AttendanceSession.date == date,
        AttendanceSession.session == session
    ).first()

    if not session_row:
        return {"error": "Session not found"}

    session_row.is_open = False
    session_row.manually_closed = True
    session_row.closed_at = datetime.now(IST).time()
    db.commit()

    return {"status": "closed"}
