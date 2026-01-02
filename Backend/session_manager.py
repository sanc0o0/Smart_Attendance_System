from datetime import time, datetime, date
from sqlalchemy.orm import Session
from .models import AttendanceSession, Holiday
from .holidays import HOLIDAYS

MORNING_START = time(8, 0)
MORNING_END = time(12, 59)

AFTERNOON_START = time(13, 0)
AFTERNOON_END = time(17, 30)


def resolve_session(db: Session, date, current_time):

    # HOLIDAY CHECK (HARD STOP)
    is_holi, reason = is_holiday(db, date)
    if is_holi:
        return None, f"Holiday: {reason}"
    
    # weekday = date.weekday() # Monday is 0, Sunday is 6 

    # # Check for weekend
    # if weekday >= 5:
    #     return None, "Holiday: Weekend"
    
    # # Check for public holiday
    # if date in HOLIDAYS:
    #     return None, "Holiday: Public Holiday"
    
    # Determine session
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

    # MANUAL OVERRIDE CHECK
    if session.manually_closed:
        return None, f"{session_name.capitalize()} session closed"
    
    if session.manually_opened:
        return session_name, None
    
    
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


def is_holiday(db: Session, today: date):
    # admin-defined holiday
    holiday = db.query(Holiday).filter(Holiday.date == today).first()
    if holiday:
        return True, holiday.reason
    
    # weekend
    if today.weekday() >= 5:
        return True, "Holiday: Weekend"
    
    return False, None
