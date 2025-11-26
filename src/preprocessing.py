"""
Data Preprocessing Module for Image Classification

This module handles:
- Image loading and preprocessing
- Data augmentation
- Batch processing for training and prediction
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from PIL import Image
import os
from typing import Tuple, Optional


class ImagePreprocessor:
    """
    Handles all image preprocessing operations
    """
    
    def __init__(self, img_size: Tuple[int, int] = (224, 224)):
        """
        Initialize the preprocessor
        
        Args:
            img_size: Target size for images (height, width)
        """
        self.img_size = img_size
        
    def create_train_generator(self, 
                               train_dir: str, 
                               batch_size: int = 32,
                               validation_split: float = 0.2) -> Tuple:
        """
        Create training and validation data generators with augmentation
        
        Args:
            train_dir: Directory containing training images
            batch_size: Batch size for training
            validation_split: Fraction of data to use for validation
            
        Returns:
            Tuple of (train_generator, validation_generator)
        """
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest',
            validation_split=validation_split
        )
        
        # Training generator
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        # Validation generator
        validation_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        return train_generator, validation_generator
    
    def create_test_generator(self, 
                             test_dir: str, 
                             batch_size: int = 32):
        """
        Create test data generator without augmentation
        
        Args:
            test_dir: Directory containing test images
            batch_size: Batch size for testing
            
        Returns:
            Test data generator
        """
        test_datagen = ImageDataGenerator(rescale=1./255)
        
        test_generator = test_datagen.flow_from_directory(
            test_dir,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        return test_generator
    
    def preprocess_single_image(self, 
                               image_path: str,
                               normalize: bool = True) -> np.ndarray:
        """
        Preprocess a single image for prediction
        
        Args:
            image_path: Path to the image file
            normalize: Whether to normalize pixel values
            
        Returns:
            Preprocessed image array ready for prediction
        """
        try:
            # Load image
            img = load_img(image_path, target_size=self.img_size)
            
            # Convert to array
            img_array = img_to_array(img)
            
            # Normalize if requested
            if normalize:
                img_array = img_array / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise ValueError(f"Error preprocessing image {image_path}: {str(e)}")
    
    def preprocess_uploaded_image(self, 
                                 image_file,
                                 normalize: bool = True) -> np.ndarray:
        """
        Preprocess an uploaded image file (e.g., from Flask request)
        
        Args:
            image_file: File object or bytes
            normalize: Whether to normalize pixel values
            
        Returns:
            Preprocessed image array ready for prediction
        """
        try:
            # Load image from file object
            img = Image.open(image_file)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize
            img = img.resize(self.img_size)
            
            # Convert to array
            img_array = img_to_array(img)
            
            # Normalize if requested
            if normalize:
                img_array = img_array / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise ValueError(f"Error preprocessing uploaded image: {str(e)}")
    
    def preprocess_batch_images(self, 
                               image_paths: list,
                               normalize: bool = True) -> np.ndarray:
        """
        Preprocess a batch of images
        
        Args:
            image_paths: List of paths to image files
            normalize: Whether to normalize pixel values
            
        Returns:
            Batch of preprocessed images
        """
        images = []
        
        for image_path in image_paths:
            try:
                img_array = self.preprocess_single_image(image_path, normalize)
                images.append(img_array[0])  # Remove batch dimension
            except Exception as e:
                print(f"Skipping {image_path}: {str(e)}")
                continue
        
        if not images:
            raise ValueError("No valid images found in the batch")
        
        return np.array(images)
    
    def save_uploaded_files(self, 
                           files, 
                           save_dir: str) -> list:
        """
        Save uploaded files to a directory
        
        Args:
            files: List of file objects
            save_dir: Directory to save files
            
        Returns:
            List of saved file paths
        """
        os.makedirs(save_dir, exist_ok=True)
        saved_paths = []
        
        for file in files:
            try:
                # Generate safe filename
                filename = os.path.basename(file.filename)
                filepath = os.path.join(save_dir, filename)
                
                # Save file
                file.save(filepath)
                saved_paths.append(filepath)
                
            except Exception as e:
                print(f"Error saving file {file.filename}: {str(e)}")
                continue
        
        return saved_paths
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate if a file is a valid image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if valid, False otherwise
        """
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        
        try:
            # Check extension
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in valid_extensions:
                return False
            
            # Try to open image
            img = Image.open(image_path)
            img.verify()
            
            return True
            
        except Exception:
            return False
    
    def get_class_weights(self, train_dir: str) -> dict:
        """
        Calculate class weights for imbalanced datasets
        
        Args:
            train_dir: Directory containing training images
            
        Returns:
            Dictionary of class weights
        """
        from collections import Counter
        
        # Count images per class
        class_counts = {}
        for class_name in os.listdir(train_dir):
            class_path = os.path.join(train_dir, class_name)
            if os.path.isdir(class_path):
                class_counts[class_name] = len(os.listdir(class_path))
        
        # Calculate weights
        total = sum(class_counts.values())
        num_classes = len(class_counts)
        
        class_weights = {}
        for idx, (class_name, count) in enumerate(class_counts.items()):
            class_weights[idx] = total / (num_classes * count)
        
        return class_weights


def preprocess_for_retraining(uploaded_dir: str, 
                              train_dir: str,
                              class_mapping: dict) -> int:
    """
    Preprocess uploaded images for retraining
    Organize them into class folders
    
    Args:
        uploaded_dir: Directory containing uploaded images
        train_dir: Directory where training images are stored
        class_mapping: Mapping of filenames to class labels
        
    Returns:
        Number of images processed
    """
    processed_count = 0
    
    for filename, class_label in class_mapping.items():
        src_path = os.path.join(uploaded_dir, filename)
        
        if not os.path.exists(src_path):
            continue
        
        # Create class directory if it doesn't exist
        class_dir = os.path.join(train_dir, class_label)
        os.makedirs(class_dir, exist_ok=True)
        
        # Copy or move file to class directory
        dst_path = os.path.join(class_dir, filename)
        
        try:
            # Validate image
            preprocessor = ImagePreprocessor()
            if preprocessor.validate_image(src_path):
                import shutil
                shutil.copy2(src_path, dst_path)
                processed_count += 1
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    return processed_count


if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = ImagePreprocessor(img_size=(224, 224))
    print("ImagePreprocessor initialized successfully!")
    print(f"Target image size: {preprocessor.img_size}")
