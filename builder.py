import cv2
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

# --- GUI Setup ---
def builder(tk.Frame):
    def start_recording():
        try:
            fps = int(fps_entry.get())
            duration = int(duration_entry.get())
            resolution = resolution_var.get()

            width, height = map(int, resolution.split('x'))

            # Start recording in a separate thread
            recording_thread = Thread(target=record_video, args=(fps, duration, width, height))
            recording_thread.start()
        except ValueError:
            print("Please enter valid numbers for FPS and Duration.")

    def record_video(fps, duration, width, height):
        output_filename = 'recorded_video.avi'

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not cap.isOpened():
            print("Error: Could not open video source.")
            return

        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_filename, fourcc, fps, (actual_width, actual_height))

        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame.")
                break

            out.write(frame)
            cv2.imshow('Live Feed', frame)

            elapsed_time = time.time() - start_time
            if elapsed_time >= duration:
                print(f"Recording finished after {duration} seconds.")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Recording stopped by user.")
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # --- Create tkinter GUI ---
    root = tk.Tk()
    root.title("Video Recorder")

    tk.Label(root, text="Frame Rate (FPS):").grid(row=0, column=0, sticky='e')
    fps_entry = tk.Entry(root)
    fps_entry.insert(0, "20")
    fps_entry.grid(row=0, column=1)

    tk.Label(root, text="Duration (seconds):").grid(row=1, column=0, sticky='e')
    duration_entry = tk.Entry(root)
    duration_entry.insert(0, "10")
    duration_entry.grid(row=1, column=1)

    tk.Label(root, text="Resolution:").grid(row=2, column=0, sticky='e')
    resolution_var = tk.StringVar(value="1920x1080")
    res_options = ["640x480", "1280x720", "1920x1080"]
    res_menu = ttk.Combobox(root, textvariable=resolution_var, values=res_options, state="readonly")
    res_menu.grid(row=2, column=1)

    start_button = tk.Button(root, text="Start Recording", command=start_recording)
    start_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()
