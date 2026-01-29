from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func

from database import get_db
from models import Attendance, Student
import pytz

router = APIRouter(prefix="/analytics", tags=["Analytics"])

IST = pytz.timezone("Asia/Kolkata")

@router.get("/today")
def attendance_today(db: Session = Depends(get_db)):
    today = datetime.now(IST).date()

    morning = db.query(func.count(Attendance.id)).filter(
        Attendance.attendance_date == today,
        Attendance.session == "morning"
    ).scalar()

    afternoon = db.query(func.count(Attendance.id)).filter(
        Attendance.attendance_date == today,
        Attendance.session == "afternoon"
    ).scalar()

    return {
        "date": str(today),
        "morning": morning,
        "afternoon": afternoon,
        "total": morning + afternoon
    }


@router.get("/students")
def attendance_by_student(db: Session = Depends(get_db)):
    # total distinct attendance days in system
    total_days = db.query(
        func.count(func.distinct(Attendance.attendance_date))
    ).scalar() or 0

    results = (
        db.query(
            Student.name,
            func.count(func.distinct(Attendance.attendance_date)).label("present_days")
        )
        .join(Attendance)
        .group_by(Student.id)
        .order_by(func.count(func.distinct(Attendance.attendance_date)).desc())
        .all()
    )

    return [
        {
            "name": name,
            "present_days": present_days,
            "total_days": total_days
        }
        for name, present_days in results
    ]

