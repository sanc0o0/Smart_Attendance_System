# ============================
# New Face Encoding Script (Old version commented out at the bottom)
# ============================
# This script:
# 1. Reads student images from Dataset/
# 2. Generates face encodings using face_recognition
# 3. Stores encodings safely in a pickle file
# 4. Prevents duplicate encodings on re-runs
# ============================

import cv2                      # OpenCV (not used directly here, kept for consistency)
import face_recognition         # Face detection & encoding library
import os                       # File & directory handling
import pickle                   # Used to store encodings in binary format


# ----------------------------
# CONFIGURATION
# ----------------------------

# Root folder containing all student folders
DATASET_DIR = "Dataset"

# File where face encodings will be stored
ENCODING_FILE = "Encodings/face_encodings.pkl"


print("[INFO] Starting face encoding process...")


# ---------------------------------------------------
# STEP 1: Load existing encodings safely
# ---------------------------------------------------

known_encodings = []
known_names = []

if os.path.exists(ENCODING_FILE):
    print("[INFO] Existing encoding file found. Attempting to load...")

    try:
        with open(ENCODING_FILE, "rb") as file:
            data = pickle.load(file)
            known_encodings = data.get("encodings", [])
            known_names = data.get("names", [])

        print("[INFO] Existing encodings loaded successfully.")

    except EOFError:
        print("[WARNING] Encoding file is empty or corrupted.")
        print("[INFO] Rebuilding encodings from scratch.")

    except Exception as e:
        print(f"[ERROR] Failed to load encoding file: {e}")
        print("[INFO] Rebuilding encodings from scratch.")
else:
    print("[INFO] No encoding file found. Creating new one.")



# Convert known student names to a set for fast lookup
# This helps us skip already-encoded students
encoded_students = set(known_names)


# ---------------------------------------------------
# STEP 2: Scan Dataset directory
# ---------------------------------------------------
# Dataset structure expected:
#
# Dataset/
# ├── Student1/
# │   └── image1.jpg
# ├── Student2/
# │   └── image1.jpg
# └── Student3/
#     └── image1.jpg
# ---------------------------------------------------

print("[INFO] Scanning dataset folder...")

# List all folders inside Dataset/
student_folders = os.listdir(DATASET_DIR)

# Counter to track how many new faces are added
new_encodings_count = 0


for student in student_folders:
    student_path = os.path.join(DATASET_DIR, student)

    # Skip if it's not a directory
    if not os.path.isdir(student_path):
        continue

    # Skip students that are already encoded
    if student in encoded_students:
        print(f"[SKIP] {student} already encoded")
        continue

    print(f"\n[INFO] Processing new student: {student}")

    # Process all images inside the student's folder
    for image_name in os.listdir(student_path):
        image_path = os.path.join(student_path, image_name)

        print(f"   → Loading image: {image_name}")

        # Load image into numpy array (RGB)
        image = face_recognition.load_image_file(image_path)

        # Extract face encodings from image
        encodings = face_recognition.face_encodings(image)

        # If no face detected, skip the image
        if len(encodings) == 0:
            print("     ❌ No face detected, skipping image")
            continue

        # Store the first detected face encoding
        known_encodings.append(encodings[0])
        known_names.append(student)

        new_encodings_count += 1
        print("     ✅ Face encoded successfully")


# ---------------------------------------------------
# STEP 3: Save encodings to disk
# ---------------------------------------------------
# Encodings are saved as a dictionary:
# {
#     "encodings": [...],
#     "names": [...]
# }

print("\n[INFO] Saving encodings to file...")

with open(ENCODING_FILE, "wb") as file:
    pickle.dump(
        {
            "encodings": known_encodings,
            "names": known_names
        },
        file
    )

# ---------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------

print("[SUCCESS] Encoding update completed!")
print(f"[INFO] New faces added: {new_encodings_count}")
print(f"[INFO] Total faces stored: {len(known_encodings)}")
print(f"[INFO] Encoding file location: {ENCODING_FILE}")



#//////////////////////////////////////////////////////////////////////////////////////////////////////////
# This is the old version of the code before optimization to avoid re-encoding existing students.
#//////////////////////////////////////////////////////////////////////////////////////////////////////////

# """
# Every time new image or student is added → re-run encode_faces.py
# """
# import cv2
# import face_recognition
# import os
# import pickle

# # -----------------------------
# # PATH CONFIGURATION
# # -----------------------------
# DATASET_DIR = "Dataset"              # Folder containing student subfolders
# ENCODINGS_DIR = "Encodings"
# ENCODING_FILE = os.path.join(ENCODINGS_DIR, "face_encodings.pkl")

# # -----------------------------
# # STORAGE LISTS
# # -----------------------------
# known_encodings = []   # Will store 128-D face vectors
# known_names = []       # Will store corresponding student names

# print("[INFO] Starting face encoding process...")
# print("[INFO] Scanning dataset folder...\n")

# # -----------------------------
# # LOOP THROUGH EACH STUDENT
# # -----------------------------
# for student_name in os.listdir(DATASET_DIR):
#     student_path = os.path.join(DATASET_DIR, student_name)

#     # Skip if not a folder
#     if not os.path.isdir(student_path):
#         continue

#     print(f"[INFO] Processing student: {student_name}")

#     # -----------------------------
#     # LOOP THROUGH IMAGES OF STUDENT
#     # -----------------------------
#     for image_name in os.listdir(student_path):
#         image_path = os.path.join(student_path, image_name)

#         print(f"   → Loading image: {image_name}")

#         # Load image
#         image = face_recognition.load_image_file(image_path)

#         # Extract face encodings
#         encodings = face_recognition.face_encodings(image)

#         # Check if a face was detected
#         if len(encodings) == 0:
#             print("     ❌ No face detected, skipping image")
#             continue

#         # Take the first detected face encoding
#         face_encoding = encodings[0]

#         # Store encoding and name
#         known_encodings.append(face_encoding)
#         known_names.append(student_name)

#         print("     ✅ Face encoded successfully")

#     print()  # Blank line for readability

# # -----------------------------
# # SAVE ENCODINGS TO FILE
# # -----------------------------
# print("[INFO] Saving encodings to file...")

# os.makedirs(ENCODINGS_DIR, exist_ok=True)

# data = {
#     "encodings": known_encodings,
#     "names": known_names
# }

# with open(ENCODING_FILE, "wb") as f:
#     pickle.dump(data, f)

# print("[SUCCESS] Face encodings saved successfully!")
# print(f"[INFO] Total faces encoded: {len(known_encodings)}")
# print(f"[INFO] Encoding file location: {ENCODING_FILE}")


