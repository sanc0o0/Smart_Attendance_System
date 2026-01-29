from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import Attendance, Student
from schemas import AttendanceRequest
from session_manager import resolve_session
import pytz

router = APIRouter(prefix="/attendance", tags=["Attendance"])

IST = pytz.timezone("Asia/Kolkata")

@router.post("/mark-attendance")
def mark_attendance(payload: AttendanceRequest, db: Session = Depends(get_db)):
    name = payload.name
    face_id = payload.face_id or name.lower().replace(" ", "_")

    now_ist = datetime.now(IST)
    today = now_ist.date()
    time_now = now_ist.time()

    session, error = resolve_session(db, today, time_now)
    if error:
        return {"status": "rejected", "message": error}

    student = db.query(Student).filter(Student.face_id == face_id).first()
    if not student:
        student = Student(name=name, face_id=face_id)
        db.add(student)
        db.commit()
        db.refresh(student)

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