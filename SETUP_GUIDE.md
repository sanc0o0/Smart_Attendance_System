# Camera Setup & Alignment Guide

(Face Recognition Attendance System)

This system relies on a local camera device connected to the machine running the OpenCV client.
Correct camera placement and configuration is critical for reliable face detection and accurate attendance marking.

## 1.  Camera Requirements
- Minimum recommended specs
- Resolution: 720p (1280×720) or higher
- Frame rate: 25–30 FPS

### Type:

- USB webcam (Logitech / HP / Lenovo – works fine)
- Laptop built-in camera (acceptable for small rooms)
- IP camera ❌ (not supported directly without modification)

⚠️ The current system is designed for direct camera access via OpenCV, not RTSP streams.

## 2. Physical Placement (Most Important Part)
### 📐 Camera height

- Place the camera at face level
- Ideal height: 4.5–5.5 feet (1.4–1.7 m) from the ground

### 📏 Distance from subjects

- Optimal distance: 1.5 – 3 meters
- Faces should occupy at least 20–25% of the frame

### 🧭 Angle

- Camera should be straight-on

### Avoid:

- Extreme top-down angles
- Side angles beyond 15–20°

✅ **Best setup**: Camera mounted on a wall or tripod facing students directly.

## 3. Lighting Conditions

### Face recognition accuracy depends heavily on lighting.

### Recommended lighting:

- Uniform indoor lighting
- Light source in front of the face
- Consistent brightness across the room

### Avoid

- Strong backlight (windows behind students)

- Harsh shadows

- Flickering or colored lights

### 💡 Tip: If faces look dark or washed out on the camera preview, recognition accuracy will drop.

## 4. Camera Device Configuration (System Level)
**🔍 Identify camera index**

If multiple cameras are connected, OpenCV may not use the correct one by default.

In 
```
capture_faces.py
``` 
or 
```
recognize_attendance.py
```

cv2.VideoCapture(0)


Try:

cv2.VideoCapture(1)
cv2.VideoCapture(2)


Use the index that shows the correct video feed.

## 🖥️ OS Permissions
```
Ensure camera access is allowed:

Windows:
Settings → Privacy → Camera → Allow desktop apps

Linux:
Ensure /dev/video0 exists and permissions are correct

macOS:
Grant terminal / Python camera access
```
## 5. Face Capture (Dataset Creation)

Before recognition can work, faces must be registered.

### Steps:

- Admin logs in via frontend dashboard
- Use the face capture script
- Capture 15–25 images per student

### Vary:

- Slight head movement
- Expressions
- Glasses (if worn daily)

📁 Captured images are stored in:

```dataset_/student_name/```


❗ Poor-quality face data = poor recognition later.

## 6. Encoding Faces

After capturing faces:

```
python encode_faces.py
```


This:

- Converts face images into numerical encodings
- Stores them in the encodings_ directory
- Makes them available for real-time recognition

**⚠️ This step must be repeated every time new faces are added.**

## 7. Real-Time Attendance Recognition
### Preconditions:
 - Backend must be running
- Admin session must be ACTIVE
- Encodings must exist

Run:

```
python recognize_attendance.py
```


### What happens:

- Camera opens
- Faces are detected live
- Known faces are matched
- Attendance is marked once per session
- Duplicate entries are blocked automatically

## 8. Admin Session Control (Critical)

**Attendance marking depends on session state.**

### Flow ↓

- Admin logs in (Next.js dashboard)
- Starts a session (time based sessions)
- Recognition client checks session status via API
- Attendance is accepted only if session is active
- Admin ends session → marking stops

### This prevents:

- Proxy attendance
- Accidental duplicate entries
- Out-of-session marking

## 9. Common Real-World Issues & Fixes

### ❌ Faces not detected

- Increase lighting
- Move camera closer
- Check camera index

### ❌ Wrong person detected

- Improve dataset quality
- Re-capture face images
- Avoid group crowding in front of camera

### ❌ Attendance not marking

- Ensure admin session is active
- Backend URL is reachable
- Internet connection is stable

## 🔐 Security & Privacy Notes

- Face data is stored locally, not in browser

- No student login credentials exist

- Only admins authenticate

- Attendance logic is server-controlled

**This design minimizes attack surface while keeping the system usable in real environments.**

## ✅ Recommended Real-Life Use Cases

- Classrooms

- Labs

- Training centers

- Office entry attendance

- Controlled-access rooms