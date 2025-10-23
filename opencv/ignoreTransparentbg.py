import cv2
import numpy as np

# Load image with alpha channel
image = cv2.imread("assets/hands_no_bg.png", cv2.IMREAD_UNCHANGED)

# Extract the alpha channel (transparency mask)
b, g, r, alpha = cv2.split(image)

# Create a mask where transparent pixels are ignored
hand_mask = alpha > 0

# Find hand contours
hand_contours, _ = cv2.findContours(
    hand_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# Create image for drawing contours
contour_image = image[:, :, :3].copy()

# Draw hand contours in green
cv2.drawContours(contour_image, hand_contours, -1, (0, 255, 0), 2)
print(f"Found {len(hand_contours)} hand contour(s)")

# Convert to HSV for skin detection
hsvim = cv2.cvtColor(contour_image, cv2.COLOR_BGR2HSV)

# Define HSV boundaries for skin detection
lower = np.array([0, 59, 50], dtype="uint8")
upper = np.array([25, 173, 255], dtype="uint8")
skin_mask = cv2.inRange(hsvim, lower, upper)

# Blur the mask to reduce noise
skin_mask = cv2.blur(skin_mask, (2, 2))

# Threshold the skin mask
ret, thresh = cv2.threshold(skin_mask, 100, 255, cv2.THRESH_BINARY)

# Invert to get non-skin regions (nails)
non_skin = cv2.bitwise_not(thresh)

# Only consider non-skin pixels inside the hand
non_skin_in_hand = cv2.bitwise_and(non_skin, non_skin, mask=hand_mask.astype(np.uint8))

# Find nail contours
nail_contours_raw, hierarchy = cv2.findContours(
    non_skin_in_hand, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
)

# Filter out small noise contours
nail_contours = [c for c in nail_contours_raw if cv2.contourArea(c) > 1500]

# Draw nail contours in yellow
cv2.drawContours(contour_image, nail_contours, -1, (255, 255, 0), 2)
print(f"Found {len(nail_contours)} nail(s)")

cv2.imshow("1. Original", image)
cv2.imshow("2. Hand Mask", (hand_mask * 255).astype(np.uint8))
cv2.imshow("3. Final Result", contour_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
