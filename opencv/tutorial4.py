import numpy as np
import cv2

# capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))  # 3 represents width
    height = int(cap.get(4))  # 4 represents width

    img = cv2.line(frame, (0, 0), (width, height), (255, 0, 0), 10)
    # line --> frame, start, end, color, thickness
    img = cv2.line(frame, (width, 0), (0, height), (255, 0, 0), 10)
    # rectangle --> frame, topleft of rectangle, bottonright of rectangle, color, thickness
    img = cv2.rectangle(img, (100, 100), (200, 200), (128, 128, 128), 5)
    # circle --> frame/source image, centre pos, radius, thickness (-1 to fill)
    img = cv2.circle(img, (300, 300), 60, (0, 0, 255), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    # text --> frame, text, from bottomleft hand corner, font, font scale, colour, thickness, line type
    img = cv2.putText(
        img, "Sanmi is Great!", (10, height - 10), font, 5, (0, 0, 0), 5, cv2.LINE_AA
    )
    cv2.imshow("frame", img)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
