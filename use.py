import cv2
from ultralytics import YOLO

# Load your trained model
model = YOLO("runs/detect/train/weights/best.pt")

# model = YOLO("yolov8n.pt")
# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference (pass frame as numpy array)
    results = model(frame)

    # results[0].plot() returns an image with boxes drawn
    annotated_frame = results[0].plot()

    # Show frame
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    # Exit on ESC or 'q' key
    if cv2.waitKey(1) & 0xFF in (27, ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
