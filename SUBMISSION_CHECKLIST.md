# MLOps Project Submission Checklist

Use this checklist to ensure your project meets all requirements before submission.

## Pre-Submission Checklist

### Core Requirements

#### 1. Notebook (10 points)

- [ ] Jupyter notebook is present in `notebook/` directory
- [ ] All cells have been executed and show outputs
- [ ] Clear markdown documentation between code cells
- [ ] Preprocessing steps are well documented
- [ ] Data augmentation is implemented
- [ ] Model uses Transfer Learning (MobileNetV2)
- [ ] Optimization techniques implemented:
  - [ ] Regularization (L2, Dropout)
  - [ ] Early Stopping
  - [ ] Learning Rate Reduction
  - [ ] Batch Normalization
- [ ] At least 4 evaluation metrics:
  - [ ] Accuracy
  - [ ] Loss
  - [ ] Precision
  - [ ] Recall
  - [ ] F1-Score
  - [ ] Confusion Matrix
- [ ] Model saved as .h5 file
- [ ] Class indices saved as JSON

#### 2. Source Code (Must be present)

- [x] `src/preprocessing.py` exists and works
- [x] `src/model.py` exists and works
- [x] `src/prediction.py` exists and works
- [x] All Python files have proper documentation
- [x] Code follows best practices

#### 3. Prediction Process (10 points)

- [x] Can upload a single image
- [x] Prediction returns correct result
- [x] Confidence scores are displayed
- [x] Prediction page works smoothly
- [x] API endpoint `/api/predict` works
- [x] Error handling is implemented

#### 4. Retraining Process (10 points)

- [x] Data upload page exists (`/upload_data`)
- [x] Can upload multiple images at once
- [x] Images are saved to database/filesystem
- [x] Uploaded data is organized by class
- [x] Retraining page exists (`/retrain`)
- [x] Retraining uses pretrained model as base
- [x] Progress is shown during retraining
- [x] Model is automatically reloaded after retraining
- [x] Preprocessing is applied to uploaded data

#### 5. Deployment (10 points)

- [x] Web UI is functional (not just API)
- [x] UI includes:
  - [x] Home page
  - [x] Prediction page
  - [x] Visualizations page
  - [x] Upload data page
  - [x] Retrain page
  - [x] Monitoring page
- [x] Data visualizations are present:
  - [x] Dataset distribution chart
  - [x] Prediction statistics
  - [x] At least 3 data insights
- [x] Dockerfile exists and works
- [x] docker-compose.yml exists and works
- [x] Application can be deployed with Docker
- [x] Model uptime is tracked and displayed

#### 6. Load Testing (Required)

- [x] Locust script exists (`locust/locustfile.py`)
- [x] Load tests have been performed
- [x] Results are documented in `locust/LOAD_TEST_RESULTS.md`
- [x] Tests performed with different scenarios (25 users, 100% success)
- [x] Latency and response times are recorded
- [x] Tables/charts show performance metrics

#### 7. Video Demo (5 points)

- [x] Video has been recorded
- [x] Camera is ON during recording
- [x] Video shows prediction process:
  - [x] Uploading an image
  - [x] Getting prediction result
  - [x] Result is correct
- [x] Video shows retraining process:
  - [x] Uploading bulk data
  - [x] Triggering retraining
  - [x] Progress indication
- [x] **Video uploaded to YouTube**: https://youtu.be/jbuXZ30CwvA
- [x] Video duration: 10-15 minutes
- [x] Video uploaded to YouTube
- [x] Video link is public/accessible
- [x] Video link added to README.md

#### 8. Documentation

- [x] README.md is comprehensive
- [x] README includes:
  - [x] Project description
  - [x] Setup instructions (clear and detailed)
  - [x] Video demo link
  - [x] Technology stack
  - [x] Project structure
  - [x] Usage examples
  - [x] Load test results summary
  - [x] API documentation
- [x] requirements.txt is complete
- [x] All dependencies are listed
- [x] .gitignore is present

### File Structure Verification

```
MLOps_Image_Classification/
├── README.md (with video link)
├── requirements.txt
├── .gitignore
│
├── notebook/
│   └── image_classification.ipynb (with outputs)
│
├── src/
│   ├── preprocessing.py
│   ├── model.py
│   └── prediction.py
│
├── app/
│   ├── app.py
│   ├── templates/ (all HTML files)
│   └── static/ (CSS, JS)
│
├── data/
│   ├── train/ (with images)
│   └── test/ (with images)
│
├── models/
│   ├── image_classifier_model.h5 or .tf
│   └── class_indices.json
│
├── deployment/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── locust/
    ├── locustfile.py
    └── LOAD_TEST_RESULTS.md (filled out)
```

### Video Demo Content Checklist

Your video should demonstrate:

- [ ] **Introduction** (10-15 seconds)

  - [ ] Your name visible/mentioned
  - [ ] Camera is ON
  - [ ] Project overview

- [ ] **Application Overview** (30 seconds)

  - [ ] Show home page
  - [ ] Explain features briefly

- [ ] **Prediction Demo** (1-2 minutes)

  - [ ] Navigate to predict page
  - [ ] Upload an image (cat or dog)
  - [ ] Show prediction result
  - [ ] Confidence score is visible
  - [ ] Result is CORRECT
  - [ ] Try with another image

- [ ] **Upload Data Demo** (30-45 seconds)

  - [ ] Navigate to upload page
  - [ ] Select class
  - [ ] Upload multiple images
  - [ ] Show success message

- [ ] **Retraining Demo** (1-2 minutes)

  - [ ] Navigate to retrain page
  - [ ] Click start retraining button
  - [ ] Show progress bar/indicator
  - [ ] Explain process
  - [ ] Show completion (or fast-forward)

- [ ] **Visualizations** (30 seconds)

  - [ ] Show data visualizations
  - [ ] Mention insights

- [ ] **Conclusion** (10-15 seconds)
  - [ ] Summary
  - [ ] Thank you

### Testing Checklist

Before recording video, test:

- [ ] Application starts without errors
- [ ] Home page loads correctly
- [ ] Prediction works with multiple test images
- [ ] Upload data accepts files
- [ ] Retraining can be triggered
- [ ] Visualizations display charts
- [ ] Monitoring page shows metrics
- [ ] All links work
- [ ] No broken images or 404 errors

### Final Submission Checklist

#### First Attempt - ZIP File

- [ ] Create ZIP of entire project folder
- [ ] ZIP includes all required files
- [ ] ZIP size is reasonable (exclude large unnecessary files)
- [ ] Video link is in README
- [ ] Submit ZIP file

#### Second Attempt - GitHub Repository

- [ ] Create GitHub repository (public)
- [ ] Push all code to repository
- [ ] README.md displays correctly on GitHub
- [ ] All files are committed
- [ ] .gitignore working properly
- [ ] Repository link is accessible
- [ ] Submit GitHub URL

### Rubric Points Verification

Check your score estimate:

- [ ] **Video Demo** (5 points)

  - Camera ON, shows prediction and retraining: **5 points**
  - Camera OFF or missing one demo: **3 points**
  - Missing video: **1 point**

- [ ] **Retraining Process** (10 points)

  - All 3 components (upload, preprocess, retrain with pretrained): **10 points**
  - Missing 1 component: **7.5 points**
  - Missing 2 components: **5 points**
  - Missing all: **2.5 points**

- [ ] **Prediction Process** (10 points)

  - Works correctly with correct predictions: **10 points**
  - Works but incorrect predictions: **7.5 points**
  - Errors/unresponsive: **5 points**
  - Not demonstrated: **2.5 points**

- [ ] **Evaluation of Models** (10 points)

  - Clear preprocessing + optimization + 4+ metrics: **10 points**
  - Good but missing some metrics: **7.5 points**
  - Unclear preprocessing or no optimization: **5 points**
  - Multiple errors or missing eval: **2.5 points**

- [ ] **Deployment Package** (10 points)
  - Web UI + data insights + Docker: **10 points**
  - API instead of UI or missing insights: **7 points**
  - Just Python scripts in terminal: **5 points**
  - Nothing deployed: **2 points**

**Estimated Total**: **\_** / 45 points

### Ready to Submit?

- [ ] All checklist items above are checked
- [ ] Estimated score is 40+ points
- [ ] Video is uploaded and link works
- [ ] README is complete and professional
- [ ] Code is clean and well-commented
- [ ] Project has been tested end-to-end
- [ ] Both submission formats prepared (ZIP + GitHub)

### Before You Submit

1. **Test the complete flow one more time:**

   - Clone/extract your project to a new location
   - Follow your own README instructions
   - Verify everything works

2. **Have someone else review:**

   - Can they understand your README?
   - Can they follow setup instructions?
   - Is your video clear?

3. **Double-check file sizes:**

   - Remove any unnecessary large files
   - Ensure model files are included (or note in README if too large)
   - Check that data samples are included

4. **Verify your video:**
   - Link works (test in incognito mode)
   - Video is public/unlisted (not private)
   - Audio is clear
   - Screen recording is visible

### Final Confirmation

I confirm that:

- [ ] My project meets ALL requirements in the rubric
- [ ] My video demonstrates prediction AND retraining with camera ON
- [ ] My notebook shows at least 4 evaluation metrics
- [ ] My application has a web UI with visualizations
- [ ] My code includes data upload and retraining functionality
- [ ] My deployment is Dockerized
- [ ] I have performed load testing and documented results
- [ ] My README has clear instructions and video link
- [ ] I am ready to submit!

---

## Good Luck!

You've got this! Your project demonstrates:

- Complete ML pipeline
- Transfer learning implementation
- Model retraining capability
- Production-ready deployment
- Professional documentation

This represents real-world MLOps skills. Well done!

---

**Note**: Save this checklist and mark items as you complete them. It will help ensure you don't miss any requirements!
