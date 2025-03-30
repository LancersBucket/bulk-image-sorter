"""Gets the metadata of an image file."""
from PIL import Image
from numpy import array as np_array

def get_image_histogram(image_path: str) -> list:
    """Gets histogram data of an image."""
    histogram = []
    with Image.open(image_path) as img:
        image = img.convert("L")  # Convert to grayscale
        histogram = np_array(image.histogram()).tolist()

    return histogram
