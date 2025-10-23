import numpy as np
import cv2

# capture
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y : y + w, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

        for ex, ey, ew, eh in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

    # scale factor -> lower number is more accurate but slower and higher is oposite, good val 1.05
    # minneighbors ->  how many neighbors each candidate has to retain higher value less detection with higher quailty good start is 3-6
    # optional:
    # minsize of face
    # maxsize  of face
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
