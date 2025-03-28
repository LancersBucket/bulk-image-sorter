import os
import shutil
from sys import exit as sys_exit
from glob import glob
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Bulk Image Sorter", width=1000, height=600)
dpg.setup_dearpygui()

# Configuration
source_folder = "images"  # Folder containing images to sort
destination_folders = {
    dpg.mvKey_1: "folder1",
    dpg.mvKey_2: "folder2",
    dpg.mvKey_3: "folder3",
    # Add more mappings as needed
}
preview_width = 975  # Width of the ImagePreview window
preview_height = 650  # Height of the ImagePreview window

# Ensure destination folders exist
for folder in destination_folders.values():
    os.makedirs(os.path.join(source_folder,folder), exist_ok=True)

# Get list of images
image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"]
image_files = []
for ext in image_extensions:
    image_files.extend(glob(os.path.join(source_folder, ext)))

current_index = 0

# Add a flag to track key press state
key_pressed = False

def load_next_image():
    """Load the next image in the list."""
    global current_index
    global preview_width
    global preview_height

    dpg.delete_item(f"texture_{current_index-1}")

    if current_index < len(image_files):
        image_path = image_files[current_index]
        dpg.set_value("ImagePath", f"Image: {image_path}")
        dpg.delete_item("ImagePreview", children_only=True)

        image_data = dpg.load_image(image_path)
        width, height, channels, data = image_data

        # Calculate scaling to fit the image into the preview window
        scale = min(preview_width / width, preview_height / height)
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)

        with dpg.texture_registry():
            texture_tag = f"texture_{current_index}"
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=texture_tag)

        dpg.add_image(texture_tag, parent="ImagePreview", width=scaled_width, height=scaled_height)
    else:
        dpg.set_value("ImagePath", "No more images to sort.")
        dpg.delete_item("ImagePreview", children_only=True)

def move_image(key):
    """Move the current image to the corresponding folder."""
    global current_index
    key = key[0]
    if current_index < len(image_files):
        image_path = image_files[current_index]
        if key in destination_folders:
            dest_folder = destination_folders[key]
            dest_folder_path = os.path.join(source_folder, dest_folder)
            shutil.move(image_path, os.path.join(dest_folder_path, os.path.basename(image_path)))
            current_index += 1
            load_next_image()

def key_callback(sender, data):
    """Handle key press events."""
    global key_pressed
    if not key_pressed:  # Only process if the key is not already pressed
        key_pressed = True
        move_image(data)

def key_release_callback(sender, data):
    """Handle key release events."""
    global key_pressed
    key_pressed = False  # Reset the flag when the key is released

with dpg.window(tag="Key Guide", no_resize=True, no_title_bar=True,
                no_move=True,no_collapse=True):
    dpg.add_text("Key Guide:")

    key = 0
    for _, folder in destination_folders.items():
        key += 1
        dpg.add_text(f"  {key}: {folder}")

    dpg.set_item_pos("Key Guide", [preview_width, 0])

with dpg.window(tag="Image Sorter", width=preview_width,no_resize=True,
                no_title_bar=True,no_move=True,no_collapse=True):
    dpg.add_text(label="", tag="ImagePath")
    dpg.add_child_window(tag="ImagePreview",width=preview_width,height=preview_height,border=True)
    dpg.set_item_pos("Image Sorter", [0, 0])

# Set up key callbacks
for key in destination_folders.keys():
    with dpg.handler_registry():
        dpg.add_key_down_handler(key=key, callback=key_callback)
        dpg.add_key_release_handler(key=key, callback=key_release_callback)

# Load the first image
load_next_image()

dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
sys_exit()