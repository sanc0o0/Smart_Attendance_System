from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    face_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    attendance_date = Column(Date, nullable=False)
    attendance_time = Column(Time, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("student_id", "attendance_date", name="unique_attendance_per_day"),
    )
