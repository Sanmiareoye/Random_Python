import cv2

img = cv2.imread("assets/hands.JPG", 1)
img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)
img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

# create a file with the new image
cv2.imwrite("new_img.jpg", img)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
