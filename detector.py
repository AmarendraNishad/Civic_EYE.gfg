from ultralytics import YOLO
import cv2

MODEL_PATH = "models/yolov8n.pt"
VIDEO_PATH = "videos/traffic.mp4"

# Load YOLOv8 Nano
model = YOLO(MODEL_PATH)

# Open traffic video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open traffic video.")
    exit()

print("CivicEye started...")
print("Press Q to stop.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detect + track vehicles
    results = model.track(
        frame,
        persist=True,
        classes=[2, 3, 5, 7],
        tracker="bytetrack.yaml",
        verbose=False
    )

    # Draw detections
    annotated_frame = results[0].plot()

    cv2.imshow("CivicEye - Vehicle Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("CivicEye stopped.")