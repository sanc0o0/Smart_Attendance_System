from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, time
import pytz

from .analytics import router as analytics_router
# from . import models
from .database import SessionLocal, Base, engine
from .models import Student, Attendance, AttendanceSession
from .schemas import AttendanceRequest
from .session_manager import resolve_session, is_holiday
from .session_status import router as session_router


app = FastAPI()
app.include_router(session_router)

Base.metadata.create_all(bind=engine)

IST = pytz.timezone("Asia/Kolkata")

def get_session(time_obj):
    morning_start = time(8, 0)
    morning_end = time(13, 0)

    afternoon_start = time(13, 0)
    afternoon_end = time(17, 30)

    if morning_start <= time_obj <= morning_end:
        return "morning"
    elif afternoon_start <= time_obj <= afternoon_end:
        return "afternoon"
    return None


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(analytics_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Attendance System API"}  


@app.post("/mark-attendance")
def mark_attendance(payload: AttendanceRequest, db: Session = Depends(get_db)):
    name = payload.name
    face_id = payload.face_id or name.lower().replace(" ", "_")

    now_ist = datetime.now(IST)
    today = now_ist.date()
    time_now = now_ist.time()

    session, error = resolve_session(db, today, time_now)
    if error:
        return {"status": "rejected", "message": error}

    # 1️⃣ Find or create student
    student = db.query(Student).filter(Student.face_id == face_id).first()
    if not student:
        student = Student(name=name, face_id=face_id)
        db.add(student)
        db.commit()
        db.refresh(student)

    # 2️⃣ Check if already marked
    existing = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student.id,
            Attendance.attendance_date == today,
            Attendance.session == session
        )
        .first()
    )

    if existing:
        return {
            "status": "already_marked",
            "message": f"{name} already marked for {session}",
            "data": {
                "name": name,
                "date": str(today),
                "session": session
            }
        }

    # 3️⃣ Insert attendance (ONCE)
    attendance = Attendance(
        student_id=student.id,
        attendance_date=today,
        attendance_time=time_now,
        session=session
    )

    db.add(attendance)
    db.commit()

    return {
        "status": "success",
        "message": f"{name} marked successfully for {session}",
        "data": {
            "name": name,
            "date": str(today),
            "time": now_ist.strftime("%I:%M %p"),
            "session": session,
            "timezone": "IST"
        }
    }

@app.get("/session/status")
def session_status(db: Session = Depends(get_db)):
    now = datetime.now(IST)
    today = now.date()
    current_time = now.time()

    is_holi, reason = is_holiday(db, today)
    if is_holi:
        session_row = db.query(AttendanceSession).filter(
            AttendanceSession.date == today
        ).first()
        return {
            "date": str(today),
            "is_holiday": True,
            "holiday_reason": reason,
            "session": None, 
            "session_open": False,
            "manual_override": (session_row.manually_opened or session_row.manually_closed) if session_row else False 
            
        }
    
    session, error = resolve_session(db, today, current_time)
    if error:
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
        "session": session,
        "session_open": True

    }

@app.post("/admin/session/open")
def force_open_session(date:str, session: str, db:Session = Depends(get_db)):
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

@app.post("/admin/session/close")
def force_close_session(date:str, session: str, db:Session = Depends(get_db)):
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