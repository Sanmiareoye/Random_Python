import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from draw_landmarks import draw_landmarks_on_image
import cv2

# STEP 1: Create the hand landmarker
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
detector = vision.HandLandmarker.create_from_options(options)

# STEP 2: Load the video
video_path = "7.mp4"
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

# Timestamp (in milliseconds)
frame_index = 0

# STEP 3: Loop through frames
while cap.isOpened():
    ret, frame = cap.read()
    # print("CAP FRAME: ", cap.read())
    if not ret:
        break

    # target_size = (960, 540)  # or whatever size worked best for your images

    # frame = cv2.resize(frame, target_size)

    # Convert to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create MediaPipe Image
    mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    # Compute timestamp in milliseconds
    timestamp = int((frame_index / fps) * 1000)

    # Detect hands in video mode
    detection_result = detector.detect_for_video(mp_frame, timestamp)

    # Draw if landmarks detected
    if detection_result.hand_landmarks:
        bgr_annotated = draw_landmarks_on_image(frame, detection_result)
        cv2.imshow("Hand Landmarks", bgr_annotated)
    else:
        cv2.imshow("Hand Landmarks", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frame_index += 1

# Cleanup
cap.release()
cv2.destroyAllWindows()
