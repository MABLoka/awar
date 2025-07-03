import os
import random
import shutil
from ultralytics import YOLO
import yaml

image_dir = 'dataset/images'
label_dir = 'dataset/labels'
yaml_path = 'dataset/data.yaml'

def frz(label_dir, image_dir, output_dir, target_class_id=0, train_ratio=0.8):
    # Ensure consistent randomness
    random.seed(42)

    # Collect files that contain the target class_id
    matching_files = []
    print(os.listdir(label_dir))
    for file_name in os.listdir(label_dir):
        if file_name.endswith(".txt"):
            full_path = os.path.join(label_dir, file_name)
            with open(full_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip().startswith(str(target_class_id)):
                        print(f"Matched file: {file_name}")
                        matching_files.append(file_name)
                        break
    print(f"Total matched files: {len(matching_files)}")
    # Shuffle and split
    random.shuffle(matching_files)
    split_index = int(len(matching_files) * train_ratio)
    print(split_index)
    train_files = matching_files[:split_index]
    val_files = matching_files[split_index:]

    def move_files(file_list, split_type):
        for label_file in file_list:
            img_file = label_file.replace(".txt", ".jpg")
            
            # Source paths
            label_src = os.path.join(label_dir, label_file)
            img_src = os.path.join(image_dir, img_file)

            # Destination paths
            label_dst_dir = os.path.join(output_dir, "labels", split_type)
            img_dst_dir = os.path.join(output_dir, "images", split_type)
            os.makedirs(label_dst_dir, exist_ok=True)
            os.makedirs(img_dst_dir, exist_ok=True)

            shutil.copy(label_src, os.path.join(label_dst_dir, label_file))
            if os.path.exists(img_src):
                shutil.copy(img_src, os.path.join(img_dst_dir, img_file))
            else:
                print(f"Warning: Missing image for {label_file}")

    move_files(train_files, "train")
    move_files(val_files, "val")

    print(f"Split complete: {len(train_files)} train, {len(val_files)} val for class ID {target_class_id}")

def has_files_only(path):
    return any(
        os.path.isfile(os.path.join(path, entry))
        for entry in os.listdir(path)
    )

if has_files_only("dataset/images") and has_files_only("dataset/labels"):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file) or {}
    classes_no = data['nc']

    for i in range(0, classes_no):
        frz(
        label_dir=label_dir, 
        image_dir=image_dir, 
        output_dir="dataset",
        target_class_id=i
        )
        
# Load a model (YOLOv8n, YOLOv8s, YOLOv8m, YOLOv8l, or YOLOv8x)
model = YOLO("yolov8n.pt")  # You can use a larger model if needed

# Train the model
model.train(
    data='dataset/data.yaml',
    epochs=50,
    project='runs/detect',  # Path to save under
    name='train',           # Folder name
    exist_ok=True           # Overwrite if it exists
)

shutil.copy("runs/detect/train9/weights/best.pt", "model/my_model.pt")
