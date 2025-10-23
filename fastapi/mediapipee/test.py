import cv2
import matplotlib.pyplot as plt

# Replace 'your_image.jpg' with your actual file name
img = cv2.imread("1.jpg")

# Convert from BGR (OpenCV default) to RGB for correct colors in matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Display the image
plt.imshow(img_rgb)
plt.axis("on")  # Optional: hides the axis
plt.show()
