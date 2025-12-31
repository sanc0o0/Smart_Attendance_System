from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    face_id = Column(String, unique=True, nullable=False)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    attendance_date = Column(Date, nullable=False)
    session = Column(String, nullable=False)  # Morning / Afternoon
    attendance_time = Column(Time, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "attendance_date",
            "session",
            name="unique_attendance_per_session"
        ),
    )
