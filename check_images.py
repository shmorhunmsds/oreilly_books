#!/usr/bin/env python3
"""Check which images PIL cannot open and remove them."""

from PIL import Image
import os
from pathlib import Path

corrupt_files = []
directories = ['./train/fish', './train/cat', './val/fish', './val/cat', './test/fish', './test/cat']

for directory in directories:
    if not os.path.exists(directory):
        continue

    for image_path in Path(directory).glob('*'):
        if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            try:
                img = Image.open(image_path)
                img.verify()  # Verify it's a valid image
                img.close()
                # Try to actually load it
                img = Image.open(image_path)
                img.load()
                img.close()
            except Exception as e:
                print(f"Corrupt: {image_path} - {e}")
                corrupt_files.append(image_path)

print(f"\nFound {len(corrupt_files)} corrupt files")

if corrupt_files:
    response = input("Delete these files? (y/n): ")
    if response.lower() == 'y':
        for f in corrupt_files:
            f.unlink()
            print(f"Deleted: {f}")
        print(f"Deleted {len(corrupt_files)} corrupt files")
