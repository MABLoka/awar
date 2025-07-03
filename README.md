## Object Labeling and Training Pipeline with YOLOv8

This project provides a complete pipeline for building custom object detection datasets and training YOLOv8 models using your webcam and a simple GUI-based labeling tool. It's ideal for quickly capturing, labeling, and training on real-world image data for computer vision tasks.

### Components

#### 1. `builder.py` — **Video Capture Utility**

Captures video directly from your webcam in Full HD resolution and saves it as `recorded_video.avi`. Adjustable settings include:

* Frame rate
* Recording duration
* Resolution

#### 2. `labeler.py` — **Interactive Image Labeling Tool**

A Tkinter-based GUI tool that allows you to:

* Load frames from a recorded video
* Navigate between frames
* Draw bounding boxes
* Assign text labels to objects
* Save images and corresponding YOLO-format label files
* Auto-manage class IDs using a `data.yaml` file

#### 3. `model.py` — **Dataset Preprocessing and YOLOv8 Training**

Automatically:

* Scans labeled data for each class
* Splits it into training and validation sets
* Trains a YOLOv8 model on the generated dataset
* Saves the best model weights as `model/my_model.pt`

### Project Structure

```
dataset/
├── images/
├── labels/
└── data.yaml
model/
└── my_model.pt
runs/
└── detect/train/...
```

### Requirements

* Python 3.8+
* OpenCV
* Tkinter (for GUI)
* `ultralytics` (YOLOv8)
* Pillow
* PyYAML

Install requirements via:

```bash
pip install -r requirements.txt
```

### Usage

1. **Record video**

   ```bash
   python builder.py
   ```

2. **Label video frames**

   ```bash
   python labeler.py
   ```

3. **Train the model**

   ```bash
   python model.py
   ```
