import cv2
import requests
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import pytz

# ----------------------------
# BACKEND CONFIG
# ----------------------------
API_MARK_ATTENDANCE = "http://127.0.0.1:8000/attendance/mark-attendance"
API_MARKED_TODAY = "http://127.0.0.1:8000/marked-today"
SESSION_STATUS_URL = "http://127.0.0.1:8000/session/status"

# ----------------------------
# FACE CONFIG
# ----------------------------
ENCODING_FILE = "Encodings/face_encodings.pkl"
CONFIDENCE_THRESHOLD = 0.6
STABLE_FRAMES_REQUIRED = 8

IST = pytz.timezone("Asia/Kolkata")

# ----------------------------
# LOAD FACE ENCODINGS
# ----------------------------
print("[INFO] Loading face encodings...")
with open(ENCODING_FILE, "rb") as f:
    data = pickle.load(f)

KNOWN_ENCODINGS = data["encodings"]
KNOWN_NAMES = data["names"]

print(f"[INFO] Loaded {len(KNOWN_NAMES)} known faces")

# ----------------------------
# CLIENT STATE
# ----------------------------
frame_stability = {}        # name -> frame count
finalized_today = set()     # name already decided today
rejected_today = set()      # name rejected by backend

# ----------------------------
# FETCH ALREADY MARKED (BACKEND TRUTH)
# ----------------------------
try:
    resp = requests.get(API_MARKED_TODAY, timeout=3).json()
    if resp.get("status") == "success":
        finalized_today = set(resp.get("marked", []))
        print(f"[INFO] Already marked today: {finalized_today}")
except Exception as e:
    print("[WARN] Could not fetch marked list:", e)

# ----------------------------
# BACKEND CALL
# ----------------------------
def send_attendance(name: str):
    try:
        resp = requests.post(
            API_MARK_ATTENDANCE,
            json={"name": name},
            timeout=3
        )
        return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

# ----------------------------
# CHECK SESSION STATUS
# ----------------------------
try:
    status_resp = requests.get(SESSION_STATUS_URL, timeout=3)
    status_data = status_resp.json()

    if not status_data.get("session_open", False):
        reason = status_data.get("holiday_reason") or "Session closed"
        print(f"[INFO] Attendance disabled: {reason}")
        exit(0)

    print(
        f"[INFO] Session active: {status_data['session']} "
        f"({status_data['opens_at']} - {status_data['closes_at']})"
    )

except Exception as e:
    print("[ERROR] Unable to fetch session status:", e)
    exit(1)


# ----------------------------
# START CAMERA
# ----------------------------
cap = cv2.VideoCapture(0)
print("[INFO] Camera started. Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        name = "Unknown"
        color = (0, 0, 255)

        distances = face_recognition.face_distance(KNOWN_ENCODINGS, face_encoding)

        if len(distances) > 0:
            best_idx = np.argmin(distances)

            if distances[best_idx] < CONFIDENCE_THRESHOLD:
                name = KNOWN_NAMES[best_idx]
                color = (0, 255, 0)

                # Ignore finalized people
                if name in finalized_today or name in rejected_today:
                    continue

                # Frame stability
                frame_stability[name] = frame_stability.get(name, 0) + 1

                if frame_stability[name] >= STABLE_FRAMES_REQUIRED:
                    print(f"[INFO] Stable face detected: {name}")

                    result = send_attendance(name)
                    status = result.get("status")

                    if status == "success":
                        print(f"[SUCCESS] {name} marked")
                        finalized_today.add(name)

                    elif status == "already_marked":
                        print(f"[INFO] {name} already marked")
                        finalized_today.add(name)

                    elif status == "rejected":
                        print(f"[REJECTED] {name}: {result.get('message')}")
                        rejected_today.add(name)

                    else:
                        print("[ERROR] Backend error:", result)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Client stopped.")
