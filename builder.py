import cv2
import time
import pickle
import numpy as np
from itertools import combinations
import threading


# --- Configuration ---
output_filename = 'recorded_video.avi'
target_fps = 20   # Desired frames per second for the output video
recording_duration_seconds = 10 # Desired recording duration in seconds
333333
# For webcam:
cap = cv2.VideoCapture(0) # 0 for default webcam, 1 for external, etc.

# Request Full HD resolution (1920x1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# Get frame dimensions from the camera
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# --- Initialize VideoWriter ---
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Codec for .avi files
out = cv2.VideoWriter(output_filename, fourcc, target_fps, (frame_width, frame_height))

# --- Record Video ---
start_time = time.time()
frames_recorded = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame.")
        break

    # Write the frame to the output video file
    out.write(frame)
    frames_recorded += 1

    # Display the live feed (optional)
    cv2.imshow('Live Feed', frame)

    # Check if recording duration or frame count is met
    elapsed_time = time.time() - start_time
    if elapsed_time >= recording_duration_seconds:
        print(f"Recording finished after {recording_duration_seconds} seconds.")
        break

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Recording stopped by user.")
        break

# --- Release Resources ---
cap.release()
out.release()
cv2.destroyAllWindows()
