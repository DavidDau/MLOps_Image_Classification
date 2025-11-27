# Quick Setup Guide

This guide will help you get started quickly with the MLOps Image Classification project.

## Quick Start (5 minutes)

### Step 1: Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd MLOps_Image_Classification

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get Sample Data

**Option A: Use provided script (recommended)**

```bash
python scripts/download_sample_data.py
```

**Option B: Use Kaggle dataset**

```bash
# Install Kaggle CLI
pip install kaggle

# Download Cats vs Dogs
kaggle datasets download -d salader/dogs-vs-cats
unzip dogs-vs-cats.zip -d data/
```

**Option C: Manual setup**

- Create folders: `data/train/cats/`, `data/train/dogs/`, `data/test/cats/`, `data/test/dogs/`
- Add at least 100 images per class to train folders
- Add at least 20 images per class to test folders

### Step 3: Train the Model

```bash
# Start Jupyter Notebook
jupyter notebook

# Open: notebook/image_classification.ipynb
# Run all cells (this will take 15-30 minutes)
```

This creates:

- `models/image_classifier_model.h5`
- `models/class_indices.json`

### Step 4: Run the Application

```bash
# Start the Flask app
python app/app.py
```

Open your browser: http://localhost:5000

### Step 5: Test Load Performance (Optional)

```bash
# In a new terminal, activate venv and run:
cd locust
locust -f locustfile.py --host=http://localhost:5000

# Open: http://localhost:8089
# Set users: 50, spawn rate: 5
# Click "Start swarming"
```

## Docker Quick Start (3 minutes)

### Prerequisites

- Docker Desktop installed and running
- Model already trained (or use pre-trained model)

### Steps

```bash
# Clone repository
git clone <your-repo-url>
cd MLOps_Image_Classification

# Build and run with Docker Compose
docker-compose -f deployment/docker-compose.yml up -d --build

# Wait for ~30 seconds for startup
# Access: http://localhost:5000
```

## Checklist

Before submitting, ensure you have:

- [ ] Trained model files in `models/` directory
- [ ] Jupyter notebook executed with all cells run and outputs visible
- [ ] README.md updated with your information
- [ ] Video demo recorded and uploaded to YouTube
- [ ] YouTube link added to README.md
- [ ] Load test performed and results documented
- [ ] Screenshots/evidence of working application
- [ ] Git repository is public or accessible
- [ ] All requirements from rubric are met

## Meeting Rubric Requirements

### Video Demo (5 points)

- Record screen with camera on
- Show prediction process (upload image, get result)
- Show retraining process (upload data, trigger retrain)
- Duration: 3-5 minutes

### Retraining Process (10 points)

Your project includes:

1. Data file uploading and saving (`/upload_data` page)
2. Data preprocessing of uploaded data (preprocessing.py)
3. Retraining using custom model as pretrained (`/retrain` page, model.py)

### Prediction Process (10 points)

Your project includes:

1. Image upload for prediction (`/predict` page)
2. Displays correct prediction with confidence (prediction.py)

### Evaluation of Models (10 points)

Your notebook includes:

1. Clear preprocessing steps
2. Optimization techniques (transfer learning, regularization, early stopping, etc.)
3. 4+ evaluation metrics (accuracy, loss, precision, recall, F1-score, confusion matrix)

### Deployment Package (10 points)

Your project includes:

1. Web UI (Flask application)
2. Data insights/visualizations (`/visualizations` page)
3. Dockerized deployment (Dockerfile, docker-compose.yml)

## Recording Your Video Demo

### Tools

- **Windows**: OBS Studio, ShareX, Windows Game Bar (Win+G)
- **Mac**: QuickTime Player, ScreenFlow
- **Linux**: OBS Studio, SimpleScreenRecorder

### Script Template

```
[Introduction - 30 seconds]
"Hello, I'm [Your Name]. This is my MLOps Image Classification project
demonstrating a complete ML pipeline with automated retraining."

[Show Application - 1 minute]
- Navigate to home page
- Show monitoring dashboard
- Explain the features

[Prediction Demo - 1 minute]
- Go to Predict page
- Upload a cat/dog image
- Show the prediction result with confidence scores
- Upload another image to show it works consistently

[Upload Data - 30 seconds]
- Go to Upload Data page
- Select class (e.g., cats)
- Upload 3-5 sample images
- Show success message

[Retraining Demo - 1.5 minutes]
- Go to Retrain page
- Click "Start Retraining"
- Show progress bar
- Explain what's happening
- Wait for or fast-forward to completion

[Visualizations - 30 seconds]
- Show dataset distribution charts
- Show prediction statistics

[Conclusion - 30 seconds]
"This completes the demonstration of prediction and retraining processes.
The system successfully uploads data, preprocesses it, and retrains
using the existing model as a pretrained base. Thank you!"
```

## Troubleshooting

### Model not found error

```bash
# Make sure you've trained the model first
jupyter notebook notebook/image_classification.ipynb
# Run all cells
```

### Port already in use

```bash
# Change port in app/app.py or kill the process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### Docker build fails

```bash
# Clear Docker cache and rebuild
docker system prune -a
docker-compose -f deployment/docker-compose.yml build --no-cache
```

### Out of memory during training

- Reduce batch size in notebook (e.g., from 32 to 16)
- Reduce number of training images
- Close other applications

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the code comments in each file
- Check error logs in `logs/` directory

## Time Estimates

- Setup environment: 5 minutes
- Download data: 5-10 minutes
- Train model: 15-30 minutes (depending on hardware)
- Test application: 5 minutes
- Record video: 10-15 minutes
- Load testing: 5-10 minutes
- **Total**: ~1-2 hours

Good luck!
