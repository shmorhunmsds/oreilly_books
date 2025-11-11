#!/usr/bin/env python3
"""
Download cat and fish images using Bing Image Downloader
This replaces the old download.py script that relied on images.csv
"""

from bing_image_downloader import downloader
import os
import shutil

# Configuration
IMAGES_PER_CLASS = 500
CLASSES = ['cat', 'fish']
SET_TYPES = ['train', 'val', 'test']

# Split ratios
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def download_images():
    """Download images for each class"""
    print("Downloading images from Bing...")

    # Download to a temp directory first
    temp_dir = './temp_downloads'
    os.makedirs(temp_dir, exist_ok=True)

    for class_name in CLASSES:
        print(f"\nDownloading {IMAGES_PER_CLASS} {class_name} images...")
        try:
            downloader.download(
                query=class_name,
                limit=IMAGES_PER_CLASS,
                output_dir=temp_dir,
                adult_filter_off=True,
                force_replace=False,
                timeout=60,
                verbose=True
            )
        except Exception as e:
            print(f"Error downloading {class_name} images: {e}")

    return temp_dir

def organize_images(temp_dir):
    """Organize downloaded images into train/val/test splits"""
    print("\nOrganizing images into train/val/test splits...")

    for class_name in CLASSES:
        source_dir = os.path.join(temp_dir, class_name)

        if not os.path.exists(source_dir):
            print(f"Warning: No images found for {class_name}")
            continue

        # Get all image files
        images = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        total = len(images)

        if total == 0:
            print(f"Warning: No valid images found for {class_name}")
            continue

        print(f"Found {total} {class_name} images")

        # Calculate split sizes
        train_size = int(total * TRAIN_RATIO)
        val_size = int(total * VAL_RATIO)

        # Create destination directories
        for set_type in SET_TYPES:
            dest_dir = os.path.join(set_type, class_name)
            os.makedirs(dest_dir, exist_ok=True)

        # Move images to appropriate splits
        for idx, image in enumerate(images):
            source_path = os.path.join(source_dir, image)

            if idx < train_size:
                dest_path = os.path.join('train', class_name, image)
            elif idx < train_size + val_size:
                dest_path = os.path.join('val', class_name, image)
            else:
                dest_path = os.path.join('test', class_name, image)

            try:
                shutil.copy2(source_path, dest_path)
            except Exception as e:
                print(f"Error copying {image}: {e}")

        print(f"  Train: {train_size}, Val: {val_size}, Test: {total - train_size - val_size}")

def cleanup(temp_dir):
    """Remove temporary download directory"""
    if os.path.exists(temp_dir):
        print("\nCleaning up temporary files...")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    print("="*60)
    print("Cat vs Fish Image Dataset Downloader")
    print("="*60)

    temp_dir = download_images()
    organize_images(temp_dir)
    cleanup(temp_dir)

    print("\n" + "="*60)
    print("Download complete!")
    print("="*60)

    # Print summary
    for set_type in SET_TYPES:
        for class_name in CLASSES:
            path = os.path.join(set_type, class_name)
            if os.path.exists(path):
                count = len([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
                print(f"{set_type}/{class_name}: {count} images")
