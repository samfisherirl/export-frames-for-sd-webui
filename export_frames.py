import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askinteger, askfloat
import cv2
import os

def select_video_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    return file_path

def get_user_input():
    fps = askinteger("Frame rate", "Enter desired frames per second (fps):", minvalue=1, maxvalue=60)
    scale = askfloat("Scale Ratio", "Enter scale ratio (1-100):", minvalue=1.0, maxvalue=100.0) / 100.0
    return fps, scale

def process_video(video_path, fps, scale):
    # Capture video
    video = cv2.VideoCapture(video_path)
    original_fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_gap = int(original_fps / fps)
    
    success, image = video.read()
    count = 0
    saved_frame_count = 0
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_name = video_name.replace(" ", "")
    output_dir = os.path.join(os.path.dirname(video_path), video_name + "_")
    # Create subdirectories
    frames_dir = os.path.join(output_dir, "frames")
    masks_dir = os.path.join(output_dir, "masks")
    output_subdir = os.path.join(output_dir, "output")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)
    os.makedirs(output_subdir, exist_ok=True)    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while success:
        if count % frame_gap == 0:
            # Resize frame
            width = int(image.shape[1] * scale)
            height = int(image.shape[0] * scale)
            resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

            # Save frame as PNG in the designated folder
            cv2.imwrite(os.path.join(frames_dir, f"{video_name}_frame{count}.png"), resized_image)
            saved_frame_count += 1

        success, image = video.read()
        count += 1

    print(f"Saved {saved_frame_count} frames to {output_dir}")

def main():
    video_path = select_video_file()
    if video_path:
        fps, scale = get_user_input()
        process_video(video_path, fps, scale)
    else:
        print("No video selected. Exiting.")

if __name__ == "__main__":
    main()