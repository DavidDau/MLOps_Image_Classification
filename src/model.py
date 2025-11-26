"""
Model Creation and Training Module

This module handles:
- Model architecture creation using Transfer Learning
- Model training and fine-tuning
- Model retraining with new data
- Model saving and loading
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np
import os
import json
from datetime import datetime
from typing import Tuple, Optional


class ImageClassifier:
    """
    Image Classification Model using Transfer Learning
    """
    
    def __init__(self, 
                 img_size: Tuple[int, int] = (224, 224),
                 num_classes: int = 2,
                 learning_rate: float = 0.0001):
        """
        Initialize the classifier
        
        Args:
            img_size: Input image size (height, width)
            num_classes: Number of output classes
            learning_rate: Initial learning rate
        """
        self.img_size = img_size
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.model = None
        self.base_model = None
        self.history = None
        
    def create_model(self) -> keras.Model:
        """
        Create the model architecture using MobileNetV2 as base
        
        Returns:
            Compiled Keras model
        """
        # Load pretrained MobileNetV2
        self.base_model = MobileNetV2(
            input_shape=(*self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model initially
        self.base_model.trainable = False
        
        # Build custom architecture
        inputs = keras.Input(shape=(*self.img_size, 3))
        
        # Preprocessing
        x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
        
        # Base model
        x = self.base_model(x, training=False)
        
        # Custom top layers
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dense(256, activation='relu', 
                        kernel_regularizer=keras.regularizers.l2(0.01))(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(128, activation='relu',
                        kernel_regularizer=keras.regularizers.l2(0.01))(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        
        # Compile model
        self._compile_model(self.learning_rate)
        
        return self.model
    
    def _compile_model(self, learning_rate: float):
        """
        Compile the model with optimizer and metrics
        
        Args:
            learning_rate: Learning rate for optimizer
        """
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy',
                    keras.metrics.Precision(name='precision'),
                    keras.metrics.Recall(name='recall')]
        )
    
    def train(self,
             train_generator,
             validation_generator,
             epochs: int = 20,
             callbacks: Optional[list] = None) -> keras.callbacks.History:
        """
        Train the model
        
        Args:
            train_generator: Training data generator
            validation_generator: Validation data generator
            epochs: Number of epochs to train
            callbacks: List of Keras callbacks
            
        Returns:
            Training history
        """
        if self.model is None:
            raise ValueError("Model not created. Call create_model() first.")
        
        if callbacks is None:
            callbacks = self._get_default_callbacks()
        
        print("=" * 60)
        print("Starting Training...")
        print("=" * 60)
        
        self.history = self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\nTraining completed!")
        return self.history
    
    def fine_tune(self,
                 train_generator,
                 validation_generator,
                 epochs: int = 30,
                 unfreeze_from: int = 100,
                 callbacks: Optional[list] = None) -> keras.callbacks.History:
        """
        Fine-tune the model by unfreezing base layers
        
        Args:
            train_generator: Training data generator
            validation_generator: Validation data generator
            epochs: Number of epochs to fine-tune
            unfreeze_from: Layer index to start unfreezing from
            callbacks: List of Keras callbacks
            
        Returns:
            Fine-tuning history
        """
        if self.model is None or self.base_model is None:
            raise ValueError("Model not trained. Train the model first.")
        
        print("=" * 60)
        print("Starting Fine-tuning...")
        print("=" * 60)
        
        # Unfreeze base model
        self.base_model.trainable = True
        
        # Freeze early layers
        for layer in self.base_model.layers[:unfreeze_from]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self._compile_model(self.learning_rate / 10)
        
        print(f"Trainable layers: {sum([1 for layer in self.model.layers if layer.trainable])}")
        
        if callbacks is None:
            callbacks = self._get_default_callbacks()
        
        history_fine = self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\nFine-tuning completed!")
        return history_fine
    
    def retrain(self,
               train_generator,
               validation_generator,
               pretrained_model_path: str,
               epochs: int = 10,
               callbacks: Optional[list] = None) -> keras.callbacks.History:
        """
        Retrain the model using a pretrained model as starting point
        
        Args:
            train_generator: Training data generator with new data
            validation_generator: Validation data generator
            pretrained_model_path: Path to pretrained model file
            epochs: Number of epochs to retrain
            callbacks: List of Keras callbacks
            
        Returns:
            Retraining history
        """
        print("=" * 60)
        print("Starting Retraining with Pretrained Model...")
        print("=" * 60)
        
        # Load pretrained model
        self.load_model(pretrained_model_path)
        
        # Unfreeze all layers for retraining
        for layer in self.model.layers:
            layer.trainable = True
        
        # Recompile with lower learning rate for retraining
        self._compile_model(self.learning_rate / 10)
        
        if callbacks is None:
            callbacks = self._get_default_callbacks()
        
        print(f"Retraining on {train_generator.samples} samples...")
        
        self.history = self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\nRetraining completed!")
        return self.history
    
    def _get_default_callbacks(self, model_dir: str = '../models') -> list:
        """
        Get default callbacks for training
        
        Args:
            model_dir: Directory to save model checkpoints
            
        Returns:
            List of callbacks
        """
        os.makedirs(model_dir, exist_ok=True)
        
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                os.path.join(model_dir, 'best_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        return callbacks
    
    def evaluate(self, test_generator) -> dict:
        """
        Evaluate the model on test data
        
        Args:
            test_generator: Test data generator
            
        Returns:
            Dictionary of evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not created or loaded.")
        
        print("=" * 60)
        print("Evaluating Model...")
        print("=" * 60)
        
        results = self.model.evaluate(test_generator, verbose=1)
        
        metrics = {
            'loss': results[0],
            'accuracy': results[1],
            'precision': results[2],
            'recall': results[3]
        }
        
        # Calculate F1 score
        if metrics['precision'] + metrics['recall'] > 0:
            metrics['f1_score'] = 2 * (metrics['precision'] * metrics['recall']) / \
                                 (metrics['precision'] + metrics['recall'])
        else:
            metrics['f1_score'] = 0.0
        
        print("\n" + "=" * 60)
        print("Evaluation Metrics:")
        print("=" * 60)
        for metric, value in metrics.items():
            print(f"{metric.capitalize()}: {value:.4f}")
        
        return metrics
    
    def predict(self, image_array: np.ndarray) -> Tuple[int, float, dict]:
        """
        Make prediction on a single image
        
        Args:
            image_array: Preprocessed image array
            
        Returns:
            Tuple of (predicted_class_index, confidence, all_probabilities)
        """
        if self.model is None:
            raise ValueError("Model not created or loaded.")
        
        predictions = self.model.predict(image_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        probabilities = {i: float(prob) for i, prob in enumerate(predictions[0])}
        
        return predicted_class, confidence, probabilities
    
    def predict_batch(self, images_array: np.ndarray) -> np.ndarray:
        """
        Make predictions on a batch of images
        
        Args:
            images_array: Batch of preprocessed images
            
        Returns:
            Array of predictions
        """
        if self.model is None:
            raise ValueError("Model not created or loaded.")
        
        return self.model.predict(images_array, verbose=0)
    
    def save_model(self, 
                   filepath: str,
                   save_format: str = 'h5',
                   include_metadata: bool = True):
        """
        Save the trained model
        
        Args:
            filepath: Path to save the model
            save_format: Format to save ('h5' or 'tf')
            include_metadata: Whether to save metadata
        """
        if self.model is None:
            raise ValueError("No model to save.")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if save_format == 'h5':
            self.model.save(filepath)
        elif save_format == 'tf':
            self.model.save(filepath, save_format='tf')
        else:
            raise ValueError("save_format must be 'h5' or 'tf'")
        
        print(f"Model saved to: {filepath}")
        
        # Save metadata
        if include_metadata:
            metadata = {
                'img_size': self.img_size,
                'num_classes': self.num_classes,
                'learning_rate': self.learning_rate,
                'saved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            metadata_path = filepath.replace('.h5', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            print(f"Metadata saved to: {metadata_path}")
    
    def load_model(self, filepath: str):
        """
        Load a trained model (supports both .h5 and .keras formats)
        
        Args:
            filepath: Path to the model file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        try:
            # For .h5 files with Keras 3, use safe_mode=False
            if filepath.endswith('.h5'):
                self.model = keras.models.load_model(filepath, safe_mode=False, compile=False)
            else:
                self.model = keras.models.load_model(filepath, compile=False)
            
            # Recompile the model with current configuration
            self.model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
                loss='categorical_crossentropy',
                metrics=['accuracy',
                         keras.metrics.Precision(name='precision'),
                         keras.metrics.Recall(name='recall')]
            )
            print(f"Model loaded from: {filepath}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
        
        # Load metadata if available
        metadata_path = filepath.replace('.h5', '_metadata.json').replace('.keras', '_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                self.img_size = tuple(metadata.get('img_size', self.img_size))
                self.num_classes = metadata.get('num_classes', self.num_classes)
                self.learning_rate = metadata.get('learning_rate', self.learning_rate)
            print(f"Metadata loaded from: {metadata_path}")
    
    def get_model_summary(self) -> str:
        """
        Get model architecture summary
        
        Returns:
            String representation of model summary
        """
        if self.model is None:
            raise ValueError("Model not created or loaded.")
        
        from io import StringIO
        import sys
        
        stream = StringIO()
        self.model.summary(print_fn=lambda x: stream.write(x + '\n'))
        return stream.getvalue()


if __name__ == "__main__":
    # Test the classifier
    classifier = ImageClassifier(img_size=(224, 224), num_classes=2)
    model = classifier.create_model()
    print("\nImageClassifier initialized successfully!")
    print(f"Model created with {model.count_params():,} parameters")
