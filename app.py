import cv2
import time
import numpy as np
import os

from ultralytics import YOLO
from incident_logger import log_incident


# =========================================================
# CIVICEYE CONFIGURATION
# =========================================================

MODEL_PATH = "models/yolov8n.pt"
VIDEO_PATH = "videos/traffic.mp4"

THRESHOLD_SECONDS = 5.0

# Create incident folder
os.makedirs("incidents", exist_ok=True)


# =========================================================
# LOAD YOLO MODEL
# =========================================================

print("Loading YOLOv8n...")

model = YOLO(MODEL_PATH)

print("YOLOv8n loaded successfully.")


# =========================================================
# OPEN VIDEO
# =========================================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():

    print("ERROR: Could not open traffic video.")
    print(f"Check this path: {VIDEO_PATH}")

    exit()


print("CivicEye started.")
print("Press Q to stop.")


# =========================================================
# EMERGENCY CORRIDOR
# =========================================================

EMERGENCY_ZONE = np.array([
    [100, 300],
    [500, 300],
    [600, 600],
    [50, 600]
], np.int32)


# =========================================================
# TRACKING DATA
# =========================================================

# Vehicle ID → time when it entered zone
vehicle_timers = {}

# Vehicles for which alert has already been generated
alerted_vehicles = set()


# =========================================================
# MAIN VIDEO LOOP
# =========================================================

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:

        print("Video finished.")
        break


    # =====================================================
    # YOLO DETECTION + TRACKING
    # =====================================================

    results = model.track(
        frame,
        persist=True,
        classes=[2, 3, 5, 7],
        tracker="bytetrack.yaml",
        verbose=False
    )


    # =====================================================
    # DRAW EMERGENCY ZONE
    # =====================================================

    overlay = frame.copy()

    cv2.polylines(
        overlay,
        [EMERGENCY_ZONE],
        isClosed=True,
        color=(0, 255, 255),
        thickness=3
    )

    cv2.fillPoly(
        overlay,
        [EMERGENCY_ZONE],
        color=(0, 255, 255)
    )

    cv2.addWeighted(
        overlay,
        0.20,
        frame,
        0.80,
        0,
        frame
    )


    # Zone label

    cv2.putText(
        frame,
        "EMERGENCY CORRIDOR",
        (100, 290),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )


    # =====================================================
    # PROCESS VEHICLES
    # =====================================================

    if (
        results[0].boxes is not None
        and results[0].boxes.id is not None
    ):

        boxes = (
            results[0]
            .boxes
            .xyxy
            .cpu()
            .numpy()
        )

        track_ids = (
            results[0]
            .boxes
            .id
            .int()
            .cpu()
            .numpy()
        )


        current_frame_ids = set()


        # =================================================
        # PROCESS EACH VEHICLE
        # =================================================

        for box, track_id in zip(
            boxes,
            track_ids
        ):

            x1, y1, x2, y2 = map(
                int,
                box
            )


            # Bottom-center of vehicle

            center_point = (
                int((x1 + x2) / 2),
                int(y2)
            )
                     