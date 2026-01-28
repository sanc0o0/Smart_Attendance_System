from pydantic import BaseModel

class AttendanceRequest(BaseModel):
    name: str
    face_id: str | None = None

class AdminLoginPayload(BaseModel):
    email: str
    password: str