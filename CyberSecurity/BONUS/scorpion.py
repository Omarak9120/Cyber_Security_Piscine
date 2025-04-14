import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
import piexif  # For stripping metadata

SUPPORTED_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def extract_metadata(file_path):
    if not file_path.lower().endswith(SUPPORTED_EXT):
        print(f"[!] Skipping unsupported file: {file_path}")
        return

    try:
        with Image.open(file_path) as img:
            print(f"\n File: {file_path}")
            print(f" Format: {img.format}")
            print(f" Size: {img.size}")
            print(f" Mode: {img.mode}")

            info = img._getexif() # Get EXIF data
            if info: # If there is EXIF data, print it
                print("\n EXIF Metadata:")
                for tag, value in info.items(): # Iterate through the EXIF data
                    readable_tag = TAGS.get(tag, tag) # Convert tag number to readable name
                    print(f"  {readable_tag}: {value}") # Print the tag and its value
            else:
                print(" No EXIF metadata found.")

    except Exception as e:
        print(f"[!] Could not read {file_path}: {e}")

def strip_metadata(file_path):
    try:
        if not file_path.lower().endswith(SUPPORTED_EXT): # Check if the file is supported
            print(f"[!] Unsupported format for stripping: {file_path}")
            return

        img = Image.open(file_path)

        piexif.remove(file_path)

        print(f"[✔] Metadata stripped from {file_path}")

    except Exception as e:
        print(f"[!] Error stripping metadata from {file_path}: {e}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Scorpion: EXIF Viewer / Metadata Stripper")
    parser.add_argument("files", nargs="+", help="Image files to process")
    parser.add_argument("--strip", action="store_true", help="Strip all EXIF metadata from images")
    args = parser.parse_args()

    for file_path in args.files:
        if args.strip:
            strip_metadata(file_path)
        else:
            extract_metadata(file_path)

if __name__ == '__main__':
    main()
