## YOLOv8 Object Detection Pipeline: Capture → Label → Train → Detect

This project offers a full workflow for developing custom YOLOv8 object detection models from scratch using webcam input. You can record video, label frames with a GUI tool, train a YOLOv8 model, and run live inference — all with minimal setup.

---

### Features

* **Video Recording** with webcam in Full HD
* **Manual Image Labeling** via intuitive GUI
* **Model Training** using YOLOv8 with class-wise dataset splitting
* **Real-Time Inference** with the trained model on webcam feed

---

### Components

#### `builder.py` — **Video Recorder**

* Captures video from the webcam and saves it as `recorded_video.avi`
* Resolution and duration are configurable

#### `labeler.py` — **Labeling Interface**

* Frame-by-frame video labeling using a Tkinter GUI
* Draw bounding boxes and enter class labels
* Saves YOLO-format annotations and updates `data.yaml` automatically

#### `model.py` — **Trainer**

* Scans and splits data by class
* Trains YOLOv8 on the labeled dataset
* Saves the trained model to `model/my_model.pt`

#### `use.py` — **Live Detection**

* Loads the trained model
* Runs real-time object detection on webcam input
* Displays annotated frames with bounding boxes and class labels

---

### Directory Layout

```
dataset/
├── images/           # Saved image frames
├── labels/           # YOLO format label files
└── data.yaml         # Class definitions and metadata

model/
└── my_model.pt       # Trained YOLOv8 weights

runs/
└── detect/train/...  # YOLOv8 training logs and checkpoints
```

---

### Requirements

```bash
pip install opencv-python pillow pyyaml ultralytics
```

---

### Usage

#### 1. Record Video

```bash
python builder.py
```

#### 2. Label Frames

```bash
python labeler.py
```

#### 3. Train YOLOv8 Model

```bash
python model.py
```

#### 4. Run Live Inference

```bash
python use.py
```

---

### Notes

* Ensure you label at least a few samples per class before training.
* You can modify YOLO model type (`yolov8n`, `yolov8s`, etc.) in `model.py` if needed.
* The project saves images using SHA-256 hash of image content and bounding box, ensuring uniqueness.

