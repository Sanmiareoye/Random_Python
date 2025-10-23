import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from draw_landmarks import draw_landmarks_on_image
import cv2
import time

# Store detection results
last_result = None


# Define the callback
def result_callback(result, output_image, timestamp_ms):
    global last_result
    last_result = result


# Create the detector with LIVE_STREAM mode
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
    num_hands=2,
    min_hand_detection_confidence=0.3,
    min_hand_presence_confidence=0.3,
    min_tracking_confidence=0.3,
    result_callback=result_callback,
)
detector = vision.HandLandmarker.create_from_options(options)

# Open webcam
cap = cv2.VideoCapture("6.mov")
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    # frame = cv2.resize(frame, (960, 540))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    timestamp = int((time.time() - start_time) * 1000)

    detector.detect_async(mp_frame, timestamp)

    if last_result and last_result.hand_landmarks:
        annotated = draw_landmarks_on_image(frame, last_result)
        cv2.imshow("Hand Landmarks", annotated)
    else:
        cv2.imshow("Hand Landmarks", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
