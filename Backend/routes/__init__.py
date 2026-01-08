from fastapi import APIRouter

from .attendance import router as attendance_router
from .session import router as session_router
from .analytics import router as analytics_router

api_router = APIRouter()

api_router.include_router(attendance_router)
api_router.include_router(session_router)
api_router.include_router(analytics_router)
