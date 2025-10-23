import cv2
import numpy as np
from PIL import Image

img = cv2.imread("assets/1.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_skin = np.array([0, 59, 50], dtype=np.uint8)
upper_skin = np.array([25, 173, 255], dtype=np.uint8)

skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
skin = cv2.bitwise_and(img, img, mask=skin_mask)

kernel = np.ones((5, 5), np.uint8)
skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, kernel)

mask_ = Image.fromarray(skin_mask)
bbox = mask_.getbbox()

if bbox is not None:
    x1, y1, x2, y2 = bbox

    img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
cv2.imshow("Original", img)
cv2.imshow("Skin", skin)
cv2.waitKey(0)
cv2.destroyAllWindows()
