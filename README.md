# Bulk Image Sorter
A simple program designed to assist sorting through photos.
## Usage
1. Create a folder named 'images' and place all the photos in it in the directory of the exe
2. Run the program, and press the key associated with the folder you want to move it into.
## Configuration
On first run Bulk Image Sorter will generate a configuration.json file. `source_folder` is the folder that the images are located in. This is also the folder where the `destination_folders` will be created. Each `destination_folder` is in the following format:
```JSON
"Alphanumeric Keyboard Key": {
    "label": "Label as it appears in BIS",
    "path": "Path of the folder (relative to source_folder)"
}
```
You can add as many `destination_folders` as you'd like.
# TODO
- Add a GUI to allow user defined destination folders (Currently done in the configuration file)