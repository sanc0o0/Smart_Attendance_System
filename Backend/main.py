from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import pytz

from .database import SessionLocal
from .models import Student, Attendance

app = FastAPI()

IST = pytz.timezone("Asia/Kolkata")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Attendance System API"}  


@app.post("/mark-attendance")
def mark_attendance(payload: dict, db: Session = Depends(get_db)):
    name = payload["name"]
    face_id = payload.get("face_id", name.lower().replace(" ", "_"))

    now_ist = datetime.now(IST)
    today = now_ist.date()
    time_now = now_ist.time()

    # 1️⃣ Find or create student
    student = db.query(Student).filter(Student.face_id == face_id).first()

    if not student:
        student = Student(name=name, face_id=face_id)
        db.add(student)
        db.commit()
        db.refresh(student)

    # 2️⃣ Insert attendance
    attendance = Attendance(
        student_id=student.id,
        attendance_date=today,
        attendance_time=time_now
    )

    try:
        db.add(attendance)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"{name} already marked today"
        )

    return {
        "status": "success",
        "name": name,
        "date": str(today),
        "time": now_ist.strftime("%I:%M %p"),
        "timezone": "IST"
    }
