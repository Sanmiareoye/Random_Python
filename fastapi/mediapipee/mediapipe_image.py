import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from draw_landmarks import draw_landmarks_on_image
import cv2
import matplotlib.pyplot as plt

from PIL import Image

# STEP 2: Create an HandLandmarker object.
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
detector = vision.HandLandmarker.create_from_options(options)

# STEP 3: Load the input image.
img = Image.open("7.heic")
img_resized = img.resize((634, 846))
img_resized.save("your_resized.jpg")
image = mp.Image.create_from_file("your_resized.jpg")

# STEP 4: Detect hand landmarks from the input image.
detection_result = detector.detect(image)
print(detection_result.hand_landmarks)
print(detection_result.handedness)

# STEP 5: Process the classification result. In this case, visualize it.
if detection_result.hand_landmarks:
    # Convert MediaPipe RGB image to BGR for drawing
    bgr_image = cv2.cvtColor(image.numpy_view(), cv2.COLOR_RGB2BGR)

    # Draw landmarks on the BGR image
    annotated_image = draw_landmarks_on_image(bgr_image, detection_result)

    # Display the result
    cv2.imshow("Hand Landmarks", annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No hands detected in the image.")
