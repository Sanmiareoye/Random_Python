# Corner detection --> Shi Tomasi Corner Dector and good features to track
import numpy as np
import cv2

img = cv2.imread("assets/chessboard.jpg")
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
# these algorithms use greyscale because they detect corners and edges easier than bgr or rgb images
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# src image, no of best corners, confidence/ qualty of corners, min euclidean dist(dist between 2 corners)
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = corners.astype(int)

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
    # ravel flattens the array so [[244, 244]] -> [244,244] or [[2,1], [1,2]] -> [2,1,1,2]

for i in range(len(corners)):
    for j in range(i + 1, len(corners)):
        corner1 = tuple(corners[i][0])
        corner2 = tuple(corners[j][0])
        print(corner1, corner2)
        color = tuple(int(x) for x in np.random.randint(0, 255, size=3))
        print(color)
        cv2.line(img, corner1, corner2, color, 1)

cv2.imshow("Frame", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
