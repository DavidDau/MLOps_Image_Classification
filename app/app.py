"""
Flask Web Application for Image Classification MLOps Pipeline

Features:
- Single image prediction
- Data visualizations
- Bulk data upload for retraining
- Trigger model retraining
- Model uptime monitoring
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sys
import json
import time
from datetime import datetime
import threading
import psutil

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from prediction import PredictionService
from model import ImageClassifier
from preprocessing import ImagePreprocessor, preprocess_for_retraining

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploaded')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')
# Prefer .keras format for Keras 3 compatibility, fallback to .h5
MODEL_PATH_KERAS = os.path.join(MODEL_DIR, 'image_classifier_model.keras')
MODEL_PATH_H5 = os.path.join(MODEL_DIR, 'image_classifier_model.h5')
MODEL_PATH = MODEL_PATH_KERAS if os.path.exists(MODEL_PATH_KERAS) else MODEL_PATH_H5
CLASS_INDICES_PATH = os.path.join(BASE_DIR, '..', 'models', 'class_indices.json')
TRAIN_DIR = os.path.join(BASE_DIR, '..', 'data', 'train')
PREDICTION_LOG_PATH = os.path.join(BASE_DIR, '..', 'logs', 'predictions.json')

# Global variables
prediction_service = None
model_start_time = None
is_retraining = False
retraining_status = {
    'is_running': False,
    'progress': 0,
    'message': '',
    'last_retrain_time': None
}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.dirname(PREDICTION_LOG_PATH), exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def initialize_model():
    """Initialize the prediction service"""
    global prediction_service, model_start_time
    
    if not os.path.exists(MODEL_PATH):
        print("Warning: Model file not found. Please train the model first.")
        return False
    
    try:
        prediction_service = PredictionService(
            model_path=MODEL_PATH,
            class_indices_path=CLASS_INDICES_PATH
        )
        model_start_time = datetime.now()
        print("Model initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        return False


def get_model_uptime():
    """Get model uptime"""
    if model_start_time is None:
        return "Model not loaded"
    
    uptime = datetime.now() - model_start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{days}d {hours}h {minutes}m {seconds}s"


def get_system_metrics():
    """Get system metrics for monitoring"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'uptime': get_model_uptime()
    }


@app.route('/')
def index():
    """Home page"""
    metrics = get_system_metrics()
    return render_template('index.html', metrics=metrics)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Single image prediction page"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Make prediction
                result = prediction_service.predict_uploaded_image(file)
                
                # Save to log
                prediction_service.save_prediction_log(result, PREDICTION_LOG_PATH)
                
                # Reset file pointer to save the image
                file.seek(0)
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                return render_template('predict.html', 
                                      result=result,
                                      image_url=url_for('static', filename=f'../data/uploaded/{filename}'))
            
            except Exception as e:
                flash(f'Error making prediction: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Allowed: png, jpg, jpeg, gif, bmp', 'error')
            return redirect(request.url)
    
    return render_template('predict.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    try:
        result = prediction_service.predict_uploaded_image(file)
        prediction_service.save_prediction_log(result, PREDICTION_LOG_PATH)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/visualizations')
def visualizations():
    """Data visualizations page"""
    try:
        # Load training data statistics
        stats = get_dataset_statistics()
        
        # Load prediction statistics
        pred_stats = prediction_service.get_prediction_statistics(PREDICTION_LOG_PATH)
        
        return render_template('visualizations.html', 
                             stats=stats,
                             pred_stats=pred_stats)
    except Exception as e:
        flash(f'Error loading visualizations: {str(e)}', 'error')
        return render_template('visualizations.html', stats={}, pred_stats={})


@app.route('/upload_data', methods=['GET', 'POST'])
def upload_data():
    """Bulk data upload for retraining"""
    if request.method == 'POST':
        # Check if files were uploaded
        if 'files' not in request.files:
            flash('No files uploaded', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        class_label = request.form.get('class_label', 'unknown')
        
        if not files or files[0].filename == '':
            flash('No files selected', 'error')
            return redirect(request.url)
        
        uploaded_count = 0
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Save to class-specific folder
                class_dir = os.path.join(TRAIN_DIR, class_label)
                os.makedirs(class_dir, exist_ok=True)
                
                filepath = os.path.join(class_dir, filename)
                file.save(filepath)
                uploaded_count += 1
        
        flash(f'Successfully uploaded {uploaded_count} images to class: {class_label}', 'success')
        return redirect(url_for('upload_data'))
    
    # Get available classes
    classes = []
    if os.path.exists(TRAIN_DIR):
        classes = [d for d in os.listdir(TRAIN_DIR) 
                  if os.path.isdir(os.path.join(TRAIN_DIR, d))]
    
    return render_template('upload_data.html', classes=classes)


@app.route('/retrain', methods=['GET', 'POST'])
def retrain():
    """Model retraining page"""
    global retraining_status
    
    if request.method == 'POST':
        if retraining_status['is_running']:
            flash('Retraining already in progress', 'warning')
            return redirect(url_for('retrain'))
        
        # Start retraining in background thread
        thread = threading.Thread(target=perform_retraining)
        thread.daemon = True
        thread.start()
        
        flash('Retraining started! This may take several minutes.', 'info')
        return redirect(url_for('retrain'))
    
    return render_template('retrain.html', status=retraining_status)


@app.route('/api/retrain_status')
def api_retrain_status():
    """API endpoint to check retraining status"""
    return jsonify(retraining_status)


def perform_retraining():
    """Perform model retraining in background"""
    global retraining_status, prediction_service
    
    try:
        retraining_status['is_running'] = True
        retraining_status['progress'] = 0
        retraining_status['message'] = 'Initializing retraining...'
        
        # Create preprocessor and classifier
        preprocessor = ImagePreprocessor(img_size=(224, 224))
        classifier = ImageClassifier(img_size=(224, 224), num_classes=2)
        
        retraining_status['progress'] = 10
        retraining_status['message'] = 'Loading data...'
        
        # Load training data
        train_generator, val_generator = preprocessor.create_train_generator(
            TRAIN_DIR,
            batch_size=32,
            validation_split=0.2
        )
        
        retraining_status['progress'] = 30
        retraining_status['message'] = 'Retraining model...'
        
        # Retrain model
        classifier.retrain(
            train_generator,
            val_generator,
            pretrained_model_path=MODEL_PATH,
            epochs=10
        )
        
        retraining_status['progress'] = 80
        retraining_status['message'] = 'Saving retrained model...'
        
        # Save retrained model
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_model_path = MODEL_PATH.replace('.h5', f'_retrained_{timestamp}.h5')
        classifier.save_model(new_model_path)
        
        # Update main model
        classifier.save_model(MODEL_PATH)
        
        retraining_status['progress'] = 90
        retraining_status['message'] = 'Reloading model...'
        
        # Reload prediction service
        initialize_model()
        
        retraining_status['progress'] = 100
        retraining_status['message'] = 'Retraining completed successfully!'
        retraining_status['last_retrain_time'] = datetime.now().isoformat()
        
    except Exception as e:
        retraining_status['message'] = f'Error during retraining: {str(e)}'
        retraining_status['progress'] = 0
    
    finally:
        retraining_status['is_running'] = False


@app.route('/monitoring')
def monitoring():
    """Model monitoring and uptime page"""
    metrics = get_system_metrics()
    
    # Get prediction statistics
    pred_stats = {}
    if prediction_service:
        pred_stats = prediction_service.get_prediction_statistics(PREDICTION_LOG_PATH)
    
    return render_template('monitoring.html', 
                         metrics=metrics,
                         pred_stats=pred_stats,
                         retrain_status=retraining_status)


def get_dataset_statistics():
    """Get statistics about the training dataset"""
    stats = {
        'classes': {},
        'total_images': 0
    }
    
    if not os.path.exists(TRAIN_DIR):
        return stats
    
    for class_name in os.listdir(TRAIN_DIR):
        class_path = os.path.join(TRAIN_DIR, class_name)
        if os.path.isdir(class_path):
            count = len([f for f in os.listdir(class_path) 
                        if allowed_file(f)])
            stats['classes'][class_name] = count
            stats['total_images'] += count
    
    return stats


@app.route('/api/metrics')
def api_metrics():
    """API endpoint for system metrics"""
    metrics = get_system_metrics()
    return jsonify(metrics)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Initialize model on startup
    if initialize_model():
        print("Starting Flask application...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to initialize model. Please train the model first.")
        print("Run the Jupyter notebook to train the model.")
