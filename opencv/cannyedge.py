import cv2
import numpy as np
from PIL import Image


def cannyEdge(img):
    def callback(x):
        pass

    img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("Canny Edge")
    cv2.createTrackbar("minThres", "Canny Edge", 50, 255, callback)
    cv2.createTrackbar("maxThres", "Canny Edge", 150, 255, callback)

    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        minThres = cv2.getTrackbarPos("minThres", "Canny Edge")
        maxThres = cv2.getTrackbarPos("maxThres", "Canny Edge")

        edges = cv2.Canny(gray, minThres, maxThres)

        cv2.imshow("Canny Edge", edges)

    cv2.destroyAllWindows()


# --- Main Code ---

img = cv2.imread("assets/nails2R.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_skin = np.array([0, 59, 50], dtype=np.uint8)
upper_skin = np.array([25, 173, 255], dtype=np.uint8)

skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
# Invert the skin mask
inverse_mask = cv2.bitwise_not(skin_mask)

# Apply the inverse mask to keep only the non-skin regions
not_skin = cv2.bitwise_and(img, img, mask=inverse_mask)


kernel = np.ones((5, 5), np.uint8)
skin = cv2.morphologyEx(not_skin, cv2.MORPH_OPEN, kernel)

mask_ = Image.fromarray(skin_mask)
bbox = mask_.getbbox()

if bbox is not None:
    x1, y1, x2, y2 = bbox
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 5)

# Call the edge detector on the skin image
cannyEdge(img)

cv2.imshow("Original", img)
cv2.imshow("Skin", skin)
cv2.waitKey(0)
cv2.destroyAllWindows()
