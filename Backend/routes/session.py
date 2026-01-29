from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db
from .models import AttendanceSession
from .session_manager import resolve_session, is_holiday
from .session_manager import (
    MORNING_START, MORNING_END,
    AFTERNOON_START, AFTERNOON_END
)
from .session_manager import is_valid_admin_open_time
from .holidays import HOLIDAYS
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
def force_open_session(session: str, db: Session = Depends(get_db)):
    today = datetime.now(IST).date()
    current_time = datetime.now(IST).time()

    # # to enforce time rule
    # _, error = resolve_session(db, today, current_time)
    # if error :
    #     raise HTTPException(status_code=400, detail=error)

    # weekend and holidays hard stop
    is_holi, reason = is_holiday(db, today)
    if is_holi:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot open session on holiday"
        )
    
    # explicit time window check
    if not is_valid_admin_open_time(session, current_time):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot open {session} session outside the time window"
        )

    # to enforce time window strictly
    if session == "morning":
        if not (MORNING_START <= current_time <= MORNING_END):
            raise HTTPException(
                status_code=400,
                detail="Cannot open morning session"
            )
    elif session == "afternoon":
        if not (AFTERNOON_START <= current_time <= AFTERNOON_END):
            raise HTTPException(
                status_code=400,
                detail="Cannot open afternoon session"
            )
    else:
        raise HTTPException(status_code=400, detail="Invalid session")
    
    # to create or reopen session
    session_row = db.query(AttendanceSession).filter(
        AttendanceSession.date == today,
        AttendanceSession.session == session
    ).first()

    # to create new session if not exists
    if not session_row:
        session_row = AttendanceSession(
            date=today,
            session=session,
            is_open=True,
            opened_at=datetime.now(IST).time(),
            manually_opened=True,
            manually_closed=False
        )
        db.add(session_row)
    else:
        session_row.is_open = True
        session_row.manually_opened = True
        session_row.manually_closed = False
        session_row.opened_at = current_time
    
    # this update opened_at time
    db.commit()
    return {"status": "opened", "session": session}


@router.post("/close")
def force_close_session(session: str, db: Session = Depends(get_db)):
    today = datetime.now(IST).date()
    session_row = db.query(AttendanceSession).filter(
        AttendanceSession.date == today,
        AttendanceSession.session == session
    ).first()

    if not session_row or not session_row.is_open:
        return {"status": "already closed"}

    session_row.is_open = False
    session_row.manually_closed = True
    session_row.closed_at = datetime.now(IST).time()
    db.commit()

    return {"status": "closed", "session": session}
