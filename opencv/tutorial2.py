import cv2
import random

img = cv2.imread("assets/hands.jpg", -1)

print(img)
print(type(img))
# numpy array
print(img.shape)
# height(rows), width(cols), channels(color space/ how many vals are representing each pixels so bgr, 3 colours)
print(img[257, 400])
# opencv understands bgr(blue, green, red ) but naturally its rgb between 0-255
# for i in range(100):
#     for j in range(img.shape[1]):
#         img[i][j] = [
#             random.randint(0, 255),
#             random.randint(0, 255),
#             random.randint(0, 255),
#         ]

tag = img[715:1015, 136:536]
img[50:350, 300:700] = tag


cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
