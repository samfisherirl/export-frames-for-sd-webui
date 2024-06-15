import os
from tkinter import Tk, filedialog

# Create a Tkinter root window
root = Tk()
root.withdraw()  # Hide the main window

# Prompt the user to select folder A
print("Please select folder A (to copy name/original):")
folder_a = filedialog.askdirectory()

# Prompt the user to select folder B
print("Please select folder B (to be renamed/mask):")
folder_b = filedialog.askdirectory()

# Get the list of files in folder A and folder B
files_a = os.listdir(folder_a)
files_b = os.listdir(folder_b)

# Sort the file lists alphabetically
files_a.sort()
files_b.sort()

# Check if the number of files in both folders is the same
if len(files_a) != len(files_b):
    print("Error: The number of files in folder A and folder B does not match.")
    exit()

# Rename the files in folder B to match the corresponding files in folder A
for i in range(len(files_a)):
    old_file_path = os.path.join(folder_b, files_b[i])
    new_file_path = os.path.join(folder_b, files_a[i])
    os.rename(old_file_path, new_file_path)

print("File renaming complete.")