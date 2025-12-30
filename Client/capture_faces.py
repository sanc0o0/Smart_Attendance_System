import cv2

face_cascade = cv2.CascadeClassifier("External_Libraries/haarcascade_frontalface_default.xml")


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detect_faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5)
    

    for (x, y, w, h) in detect_faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1) 
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        
        if len(detect_faces) > 0:
            cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
        

    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
cap.release()
cv2.destroyAllWindows()