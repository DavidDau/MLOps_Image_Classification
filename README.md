# Image Classification MLOps Pipeline

A comprehensive end-to-end machine learning pipeline for image classification featuring automated retraining, model monitoring, and scalable deployment using Docker.

**[ Click here to watch the demonstration video](https://youtu.be/jbuXZ30CwvA)**

## Live Demo

**Application URL**: [Add your deployed URL here if applicable]

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Model Information](#model-information)
- [Load Testing Results](#load-testing-results)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Description

This project implements a complete MLOps pipeline for leaf disease classification using Transfer Learning with MobileNetV2. The system includes:

- **Model Training**: Jupyter notebook with comprehensive preprocessing, training, and evaluation
- **Web Application**: Flask-based UI for predictions, visualizations, and retraining
- **Automated Retraining**: Upload new data and retrain the model with a single click
- **System Monitoring**: Real-time monitoring of model uptime and system resources
- **Containerized Deployment**: Docker and Docker Compose for easy deployment
- **Load Testing**: Locust-based performance testing and scalability analysis

## Features

### 1. **Single Image Prediction**

- Upload any image and get instant classification
- Confidence scores for all classes
- Visual probability distribution

### 2. **Data Visualizations**

- Interactive charts showing dataset distribution
- Prediction statistics and trends
- Model performance insights

### 3. **Bulk Data Upload**

- Upload multiple images at once
- Organize by class/category
- Automatic validation and preprocessing

### 4. **One-Click Model Retraining**

- Trigger retraining with updated data
- Uses previous model as pretrained base
- Real-time progress tracking
- Automatic model reload

### 5. **System Monitoring**

- Model uptime tracking
- CPU, Memory, and Disk usage
- Prediction statistics
- Health checks

### 6. **RESTful API**

- `/api/predict` - Make predictions
- `/api/metrics` - Get system metrics
- `/api/retrain_status` - Check retraining progress

## Project Structure

```
MLOps_Image_Classification/
│
├── README.md                          # This file
│
├── notebook/
│   └── image_classification.ipynb     # Model training notebook
│
├── src/
│   ├── preprocessing.py               # Data preprocessing utilities
│   ├── model.py                       # Model architecture and training
│   └── prediction.py                  # Prediction service
│
├── app/
│   ├── app.py                         # Flask web application
│   ├── templates/                     # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── predict.html
│   │   ├── visualizations.html
│   │   ├── upload_data.html
│   │   ├── retrain.html
│   │   └── monitoring.html
│   └── static/
│       └── css/
│           └── style.css
│
├── data/
│   ├── train/                         # Training images (organized by class)
│   ├── test/                          # Test images
│   └── uploaded/                      # User-uploaded images
│
├── models/
│   ├── image_classifier_model.h5      # Trained model
│   └── class_indices.json             # Class label mappings
│
├── deployment/
│   ├── Dockerfile                     # Docker configuration
│   ├── docker-compose.yml             # Multi-container setup
│   ├── nginx.conf                     # Nginx reverse proxy config
│   ├── deploy.sh                      # Deployment script (Linux/Mac)
│   └── deploy.ps1                     # Deployment script (Windows)
│
├── locust/
│   ├── locustfile.py                  # Load testing script
│   └── LOAD_TEST_RESULTS.md           # Test results template
│
└── requirements.txt                   # Python dependencies
```

## Technologies Used

### Machine Learning & Data Science

- **TensorFlow/Keras** - Deep learning framework
- **MobileNetV2** - Pretrained model for transfer learning
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Data visualization
- **Scikit-learn** - ML utilities and metrics

### Web Development

- **Flask** - Web framework
- **HTML/CSS/JavaScript** - Frontend
- **Bootstrap 5** - UI framework
- **Chart.js** - Interactive charts

### DevOps & Deployment

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy
- **Locust** - Load testing

### Monitoring & Utilities

- **psutil** - System monitoring
- **Pillow (PIL)** - Image processing

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker and Docker Compose (for containerized deployment)
- At least 4GB RAM
- 10GB free disk space

### Option 1: Local Setup (Development)

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd MLOps_Image_Classification
   ```

2. **Create a virtual environment**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the dataset**

   - Download a Cats vs Dogs dataset or use your own images
   - Organize images into folders:
     ```
     data/train/cats/    # Cat images for training
     data/train/dogs/    # Dog images for training
     data/test/cats/     # Cat images for testing
     data/test/dogs/     # Dog images for testing
     ```

5. **Train the model**

   ```bash
   # Open and run the Jupyter notebook
   jupyter notebook notebook/image_classification.ipynb
   ```

   Run all cells to train the model. This will create:

   - `models/image_classifier_model.h5`
   - `models/class_indices.json`

6. **Run the web application**
   ```bash
   python app/app.py
   ```
   Access at: http://localhost:5000

### Option 2: Docker Deployment (Production)

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd MLOps_Image_Classification
   ```

2. **Ensure you have trained the model**

   - The model files must exist in the `models/` directory
   - If not, train the model using the Jupyter notebook first

3. **Build and deploy with Docker Compose**

   **Windows (PowerShell):**

   ```powershell
   .\deployment\deploy.ps1
   ```

   **Linux/Mac:**

   ```bash
   chmod +x deployment/deploy.sh
   ./deployment/deploy.sh
   ```

   **Or manually:**

   ```bash
   docker-compose -f deployment/docker-compose.yml up -d --build
   ```

4. **Access the application**

   - Direct access: http://localhost:5000
   - Via Nginx: http://localhost:80

5. **View logs**

   ```bash
   docker-compose -f deployment/docker-compose.yml logs -f
   ```

6. **Stop the application**
   ```bash
   docker-compose -f deployment/docker-compose.yml down
   ```

### Option 3: Quick Dataset Setup

If you don't have a dataset ready:

1. **Download Kaggle Cats and Dogs dataset**

   ```bash
   # Using Kaggle API
   pip install kaggle
   kaggle datasets download -d salader/dogs-vs-cats
   unzip dogs-vs-cats.zip -d data/
   ```

2. **Or use a sample dataset**
   - Collect ~200 cat images and ~200 dog images from the internet
   - Organize them as shown in the dataset structure above

## Usage

### 1. Making Predictions

**Via Web Interface:**

1. Navigate to http://localhost:5000/predict
2. Upload an image (PNG, JPG, JPEG, GIF, BMP)
3. Click "Predict"
4. View results with confidence scores

**Via API:**

```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5000/api/predict
```

**Via Python:**

```python
from src.prediction import PredictionService

service = PredictionService(
    model_path='models/image_classifier_model.h5',
    class_indices_path='models/class_indices.json'
)

result = service.predict_image('path/to/image.jpg')
print(result)
```

### 2. Viewing Visualizations

1. Navigate to http://localhost:5000/visualizations
2. Explore:
   - Training dataset distribution
   - Prediction statistics
   - Class distribution insights

### 3. Uploading Training Data

1. Navigate to http://localhost:5000/upload_data
2. Select the class/category
3. Choose multiple images
4. Click "Upload Images"

### 4. Retraining the Model

1. Navigate to http://localhost:5000/retrain
2. Click "Start Retraining"
3. Monitor progress in real-time
4. Wait for completion (~5-30 minutes depending on data size)

### 5. Monitoring System Health

1. Navigate to http://localhost:5000/monitoring
2. View:
   - Model uptime
   - CPU/Memory/Disk usage
   - Prediction statistics
   - Retraining status

## Model Information

### Architecture

**Base Model**: MobileNetV2 (Pretrained on ImageNet)

**Custom Layers**:

- Global Average Pooling
- Batch Normalization
- Dense (256 units, ReLU, L2 regularization, Dropout 0.5)
- Dense (128 units, ReLU, L2 regularization, Dropout 0.3)
- Dense (2 units, Softmax)

### Training Details

**Optimization Techniques**:

1. Transfer Learning with MobileNetV2
2. Data Augmentation (rotation, flipping, zooming, shifting)
3. Regularization (L2 and Dropout)
4. Batch Normalization
5. Early Stopping
6. Learning Rate Reduction on Plateau
7. Two-phase Training (frozen → fine-tuning)
8. Adam Optimizer

**Hyperparameters**:

- Image Size: 224x224
- Batch Size: 32
- Initial Learning Rate: 0.0001
- Epochs: 50 (with early stopping)

### Evaluation Metrics

The model is evaluated using:

- **Accuracy**: Overall correctness
- **Loss**: Cross-entropy loss
- **Precision**: True positives / Predicted positives
- **Recall**: True positives / Actual positives
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Visual representation of predictions

## Load Testing Results

### Test Configuration

Load testing performed using Locust with the following scenarios:

| Scenario    | Users | Spawn Rate | Duration | Results                    |
| ----------- | ----- | ---------- | -------- | -------------------------- |
| Light Load  | 10    | 2/sec      | 2 min    | [See LOAD_TEST_RESULTS.md] |
| Normal Load | 50    | 5/sec      | 5 min    | [See LOAD_TEST_RESULTS.md] |
| Heavy Load  | 100   | 10/sec     | 5 min    | [See LOAD_TEST_RESULTS.md] |
| Peak Load   | 200   | 20/sec     | 3 min    | [See LOAD_TEST_RESULTS.md] |

### Running Load Tests

```bash
# Navigate to locust directory
cd locust

# Run with web interface
locust -f locustfile.py --host=http://localhost:5000

# Run headless
locust -f locustfile.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 --run-time 5m --headless
```

**Detailed results**: See [locust/LOAD_TEST_RESULTS.md](locust/LOAD_TEST_RESULTS.md)

### Performance with Multiple Containers

Test with different numbers of containers:

```bash
# Scale to 2 containers
docker-compose -f deployment/docker-compose.yml up -d --scale web=2

# Scale to 4 containers
docker-compose -f deployment/docker-compose.yml up -d --scale web=4
```

## API Documentation

### Endpoints

#### `GET /`

Home page with system overview

#### `GET /predict`

Prediction page (Web UI)

#### `POST /predict`

Submit image for prediction (Web Form)

#### `POST /api/predict`

**Description**: Make a prediction on an uploaded image

**Request**:

- Method: POST
- Content-Type: multipart/form-data
- Body: file (image file)

**Response**:

```json
{
  "success": true,
  "predicted_class": "cat",
  "predicted_index": 0,
  "confidence": 0.9523,
  "probabilities": {
    "cat": 0.9523,
    "dog": 0.0477
  },
  "filename": "test.jpg",
  "timestamp": "2025-11-25T10:30:00"
}
```

#### `GET /api/metrics`

**Description**: Get system metrics

**Response**:

```json
{
  "cpu_percent": 45.2,
  "memory_percent": 62.8,
  "disk_percent": 38.5,
  "uptime": "2d 5h 23m 15s"
}
```

#### `GET /api/retrain_status`

**Description**: Get retraining status

**Response**:

```json
{
  "is_running": true,
  "progress": 65,
  "message": "Retraining model...",
  "last_retrain_time": "2025-11-25T08:15:00"
}
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**David CYUBAHIRO**

- GitHub: [@DavidDau](https://github.com/DavidDau)
- LinkedIn: [David CYUBAHIRO](https://linkedin.com/in/davidcyubahiro)

## Acknowledgments

- MobileNetV2 architecture by Google
- Flask framework
- TensorFlow/Keras team
- Bootstrap for UI components
- Locust for load testing

## Contact

For questions or support, please contact: davidcyubahiro53@gmail.com

## Links

- **Video Demo**: [YouTube Link](https://youtu.be/jbuXZ30CwvA)
- **Documentation**: This README
- **Load Test Results**: [locust/LOAD_TEST_RESULTS.md](locust/LOAD_TEST_RESULTS.md)
