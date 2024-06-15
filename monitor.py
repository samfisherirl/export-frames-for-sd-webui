import tkinter as tk
from tkinter import filedialog
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from PIL import Image

# Initialize global variables for folders A and B
folder_a_path = ""
folder_b_path = r"C:\Users\dower\Documents\sdwebui\webui\output\img2img-images"

def select_folder_a():
    """Select folder A"""
    global folder_a_path
    folder_a_path = filedialog.askdirectory()
    print(f"Folder A selected: {folder_a_path}")

def select_folder_b():
    """Select folder B"""
    global folder_b_path
    folder_b_path = filedialog.askdirectory()
    print(f"Folder B selected: {folder_b_path}")

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if is_image(event.src_path):
            try:
                replace_image_in_folder_a(event.src_path)
            except Exception as e:
                print(e)

def is_image(path):
    """Check if the file is an image."""
    try:
        Image.open(path)
    except IOError:
        return False
    return True

def get_sorted_image_paths(folder_path):
    """Return sorted list of image paths in the given folder."""
    image_files = [f for f in os.listdir(folder_path) if is_image(os.path.join(folder_path, f))]
    image_files.sort()
    return [os.path.join(folder_path, f) for f in image_files]

def replace_image_in_folder_a(new_image_path):
    """Replace the image in folder A with the one in folder B in order."""
    global folder_a_path
    image_list_a = get_sorted_image_paths(folder_a_path)
    # Skipping the first image as per requirement, replacement starts from the second image.
    if len(image_list_a) > 1:
        target_image_path = image_list_a[1]  # Targeting the second image for replacement
        shutil.copyfile(new_image_path, target_image_path)
        print(f"Replaced image: {target_image_path} with {new_image_path}")


def monitor_folder_b():
    """Monitor folder B for new images."""
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_b_path, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    root = tk.Tk()
    root.withdraw()  # Avoid Tk root window

    print("Select Folder A:")
    select_folder_a()

    print("Select Folder B:")
    select_folder_b()

    if folder_a_path and folder_b_path:
        print(f"Monitoring new images in {folder_b_path}...")
        monitor_folder_b()
    else:
        print("Folders not selected properly. Exiting.")

if __name__ == "__main__":
    main()