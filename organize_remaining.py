#!/usr/bin/env python3
"""
Organize remaining images from temp_downloads into train/val/test splits
"""

import os
import shutil

# Configuration
TEMP_DIR = './temp_downloads'
CLASSES = ['cat', 'fish']
SET_TYPES = ['train', 'val', 'test']

# Split ratios
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def organize_images():
    """Organize downloaded images into train/val/test splits"""
    print("Organizing remaining images from temp_downloads...")

    for class_name in CLASSES:
        source_dir = os.path.join(TEMP_DIR, class_name)

        if not os.path.exists(source_dir):
            print(f"Warning: No directory found for {class_name}")
            continue

        # Get all image files
        images = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        total = len(images)

        if total == 0:
            print(f"No images found for {class_name}")
            continue

        print(f"\nProcessing {total} {class_name} images from temp_downloads")

        # Calculate split sizes
        train_size = int(total * TRAIN_RATIO)
        val_size = int(total * VAL_RATIO)

        # Ensure destination directories exist
        for set_type in SET_TYPES:
            dest_dir = os.path.join(set_type, class_name)
            os.makedirs(dest_dir, exist_ok=True)

        # Move images to appropriate splits
        train_count = 0
        val_count = 0
        test_count = 0

        for idx, image in enumerate(images):
            source_path = os.path.join(source_dir, image)

            if idx < train_size:
                dest_path = os.path.join('train', class_name, image)
                train_count += 1
            elif idx < train_size + val_size:
                dest_path = os.path.join('val', class_name, image)
                val_count += 1
            else:
                dest_path = os.path.join('test', class_name, image)
                test_count += 1

            try:
                shutil.copy2(source_path, dest_path)
            except Exception as e:
                print(f"Error copying {image}: {e}")

        print(f"  Added to train: {train_count}")
        print(f"  Added to val: {val_count}")
        print(f"  Added to test: {test_count}")

def cleanup():
    """Remove temporary download directory"""
    if os.path.exists(TEMP_DIR):
        print("\nCleaning up temp_downloads directory...")
        shutil.rmtree(TEMP_DIR)
        print("Done!")

def print_summary():
    """Print final dataset summary"""
    print("\n" + "="*60)
    print("Final Dataset Summary")
    print("="*60)

    for set_type in SET_TYPES:
        print(f"\n{set_type.upper()}:")
        for class_name in CLASSES:
            path = os.path.join(set_type, class_name)
            if os.path.exists(path):
                count = len([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
                print(f"  {class_name}: {count} images")

if __name__ == "__main__":
    print("="*60)
    print("Organizing Remaining Images")
    print("="*60)

    organize_images()
    cleanup()
    print_summary()

    print("\n" + "="*60)
    print("Dataset is ready!")
    print("="*60)
