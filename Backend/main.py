from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pytz

from database import Base, engine
from routes import api_router
import os 


app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(api_router)

IST = pytz.timezone("Asia/Kolkata")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Attendance System API"} 


