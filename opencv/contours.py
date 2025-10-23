import cv2
import numpy as np

img_path = "assets/hands_no_bg.png"
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

# define the upper and lower boundaries of the HSV pixel intensities
# to be considered 'skin'
hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 59, 50], dtype="uint8")
upper = np.array([25, 173, 255], dtype="uint8")
skinMask = cv2.inRange(hsvim, lower, upper)

# blur the mask to help remove noise
skinMask = cv2.blur(skinMask, (2, 2))

# get threshold image
ret, thresh = cv2.threshold(skinMask, 100, 255, cv2.THRESH_BINARY)

# INVERT the mask to get NON-skin regions
non_skin = cv2.bitwise_not(thresh)

# Optional: Visualize the non-skin mask
cv2.imshow("Non-skin Mask", non_skin)

# draw the contours on the empty image
contours, hierarchy = cv2.findContours(non_skin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = max(contours, key=lambda x: cv2.contourArea(x))
cv2.drawContours(img, [contours], -1, (255, 255, 0), 5)
cv2.imshow("contours", img)

cv2.waitKey()
