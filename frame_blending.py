from PIL import Image
import os
from tkinter import filedialog
import tkinter as tk
import shutil
from pathlib import Path

def select_folder():
    """
    Opens a dialog to select a folder and prints the selected folder's path.
    """
    root = tk.Tk()
    root.withdraw()  # Use to hide the tkinter root window
    
    folder_selected = filedialog.askdirectory()  # Open the dialog to choose a folder
    print(f"Selected folder: {folder_selected}")
    return folder_selected
    
def blend_frames():
    """
    Improved function to blend frames by averaging every consecutive pair of images in a folder.
    Now includes creating separate folders for duplicates and blended images.
    """
    input_folder = select_folder()  # Assume this function is defined elsewhere to select the folder.
    
    # Define the parent of the input folder
    parent_folder = os.path.dirname(input_folder)
    
    # Create folders for duplicates and blended images
    dupe_folder = os.path.join(parent_folder, 'dupes')
    blended_folder = os.path.join(parent_folder, 'blended')
    if not os.path.exists(dupe_folder):
        os.makedirs(dupe_folder)
    if not os.path.exists(blended_folder):
        os.makedirs(blended_folder)
    
    # Get all .png files and sort them to maintain the sequence
    files = [f for f in sorted(os.listdir(input_folder)) if f.endswith('.png')]
    num_files = len(files)
    
    for i in range(num_files - 1):
        # Load images
        img1 = Image.open(os.path.join(input_folder, files[i]))
        img2 = Image.open(os.path.join(input_folder, files[i + 1]))
        
        # Blend images
        blended_img = Image.blend(img1, img2, alpha=0.5)
        
        # Save blended image with modified filename
        framename_without_extension, _ = os.path.splitext(files[i])
        output_filename = f"{framename_without_extension}_blended.png"
        blended_img.save(os.path.join(blended_folder, output_filename))

        # Names for duplicate files
        dupename = f"{framename_without_extension}_1_dupe.png"
        dupename2 = f"{framename_without_extension}_2_dupe.png"
        
        # Save duplicate files in dupe_folder
        shutil.copy(os.path.join(input_folder, files[i]), os.path.join(dupe_folder, dupename))
        shutil.copy(os.path.join(input_folder, files[i+1]), os.path.join(dupe_folder, dupename2))

        print(f"Saved blended image: {output_filename} in {blended_folder}")
        print(f"Saved duplicate: {dupename} and {dupename2} in {dupe_folder}")

if __name__ == "__main__":
    blend_frames()