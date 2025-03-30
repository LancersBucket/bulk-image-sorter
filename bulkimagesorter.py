"""Bulk Image Sorter"""
import os
import shutil
from sys import exit as sys_exit
from glob import glob
import dearpygui.dearpygui as dpg
import imagemetadata as imd
import mvkeylookup as mvkl

class Global:
    """Configuration and global variables."""
    VERSION = "Bulk Image Sorter v1.1.0-DEV"

    # Configuration
    source_folder = "images"
    destination_folders = {
        "1": "Accept",
        "2": "Needs Cropping",
        "3": "Needs Review",
        "4": "Reject",
    }
    image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"]

    # Flags
    key_pressed = False

    # Global variables
    current_index = 0
    image_files = []

def load_next_image() -> None:
    """Load the next image in the list."""
    # Delete the previous image data
    dpg.delete_item(f"texture_{Global.current_index-1}")
    dpg.delete_item("LevelsHistogram_Data")
    dpg.delete_item("ImagePreview", children_only=True)

    # If there are still more images
    if Global.current_index < len(Global.image_files):
        image_path = Global.image_files[Global.current_index]

        # Load the next image along with all the metadata
        dpg.set_value("ImagePath", f"Image: {image_path}")

        dpg.add_line_series(list(range(256)), imd.get_image_histogram(image_path),
                            tag="LevelsHistogram_Data", parent="LevelsHistogram_Y")
        dpg.bind_item_theme("LevelsHistogram_Data", "plot_theme")

        # Load the image
        image_data = dpg.load_image(image_path)
        width, height, _, data = image_data

        # Calculate scaling to fit the image into the preview window
        scale = min(975 / width, 650 / height)
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)

        # Add the image to the texture registry
        with dpg.texture_registry():
            texture_tag = f"texture_{Global.current_index}"
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=texture_tag)

        # Display the image
        dpg.add_image(texture_tag, parent="ImagePreview", width=scaled_width, height=scaled_height)
    else:
        dpg.set_value("ImagePath", "No more images to sort.")

def move_image(img_key: str) -> None:
    """Move the current image to the corresponding folder."""
    img_key = mvkl.mvkey_to_string(img_key[0])
    if Global.current_index < len(Global.image_files):
        image_path = Global.image_files[Global.current_index]
        if img_key in Global.destination_folders:
            dest_folder = Global.destination_folders[img_key]
            dest_folder_path = os.path.join(Global.source_folder, dest_folder)
            shutil.move(image_path, os.path.join(dest_folder_path, os.path.basename(image_path)))
            Global.current_index += 1
            load_next_image()

def key_callback(_, data) -> None:
    """Handle key press events."""
    if not Global.key_pressed:
        Global.key_pressed = True
        move_image(data)

def key_release_callback() -> None:
    """Handle key release events."""
    Global.key_pressed = False

if __name__ == "__main__":
    # Initialize dpg
    dpg.create_context()
    dpg.create_viewport(title=Global.VERSION)
    dpg.setup_dearpygui()

    # Create destination folders
    for folder in Global.destination_folders.values():
        os.makedirs(os.path.join(Global.source_folder,folder), exist_ok=True)

    # Get list of images
    for ext in Global.image_extensions:
        Global.image_files.extend(glob(os.path.join(Global.source_folder, ext)))

    # Guide and Metadata Window
    with dpg.window(tag="Key Guide", no_resize=True, no_title_bar=True,
                    no_move=True,no_collapse=True, width=289):
        dpg.add_text("Key Guide:")
        for key, folder in Global.destination_folders.items():
            dpg.add_text(f"  {key}: {folder}")

        dpg.add_spacer()
        dpg.add_spacer()

        dpg.add_text("Metadata:")

        # Themeing for histogram
        with dpg.theme(tag="plot_theme"):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255),
                                    category=dpg.mvThemeCat_Plots)

        # Create levels histogram
        with dpg.plot(height=160, width=274, tag="LevelsHistogram",no_inputs=True,no_frame=True):
            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True, no_gridlines=True,
                              no_tick_marks=True)
            dpg.add_plot_axis(dpg.mvYAxis, no_tick_labels=True, no_gridlines=True,
                              no_tick_marks=True, tag="LevelsHistogram_Y")

        # Move the window to the right of the display
        dpg.set_item_pos("Key Guide", [990, 0])

    # Image Preview Window
    with dpg.window(tag="Image Sorter", width=991, no_resize=True,
                    no_title_bar=True, no_move=True, no_collapse=True):
        dpg.add_text(label="", tag="ImagePath")
        dpg.add_child_window(tag="ImagePreview",width=975,
                            height=650,border=False)
        dpg.set_item_pos("Image Sorter", [0, 0])

    # Key Callbacks
    for key in Global.destination_folders:
        # Convert string rep of the key to mvKey_* constant
        mvkey = mvkl.string_to_mvkey(key)

        print(f"Key: {key} -> mvKey: {mvkey}")

        if mvkey is None:
            raise ValueError(f'Key {key} is not a valid key. Only alphanumeric keys are supported.')

        with dpg.handler_registry():
            dpg.add_key_down_handler(key=mvkey, callback=key_callback)
            dpg.add_key_release_handler(key=mvkey, callback=key_release_callback)

    # Load the first image
    load_next_image()

    # Finish initialization
    dpg.maximize_viewport()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    # When the window closes, exit the program
    sys_exit()
