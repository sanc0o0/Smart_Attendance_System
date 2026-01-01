from datetime import time
from sqlalchemy.orm import Session
from .models import AttendanceSession

MORNING_START = time(8, 0)
MORNING_END = time(12, 59)

AFTERNOON_START = time(13, 0)
AFTERNOON_END = time(17, 30)


def resolve_session(db: Session, date, current_time):
    if MORNING_START <= current_time <= MORNING_END:
        session_name = "morning"
        close_time = MORNING_END
    elif AFTERNOON_START <= current_time <= AFTERNOON_END:
        session_name = "afternoon"
        close_time = AFTERNOON_END
    else:
        return None, "Attendance not allowed at this time"

    session = db.query(AttendanceSession).filter(
        AttendanceSession.date == date,
        AttendanceSession.session == session_name
    ).first()
    # current_time = time(9, 30)

    if not session:
        session = AttendanceSession(
            date=date,
            session=session_name,
            is_open=True,
            opened_at=current_time
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # HARD STOP: session never reopens
    if not session.is_open:
        return None, f"{session_name.capitalize()} session closed"

    # Auto close
    if current_time > close_time:
        session.is_open = False
        session.closed_at = close_time
        db.commit()
        return None, f"{session_name.capitalize()} session closed"

    return session_name, None
