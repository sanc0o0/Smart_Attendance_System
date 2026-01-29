from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.types import Boolean
from datetime import time

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

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    session = Column(String, nullable=False)  # morning / afternoon
    is_open : Mapped[bool] = mapped_column(Boolean, default=True)
    opened_at: Mapped[time] = mapped_column(Time, nullable=False)
    closed_at: Mapped[time | None] = mapped_column(Time, nullable=True)
    
    manually_opened: Mapped[bool] = mapped_column(Boolean, default=False)
    manually_closed: Mapped[bool] = mapped_column(Boolean, default=False)


    __table_args__ = (
        UniqueConstraint("date", "session", name="unique_date_session"),
    )

class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    role = Column(String, default="admin")  
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
#     phone: Mapped[str | None] = mapped_column(String, nullable=True)

#     role: Mapped[str] = mapped_column(String, default="admin")
#     password_hash: Mapped[str] = mapped_column(String, nullable=False)

#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
#     created_at: Mapped = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now()
#     )