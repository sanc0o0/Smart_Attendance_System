"""
One-time admin seeding script.
Run manually in development only.
DO NOT USE IN PRODUCTION.
"""

import os
from passlib.context import CryptContext
from database import SessionLocal
from models import User

if os.getenv("ENV") == "production":
    raise RuntimeError("Seeding script must NOT be run in production")

ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if not ADMIN_PASSWORD:
    raise RuntimeError("ADMIN_PASSWORD env var not set")

pwd = CryptContext(schemes=["bcrypt"])
db = SessionLocal()

admin = User(
    name="Admin User",
    email=ADMIN_EMAIL,
    phone="9999999999",
    role="admin",
    password_hash=pwd.hash(ADMIN_PASSWORD),
    is_active=True
)

db.add(admin)
db.commit()
db.close()

print("Admin user seeded successfully")
