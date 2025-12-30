import cv2
import requests
from datetime import datetime
import face_recognition
import pickle
import numpy as np
import os
from datetime import datetime

# ----------------------------
# BACKEND API CONFIG
# ----------------------------
API_URL = "http://127.0.0.1:8000/mark-attendance"

# ----------------------------
# CONFIGURATION
# ----------------------------
ENCODING_FILE = "Encodings/face_encodings.pkl"
ATTENDANCE_DIR = "Attendance"
CONFIDENCE_THRESHOLD = 0.6

os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Create today's attendance file
today_date = datetime.now().strftime("%Y-%m-%d")
attendance_file = f"{ATTENDANCE_DIR}/attendance_{today_date}.csv"

# ----------------------------
# LOAD FACE ENCODINGS
# ----------------------------
print("[INFO] Loading face encodings...")

with open(ENCODING_FILE, "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

print(f"[INFO] Total known faces: {len(known_encodings)}")

# ----------------------------
# LOAD ATTENDANCE (IF EXISTS)
# ----------------------------
marked_students = set()

if os.path.exists(attendance_file):
    with open(attendance_file, "r") as f:
        for line in f.readlines()[1:]:
            marked_students.add(line.split(",")[0])

# ----------------------------
# START CAMERA
# ----------------------------
cap = cv2.VideoCapture(0)
print("[INFO] Camera started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB for face_recognition
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations & encodings
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        name = "Unknown"
        color = (0, 0, 255)

        distances = face_recognition.face_distance(known_encodings, face_encoding)

        if len(distances) > 0:
            best_match_index = np.argmin(distances)

            if distances[best_match_index] < CONFIDENCE_THRESHOLD:
                name = known_names[best_match_index]
                color = (0, 255, 0)

                # Mark attendance if not already marked
                if name not in marked_students:

                    payload = {
                        "name": name,
                        "timestamp": datetime.now().isoformat()
                    }

                    try:
                        response = requests.post(API_URL, json=payload)
                        result = response.json()

                        status = result.get("status")
                        detail = result.get("detail", "").lower()

                        if status == "success":
                            print(f"[ATTENDANCE] {name} marked successfully")
                            marked_students.add(name)

                        elif status == "already_marked" or "already marked" in detail:
                            print(f"[INFO] {name} already marked today")
                            marked_students.add(name)

                        else:
                            print(f"[ERROR] Unexpected backend response: {result}")



                    except KeyError as e:
                        print("[ERROR] Backend response missing key:", e, result)

                    except Exception as e:
                        print("[ERROR] Attendance processing failed:", e)



        # Draw face box & name``
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] System stopped.")
