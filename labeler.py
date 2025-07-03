import cv2
from tkinter import *
from PIL import ImageTk, Image, ImageGrab
import hashlib
import io
import os
import yaml

image_dir = 'dataset/images'
label_dir = 'dataset/labels'
yaml_path = 'dataset/data.yaml'

class Labeler():

    def __init__(self):

        self.rect_id = None  # no global needed
        self.start_x = None
        self.start_y = None
        self.img_no = 1
        # Load Video
        self.cap = cap = cv2.VideoCapture("recorded_video.avi")

        # Calling the Tk (The initial constructor of tkinter)
        self.root = Tk()
        self.canvas = Canvas(self.root)
        self.canvas.grid(row=1, column=0, columnspan=3)
        # We will make the title of our app as Image Viewer
        self.root.title("Image Viewer")

        # The geometry of the box which will be displayed
        # on the screen
        self.root.geometry("1200x1200")


        # Check if the video opened successfully
        if not self.cap.isOpened():
            print("Error: Cannot open video file")
            exit()

        # Init the frame list
        self.frames = []


        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self.frames.append(frame)

        self.cap.release()

        # OpenCV frames to PIL images
        self.pil_images = []
        for frame in self.frames:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            self.pil_images.append(Image.fromarray(frame_rgb))                  # Convert to PIL Image
                    
        # Convert to Tk-compatible image
        # List of the images so that we traverse the list
        self.List_images = []
        for pil_image in self.pil_images:
            self.List_images.append(ImageTk.PhotoImage(pil_image))


        # Set canvas
        image = self.List_images[0]
        self.canvas.create_image(0, 0, image=image, anchor=NW)
        self.canvas.config(width=image.width(), height=image.height()) 

        # We will have three button back ,forward and exit
        self.button_back = Button(self.root, text="Back", command=self.back,
                            state=DISABLED)

        # root.quit for closing the app
        self.button_exit = Button(self.root, text="Exit",
                            command=self.root.quit)

        self.button_forward = Button(self.root, text="Forward",
                                command=lambda: self.forward())
        # Create text widget and specify size.
        self.text_box = Text(self.root, height = 5, width = 52)
        
        # Button to save labeled image 
        self.button_label = Button(self.root, text="Label",
                            command=self.on_button_label)

        # Label to show image number
        self.label = Label(self.root, text=f"{self.img_no}/{len(self.pil_images)}")
        

        # grid function is for placing the buttons in the frame
        self.button_back.grid(row=5, column=0)
        self.button_exit.grid(row=5, column=1)
        self.button_forward.grid(row=5, column=2)
        self.text_box.grid(row=7, column=0)
        self.button_label.grid(row=7, column=1)
        self.label.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Set frame to be labeled
        self.im2 = ''

    def forward(self):
        self.img_no = self.img_no + 1
        self.canvas.grid_forget()

        image = self.List_images[self.img_no]

        # Reset canvas
        self.canvas.create_image(0, 0, image=image, anchor=NW)
        self.canvas.config(width=image.width(), height=image.height())

        self.button_forward = Button(self.root, text="forward",
                            command=lambda: self.forward())
        
        # img_no+1 as we want the next image to pop up
        if self.img_no == self.List_images.__len__:
            self.button_forward = Button(self.root, text="Forward",
                                    state=DISABLED)

        # img_no-1 as we want previous image when we click
        # back button
        self.button_back = Button(self.root, text="Back",
                            command=lambda: self.back())

        # Placing the button in new grid
        self.canvas.grid(row=1, column=0, columnspan=3)
        self.button_back.grid(row=5, column=0)
        self.button_exit.grid(row=5, column=1)
        self.button_forward.grid(row=5, column=2)

        self.label.config(text=f"{self.img_no}/{len(self.pil_images)}")
        self.label.grid(row=0, column=0, columnspan=3)

    def back(self):
        self.img_no = self.img_no - 1
        self.canvas.grid_forget()

        image = self.List_images[self.img_no]

        # Reset canvas
        self.canvas.create_image(0, 0, image=image, anchor=NW)
        self.canvas.config(width=image.width(), height=image.height()) 

        self.button_forward = Button(self.root, text="forward",
                                command=lambda: self.forward())
        self.button_back = Button(self.root, text="Back",
                            command=lambda: self.back())

        if self.img_no == 1:
            self.button_back = Button(self.root, text="Back", state=DISABLED)

        self.canvas.grid(row=1, column=0, columnspan=3)
        self.button_back.grid(row=5, column=0)
        self.button_exit.grid(row=5, column=1)
        self.button_forward.grid(row=5, column=2)

        self.label.config(text=f"{self.img_no}/{len(self.pil_images)}")
        self.label.grid(row=0, column=0, columnspan=3)

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y

        # Delete existing rectangle
        if self.rect_id:
            self.canvas.delete(self.rect_id)

        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_mouse_drag(self, event):
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.rect_id:
            print(f"Box: ({self.start_x}, {self.start_y}) to ({event.x}, {event.y})")
    
    def on_button_label(self):
        if self.rect_id:
            # Get widget coordinates
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()

            # Get label from textbox
            label = self.text_box.get("1.0", "end-1c").strip()
            if not label:
                return  # Don't proceed if label is empty

            # Get class number
            label_no = get_or_add_label(label)

            # Get actual image
            img = self.pil_images[self.img_no - 1]
            img_width, img_height = img.size

            # Convert box to YOLO format
            x_center, y_center, width, height = self.to_yolo_format(img_width, img_height)

            # Hide rectangle before capture
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.canvas.update()

            # Hash image and rectangle coords
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            hash_input = img_bytes + f"{self.start_x},{self.start_y}".encode()
            sha_hash = hashlib.sha256(hash_input).hexdigest()
            filename = f"{sha_hash[:10]}"

            # Save label file
            full_path_label = os.path.join(label_dir, filename + '.txt')
            with open(full_path_label, 'w') as file:
                file.write(f"{label_no} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

            # Save image file
            full_path_image = os.path.join(image_dir, filename + '.jpg')
            img.save(full_path_image)

            # Clear textbox
            self.text_box.delete("1.0", "end")

    def to_yolo_format(self, image_width, image_height):
        x_center, y_center, width, height = self.get_rect_center_and_size()

        return (
            x_center / image_width,
            y_center / image_height,
            width / image_width,
            height / image_height
        )
    
    def get_rect_center_and_size(self):
        # Get coords: [x1, y1, x2, y2]
        x1, y1, x2, y2 = self.canvas.coords(self.rect_id)

        # Normalize coordinates (in case user draws from bottom-right to top-left)
        x_min, x_max = sorted([x1, x2])
        y_min, y_max = sorted([y1, y2])

        # Compute center and size
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        return x_center, y_center, width, height
    
    
         
def get_or_add_label(label_name):
    label_name_lower = label_name.lower()

    # If file doesn't exist, initialize with empty structure
    if not os.path.exists(yaml_path):
        data = {"names": {}}
    else:
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file) or {}

    # Ensure 'names' exists
    if 'names' not in data:
        data['names'] = {}

    names = data['names']

    # Convert list to dict if needed
    if isinstance(names, list):
        names = {i: name for i, name in enumerate(names)}

    # Check for existing label (case-insensitive)
    for class_id, name in names.items():
        if name.lower() == label_name_lower:
            return int(class_id)

    # Add new label with next available id
    new_id = max(map(int, names.keys()), default=-1) + 1
    names[new_id] = label_name
    data['names'] = names

    # Update number of classes
    data['nc'] = len(names)

    # Save updated YAML file
    with open(yaml_path, 'w') as file:
        yaml.safe_dump(data, file)

    return new_id

    
labeler = Labeler()

labeler.root.mainloop()

