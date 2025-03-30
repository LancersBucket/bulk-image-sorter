"""Gets the metadata of an image file."""
import os
from PIL import Image
from numpy import array as np_array
import exifread

def path(pth: str) -> str:
    """ Get the absolute path to a resource, works for PyInstaller and script mode."""
    return os.path.join(os.getcwd(), pth)

class ImageMetadata:
    """Class to get the metadata of an image file."""
    meta = {
        "Camera": "",
        "ISO": "",
        "F-Stop": "",
        "Exposure": "",
        "White Balance": ""
    }
    histogram = []

    def __init__(self, image_path: str = None) -> None:
        if image_path is not None:
            self._get_image_histogram(image_path)
            self._get_metadata(image_path)

    def get_metadata(self) -> dict:
        """Returns metadata dict"""
        return self.meta

    def get_histogram(self) -> list:
        """Returns histogram data"""
        return self.histogram

    def _get_image_histogram(self, image_path: str) -> list:
        """Gets histogram data of an image."""
        histogram = []
        with Image.open(path(image_path)) as img:
            image = img.convert("L")  # Convert to grayscale
            histogram = np_array(image.histogram()).tolist()

        self.histogram = histogram

    def _get_metadata(self, image_path: str) -> dict:
        """Gets the metadata of an image file.
        Returns camera, iso, f-stop, and exposure."""
        # Open the image file in binary mode and read metadata using exifread
        with open(path(image_path), "rb") as f:
            tags = exifread.process_file(f)

        self.meta["Camera"] = tags.get("Image Model", "Unknown")
        self.meta["ISO"] = tags.get("EXIF ISOSpeedRatings", "Unknown")

        # Convert f_stop to a decimal
        f_stop = tags.get("EXIF FNumber", "Unknown")
        if f_stop != "Unknown":
            a, b = str(f_stop).split("/")
            f_stop = f'f/{int(a)/int(b)}'
        self.meta["F-Stop"] = f_stop

        # Add s to the exposure
        exposure = str(tags.get("EXIF ExposureTime", "Unknown"))
        if exposure != "Unknown":
            exposure += "s"
        self.meta["Exposure"] = exposure

        self.meta["White Balance"] = tags.get("EXIF WhiteBalance", "Unknown")
