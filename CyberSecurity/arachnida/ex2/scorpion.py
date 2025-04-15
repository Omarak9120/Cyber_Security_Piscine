import os
import sys #to read command-line arguments (sys.argv)
from PIL import Image #opens image files
from PIL.ExifTags import TAGS #converts raw EXIF tag numbers to readable names 271 → "Make"

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

def main():
    if len(sys.argv) < 2:
        print("Usage: python scorpion.py FILE1 [FILE2 ...]")
        sys.exit(1)

    for file in sys.argv[1:]:
        extract_metadata(file)

if __name__ == '__main__':
    main()
