"""Bulk Image Sorter"""
import os
import shutil
from sys import exit as sys_exit
from glob import glob
import dearpygui.dearpygui as dpg

class Global:
    """Configuration and global variables."""
    VERSION = "Bulk Image Sorter v1.0.0"

    source_folder = "images"
    destination_folders = {
        dpg.mvKey_1: "Accept",
        dpg.mvKey_2: "Needs Cropping",
        dpg.mvKey_3: "Needs Review",
        dpg.mvKey_4: "Reject",
        # Add more mappings as needed
    }
    image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"]
    preview_width = 975
    preview_height = 650

    current_index = 0
    key_pressed = False

dpg.create_context()
dpg.create_viewport(title=Global.VERSION, width=1000, height=600)
dpg.setup_dearpygui()

# Ensure destination folders exist
for folder in Global.destination_folders.values():
    os.makedirs(os.path.join(Global.source_folder,folder), exist_ok=True)

# Get list of images
image_files = []
for ext in Global.image_extensions:
    image_files.extend(glob(os.path.join(Global.source_folder, ext)))

def load_next_image():
    """Load the next image in the list."""
    dpg.delete_item(f"texture_{Global.current_index-1}")

    if Global.current_index < len(image_files):
        image_path = image_files[Global.current_index]
        dpg.set_value("ImagePath", f"Image: {image_path}")
        dpg.delete_item("ImagePreview", children_only=True)

        image_data = dpg.load_image(image_path)
        width, height, _, data = image_data

        # Calculate scaling to fit the image into the preview window
        scale = min(Global.preview_width / width, Global.preview_height / height)
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)

        with dpg.texture_registry():
            texture_tag = f"texture_{Global.current_index}"
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=texture_tag)

        dpg.add_image(texture_tag, parent="ImagePreview", width=scaled_width, height=scaled_height)
    else:
        dpg.set_value("ImagePath", "No more images to sort.")
        dpg.delete_item("ImagePreview", children_only=True)

def move_image(img_key):
    """Move the current image to the corresponding folder."""
    img_key = img_key[0]
    if Global.current_index < len(image_files):
        image_path = image_files[Global.current_index]
        if img_key in Global.destination_folders:
            dest_folder = Global.destination_folders[img_key]
            dest_folder_path = os.path.join(Global.source_folder, dest_folder)
            shutil.move(image_path, os.path.join(dest_folder_path, os.path.basename(image_path)))
            Global.current_index += 1
            load_next_image()

def key_callback(_, data):
    """Handle key press events."""
    if not Global.key_pressed:
        Global.key_pressed = True
        move_image(data)

def key_release_callback():
    """Handle key release events."""
    Global.key_pressed = False

with dpg.window(tag="Key Guide", no_resize=True, no_title_bar=True,
                no_move=True,no_collapse=True):

    dpg.add_text("Key Guide:")

    key = 0
    for _, folder in Global.destination_folders.items():
        key += 1
        dpg.add_text(f"  {key}: {folder}")

    dpg.set_item_pos("Key Guide", [Global.preview_width, 0])

with dpg.window(tag="Image Sorter", width=Global.preview_width,no_resize=True,
                no_title_bar=True,no_move=True,no_collapse=True):
    dpg.add_text(label="", tag="ImagePath")
    dpg.add_child_window(tag="ImagePreview",width=Global.preview_width,
                         height=Global.preview_height,border=False)
    dpg.set_item_pos("Image Sorter", [0, 0])

# Set up key callbacks
for key in Global.destination_folders:
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
