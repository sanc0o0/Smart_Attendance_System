# Smart Attendance System (Face Recognition)

A production-oriented **face recognition–based attendance system** with:
- Admin-controlled sessions
- Real-time attendance marking
- No student login (face = identity)
- Clean separation of backend, frontend, and camera client

This repository is designed so it can be **cloned, deployed, and extended** for real institutions.

---

##  System Overview

**Actors**
- **Admin**: Controls sessions, views attendance, analytics
- **Student**: No login, identified via face recognition

**Flow**
1. Admin logs into dashboard
2. Admin starts an attendance session
3. Camera client recognizes faces
4. Backend validates active session
5. Attendance is marked once per session

---

##  Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Session-based admin authentication

### Frontend
- Next.js (App Router)
- Role-protected admin pages
- API-driven UI

### Face Recognition Client
- OpenCV
- Haar Cascade
- Face encodings (local)
- Camera-based recognition

---

## 📁 Project Structure

```
├── Backend/ # API & business logic
│ ├── routes/ # Auth, attendance, sessions, analytics
│ ├── dependencies/ # Role guards & auth helpers
│ ├── models.py # DB models
│ ├── schemas.py # Request/response schemas
│ ├── session_manager.py # Attendance session control
│ └── main.py # FastAPI entry point
│
├── Client/ # Camera & face recognition
│ ├── capture_faces.py
│ ├── encode_faces.py
│ └── recognize_attendance.py
│
├── frontend/ # Admin dashboard (Next.js)
│
├── dataset_/ # Student face images
├── encodings_/ # Generated face encodings
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL
- Webcam (USB or built-in)

---

##  Backend Setup

```bash
cd Backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## Environment Variables

```bash 

# Create .env using .env.example:

DATABASE_URL=postgresql://user:password@localhost/attendance_db
SECRET_KEY=your_secret_key

# Run Backend
uvicorn main:app --reload
```

## API will be available at:

http://localhost:8000

## Admin Setup

Seed initial admin user. 
And use the seeded credentials to log in.
```
python scripts/seed_admin.py
```
## Frontend Setup
```
cd frontend
npm install
npm run dev
```

Open:
```
http://localhost:3000
```

Admin-only routes are protected via backend auth.

## Face Recognition Setup
### Step 1: Capture Student Faces
```
cd Client
python capture_faces.py
```

1. Enter student ID
2. Capture multiple angles
3. Images saved in dataset_/

### Step 2: Encode Faces
```
python encode_faces.py
```
1. Converts images into numerical encodings
2. Stored in encodings_/

### Step 3: Start Attendance Recognition
```
python recognize_attendance.py
```


What this does:
- Opens camera
- Detects faces
- Matches encodings
- Sends attendance to backend
- Prevents duplicate marking

## Attendance Session Logic

Attendance is only marked when:

- Admin session is ACTIVE

- Student is recognized

- Student has not already been marked

This logic lives in:

Backend/session_manager.py


# How to Extend This Project

You can:
- Add attendance reports (PDF / CSV)
- Add multi-class or multi-branch support
- Replace Haar Cascade with deep learning models
- Add hardware camera integration
- Deploy backend + frontend on cloud, keep client local

The architecture is intentionally modular.

## Notes
```

Face recognition runs locally (not as an API)

Backend only validates and stores data

This avoids security and performance issues
```
```
AND IF YOU STILL GET STUCK AND NEED HELP SETTING UP THIS PROJECT REACH OUT TO ME @sanc0o0 on linkedin or drop me an email at sanansari0305@gmail.com
```