from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, time
import pytz

from .analytics import router as analytics_router
# from . import models
from .database import SessionLocal, Base, engine
from .models import Student, Attendance
from .schemas import AttendanceRequest


app = FastAPI()

Base.metadata.create_all(bind=engine)

IST = pytz.timezone("Asia/Kolkata")

def get_session(time_obj):
    morning_start = time(8, 0)
    morning_end = time(12, 59)

    afternoon_start = time(13, 0)
    afternoon_end = time(17, 30)

    if morning_start <= time_obj <= morning_end:
        return "morning"
    elif afternoon_start <= time_obj <= afternoon_end:
        return "afternoon"
    else:
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

    session = get_session(time_now)
    if not session:
        return {
            "status": "rejected",
            "message": "Attendance allowed only in morning or afternoon sessions"
        }

    # 1️⃣ Find or create student
    student = db.query(Student).filter(Student.face_id == face_id).first()
    if not student:
        student = Student(name=name, face_id=face_id)
        db.add(student)
        db.commit()
        db.refresh(student)

    # # 2️⃣ Insert attendance
    # attendance = Attendance(
    #     student_id=student.id,
    #     attendance_date=today,
    #     attendance_time=time_now
    # )


    existing = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.attendance_date == today,
        Attendance.session == session
    ).first()

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



@app.get("/marked-today")
def get_marked_today(db: Session = Depends(get_db)):
    today = datetime.now(IST).date()

    records = (
        db.query(Student.name)
        .join(Attendance)
        .filter(Attendance.attendance_date == today)
        .all()
    )

    return {
        "status": "success",
        "marked": [r[0] for r in records]
    }


