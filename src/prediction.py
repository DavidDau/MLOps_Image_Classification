"""
Prediction Module

This module handles:
- Single image predictions
- Batch predictions
- Prediction result formatting
"""

import numpy as np
import json
import os
from typing import Dict, List, Tuple
from datetime import datetime

from model import ImageClassifier
from preprocessing import ImagePreprocessor


class PredictionService:
    """
    Service for making predictions with the trained model
    """
    
    def __init__(self, 
                 model_path: str,
                 class_indices_path: str,
                 img_size: Tuple[int, int] = (128, 128)):  # Updated default to match training
        """
        Initialize the prediction service
        
        Args:
            model_path: Path to trained model file
            class_indices_path: Path to class indices JSON file
            img_size: Input image size (should match training size)
        """
        self.img_size = img_size
        
        # Load model
        self.classifier = ImageClassifier(img_size=img_size)
        self.classifier.load_model(model_path)
        
        # Load class indices
        with open(class_indices_path, 'r') as f:
            self.class_indices = json.load(f)
        
        # Create reverse mapping (index to class name)
        self.index_to_class = {v: k for k, v in self.class_indices.items()}
        
        # Initialize preprocessor
        self.preprocessor = ImagePreprocessor(img_size=img_size)
        
        print(f"Prediction service initialized!")
        print(f"Classes: {list(self.class_indices.keys())}")
    
    def predict_image(self, image_path: str) -> Dict:
        """
        Predict class for a single image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Preprocess image
            img_array = self.preprocessor.preprocess_single_image(image_path)
            
            # Make prediction
            predicted_idx, confidence, probabilities = self.classifier.predict(img_array)
            
            # Format results
            result = {
                'success': True,
                'predicted_class': self.index_to_class[predicted_idx],
                'predicted_index': int(predicted_idx),
                'confidence': float(confidence),
                'probabilities': {
                    self.index_to_class[idx]: float(prob)
                    for idx, prob in probabilities.items()
                },
                'image_path': image_path,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'image_path': image_path,
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_uploaded_image(self, image_file) -> Dict:
        """
        Predict class for an uploaded image file
        
        Args:
            image_file: Uploaded file object (e.g., from Flask request)
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Preprocess uploaded image
            img_array = self.preprocessor.preprocess_uploaded_image(image_file)
            
            # Make prediction
            predicted_idx, confidence, probabilities = self.classifier.predict(img_array)
            
            # Format results
            result = {
                'success': True,
                'predicted_class': self.index_to_class[predicted_idx],
                'predicted_index': int(predicted_idx),
                'confidence': float(confidence),
                'probabilities': {
                    self.index_to_class[idx]: float(prob)
                    for idx, prob in probabilities.items()
                },
                'filename': getattr(image_file, 'filename', 'unknown'),
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'filename': getattr(image_file, 'filename', 'unknown'),
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_batch(self, image_paths: List[str]) -> List[Dict]:
        """
        Predict classes for multiple images
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of prediction result dictionaries
        """
        results = []
        
        for image_path in image_paths:
            result = self.predict_image(image_path)
            results.append(result)
        
        return results
    
    def get_top_k_predictions(self, 
                             image_path: str, 
                             k: int = 3) -> Dict:
        """
        Get top-k predictions for an image
        
        Args:
            image_path: Path to image file
            k: Number of top predictions to return
            
        Returns:
            Dictionary with top-k predictions
        """
        try:
            # Preprocess image
            img_array = self.preprocessor.preprocess_single_image(image_path)
            
            # Make prediction
            _, _, probabilities = self.classifier.predict(img_array)
            
            # Sort by probability
            sorted_probs = sorted(probabilities.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)[:k]
            
            # Format results
            top_k = [
                {
                    'class': self.index_to_class[idx],
                    'probability': float(prob)
                }
                for idx, prob in sorted_probs
            ]
            
            result = {
                'success': True,
                'top_predictions': top_k,
                'image_path': image_path,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'image_path': image_path,
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_with_threshold(self, 
                              image_path: str, 
                              threshold: float = 0.5) -> Dict:
        """
        Predict with a confidence threshold
        
        Args:
            image_path: Path to image file
            threshold: Minimum confidence threshold (0-1)
            
        Returns:
            Dictionary with prediction results
        """
        result = self.predict_image(image_path)
        
        if result['success']:
            if result['confidence'] < threshold:
                result['prediction_status'] = 'uncertain'
                result['message'] = f"Confidence {result['confidence']:.2%} below threshold {threshold:.2%}"
            else:
                result['prediction_status'] = 'confident'
        
        return result
    
    def save_prediction_log(self, 
                           prediction_result: Dict, 
                           log_path: str = 'prediction_log.json'):
        """
        Save prediction result to a log file
        
        Args:
            prediction_result: Prediction result dictionary
            log_path: Path to log file
        """
        try:
            # Load existing logs
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Append new prediction
            logs.append(prediction_result)
            
            # Save updated logs
            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=4)
            
            print(f"Prediction logged to {log_path}")
            
        except Exception as e:
            print(f"Error saving prediction log: {str(e)}")
    
    def get_prediction_statistics(self, 
                                  log_path: str = 'prediction_log.json') -> Dict:
        """
        Get statistics from prediction logs
        
        Args:
            log_path: Path to log file
            
        Returns:
            Dictionary with statistics
        """
        try:
            if not os.path.exists(log_path):
                return {'error': 'No prediction logs found'}
            
            with open(log_path, 'r') as f:
                logs = json.load(f)
            
            # Calculate statistics
            total_predictions = len(logs)
            successful_predictions = sum(1 for log in logs if log.get('success', False))
            
            # Class distribution
            class_counts = {}
            confidences = []
            
            for log in logs:
                if log.get('success', False):
                    pred_class = log.get('predicted_class')
                    if pred_class:
                        class_counts[pred_class] = class_counts.get(pred_class, 0) + 1
                    
                    confidence = log.get('confidence')
                    if confidence is not None:
                        confidences.append(confidence)
            
            stats = {
                'total_predictions': total_predictions,
                'successful_predictions': successful_predictions,
                'failed_predictions': total_predictions - successful_predictions,
                'class_distribution': class_counts,
                'average_confidence': np.mean(confidences) if confidences else 0,
                'min_confidence': np.min(confidences) if confidences else 0,
                'max_confidence': np.max(confidences) if confidences else 0
            }
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}


def predict_from_cli(model_path: str, 
                    class_indices_path: str,
                    image_path: str):
    """
    Command-line interface for making predictions
    
    Args:
        model_path: Path to trained model
        class_indices_path: Path to class indices JSON
        image_path: Path to image to predict
    """
    # Initialize prediction service
    service = PredictionService(model_path, class_indices_path)
    
    # Make prediction
    result = service.predict_image(image_path)
    
    # Print results
    print("\n" + "=" * 60)
    print("PREDICTION RESULTS")
    print("=" * 60)
    
    if result['success']:
        print(f"\nImage: {result['image_path']}")
        print(f"Predicted Class: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nAll Probabilities:")
        for class_name, prob in result['probabilities'].items():
            print(f"  {class_name}: {prob:.2%}")
    else:
        print(f"\nError: {result['error']}")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 4:
        model_path = sys.argv[1]
        class_indices_path = sys.argv[2]
        image_path = sys.argv[3]
        
        predict_from_cli(model_path, class_indices_path, image_path)
    else:
        print("Usage: python prediction.py <model_path> <class_indices_path> <image_path>")
        print("\nExample:")
        print("python prediction.py ../models/image_classifier_model.h5 ../models/class_indices.json ../data/test/cat.jpg")
