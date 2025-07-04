import cv2
from ultralytics import YOLO
import tkinter as tk
from threading import Thread

# --- Global control flag ---
running = False
cap = None

# Load YOLO model
model = YOLO("runs/detect/train/weights/best.pt")  # Adjust the path as needed

def start_detection():
    global running, cap
    if running:
        return  # Already running
    running = True
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        running = False
        return

    detection_thread = Thread(target=run_detection)
    detection_thread.start()

def run_detection():
    global running, cap

    while running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference
        results = model(frame)

        # Draw boxes
        annotated_frame = results[0].plot()

        # Show in OpenCV window
        cv2.imshow("YOLOv8 Live Detection", annotated_frame)

        # Exit if user presses 'q' or ESC
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord('q')):
            stop_detection()
            break

    if cap:
        cap.release()
    cv2.destroyAllWindows()

def stop_detection():
    global running
    running = False

# --- tkinter GUI ---
root = tk.Tk()
root.title("YOLOv8 Live Detection")

start_button = tk.Button(root, text="Start Detection", command=start_detection)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=lambda: (stop_detection(), root.quit()))
exit_button.pack(pady=10)

root.mainloop()
