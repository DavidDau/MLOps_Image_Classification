"""
Download Sample Data for Image Classification

This script helps you download and organize a sample dataset
for quick testing of the MLOps pipeline.

Usage:
    python scripts/download_sample_data.py
"""

import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'

def create_directories():
    """Create necessary directories"""
    dirs = [
        DATA_DIR / 'train' / 'healthy',
        DATA_DIR / 'train' / 'diseased',
        DATA_DIR / 'test' / 'healthy',
        DATA_DIR / 'test' / 'diseased',
        DATA_DIR / 'uploaded'
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def download_sample_images():
    """
    Download sample images from a public source
    
    Note: You can replace this with your own dataset or use Kaggle API
    """
    print("\n" + "="*60)
    print("Sample Dataset Download")
    print("="*60)
    print("\nOptions for getting data:")
    print("\n1. Manual Download (Recommended)")
    print("   - Visit: https://www.kaggle.com/datasets/plant-disease")
    print("   - Or search Kaggle for 'leaf disease dataset' or 'plant disease dataset'")
    print("   - Download the dataset")
    print("   - Extract to data/ directory")
    print("   - Organize into train/test folders (e.g., healthy/diseased or specific disease types)")
    
    print("\n2. Kaggle API (If you have Kaggle credentials)")
    print("   - Install: pip install kaggle")
    print("   - Setup credentials: ~/.kaggle/kaggle.json")
    print("   - Run: kaggle datasets download -d salader/dogs-vs-cats")
    
    print("\n3. Use Your Own Images")
    print("   - Collect cat and dog images")
    print("   - Place them in:")
    print("     - data/train/cats/ (100+ images)")
    print("     - data/train/dogs/ (100+ images)")
    print("     - data/test/cats/ (20+ images)")
    print("     - data/test/dogs/ (20+ images)")
    
    print("\n" + "="*60)

def check_dataset():
    """Check if dataset is properly organized"""
    print("\n" + "="*60)
    print("Dataset Status Check")
    print("="*60)
    
    train_cats = len(list((DATA_DIR / 'train' / 'cats').glob('*.jpg'))) + \
                 len(list((DATA_DIR / 'train' / 'cats').glob('*.png')))
    train_dogs = len(list((DATA_DIR / 'train' / 'dogs').glob('*.jpg'))) + \
                 len(list((DATA_DIR / 'train' / 'dogs').glob('*.png')))
    test_cats = len(list((DATA_DIR / 'test' / 'cats').glob('*.jpg'))) + \
                len(list((DATA_DIR / 'test' / 'cats').glob('*.png')))
    test_dogs = len(list((DATA_DIR / 'test' / 'dogs').glob('*.jpg'))) + \
                len(list((DATA_DIR / 'test' / 'dogs').glob('*.png')))
    
    print(f"\nTraining Data:")
    print(f"  Cats: {train_cats} images")
    print(f"  Dogs: {train_dogs} images")
    print(f"  Total: {train_cats + train_dogs} images")
    
    print(f"\nTest Data:")
    print(f"  Cats: {test_cats} images")
    print(f"  Dogs: {test_dogs} images")
    print(f"  Total: {test_cats + test_dogs} images")
    
    total = train_cats + train_dogs + test_cats + test_dogs
    
    if total == 0:
        print("\n⚠️  No images found! Please add images to the data directories.")
        print("\nRecommended minimum:")
        print("  - Training: 100 images per class (200 total)")
        print("  - Testing: 20 images per class (40 total)")
        return False
    elif total < 240:
        print("\n⚠️  Dataset is small. Consider adding more images for better results.")
        print("     Current: {} images, Recommended: 240+ images".format(total))
        return False
    else:
        print("\n✓ Dataset looks good! Ready for training.")
        return True

def create_sample_structure():
    """Create a sample structure file for reference"""
    structure = """
MLOps_Image_Classification/
│
├── data/
│   ├── train/
│   │   ├── cats/
│   │   │   ├── cat.1.jpg
│   │   │   ├── cat.2.jpg
│   │   │   └── ... (100+ images)
│   │   └── dogs/
│   │       ├── dog.1.jpg
│   │       ├── dog.2.jpg
│   │       └── ... (100+ images)
│   │
│   ├── test/
│   │   ├── cats/
│   │   │   └── ... (20+ images)
│   │   └── dogs/
│   │       └── ... (20+ images)
│   │
│   └── uploaded/
│       └── (user uploaded images)
"""
    
    with open(DATA_DIR / 'STRUCTURE.txt', 'w') as f:
        f.write(structure)
    
    print(f"\n✓ Created structure reference file: {DATA_DIR / 'STRUCTURE.txt'}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("MLOps Image Classification - Data Setup")
    print("="*60)
    
    # Create directories
    create_directories()
    
    # Create structure reference
    create_sample_structure()
    
    # Show download options
    download_sample_images()
    
    # Check current dataset status
    dataset_ready = check_dataset()
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    
    if dataset_ready:
        print("\n1. ✓ Dataset is ready!")
        print("2. Open and run: notebook/image_classification.ipynb")
        print("3. Train the model (this will take 15-30 minutes)")
        print("4. Start the application: python app/app.py")
    else:
        print("\n1. Add images to the data directories")
        print("2. Run this script again to verify: python scripts/download_sample_data.py")
        print("3. Once ready, train the model using the Jupyter notebook")
    
    print("\n" + "="*60 + "\n")
