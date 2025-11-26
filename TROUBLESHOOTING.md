# Troubleshooting Guide

Common issues and solutions for the MLOps Image Classification project.

## 🔧 Installation Issues

### Issue: `pip install` fails with dependency conflicts

**Solution:**

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install with no dependencies check (use carefully)
pip install --no-deps -r requirements.txt

# Or install key packages individually
pip install tensorflow==2.13.0
pip install flask==2.3.3
pip install pillow==10.0.0
```

### Issue: TensorFlow installation fails

**Solution for Windows:**

```bash
# Install Visual C++ Redistributable
# Download from: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

# Then install TensorFlow
pip install tensorflow==2.13.0
```

**Solution for Mac (M1/M2):**

```bash
# Use miniforge
brew install miniforge
conda create -n mlops python=3.9
conda activate mlops
conda install -c apple tensorflow-deps
pip install tensorflow-macos
pip install tensorflow-metal
```

## 🚫 Model Training Issues

### Issue: Out of Memory during training

**Solution:**

```python
# In the notebook, reduce batch size
BATCH_SIZE = 16  # or even 8

# Or reduce image size
IMG_SIZE = (128, 128)  # instead of (224, 224)

# Or train on fewer images initially
```

### Issue: Training is very slow

**Solutions:**

1. **Check GPU availability:**

```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
```

2. **Reduce epochs for testing:**

```python
EPOCHS = 10  # Instead of 50
```

3. **Use fewer images initially:**

- Start with 50 images per class for testing
- Then scale up once it works

### Issue: Model accuracy is poor (< 70%)

**Solutions:**

1. **Check data quality:**

   - Ensure images are correctly labeled
   - Remove corrupted images
   - Balance classes (equal samples per class)

2. **Increase training data:**

   - Add more images (aim for 200+ per class)

3. **Adjust hyperparameters:**

```python
# Increase training time
EPOCHS = 100

# Adjust learning rate
LEARNING_RATE = 0.00001  # Smaller for fine-tuning
```

## 🌐 Application Issues

### Issue: Application fails to start - "Model file not found"

**Solution:**

```bash
# Make sure you've trained the model first
# Check if these files exist:
ls models/image_classifier_model.h5
ls models/class_indices.json

# If not, train the model:
jupyter notebook notebook/image_classification.ipynb
# Run all cells
```

### Issue: Port 5000 already in use

**Solution:**

**Windows:**

```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

**Linux/Mac:**

```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use a different port
# In app/app.py, change:
app.run(host='0.0.0.0', port=5001)
```

### Issue: Images not displaying in web interface

**Solution:**

1. Check file permissions:

```bash
# Windows (PowerShell)
icacls data\uploaded /grant Everyone:F

# Linux/Mac
chmod -R 755 data/uploaded
```

2. Check Flask static files configuration
3. Clear browser cache (Ctrl+Shift+Del)

### Issue: Prediction returns error

**Possible causes and solutions:**

1. **Wrong image format:**

```python
# Supported: PNG, JPG, JPEG, GIF, BMP
# Convert other formats using:
from PIL import Image
img = Image.open('image.webp')
img.save('image.jpg', 'JPEG')
```

2. **Image too large:**

```python
# Check max file size in app.py:
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

3. **Corrupted model:**

```bash
# Retrain the model
# Delete old model first
rm models/image_classifier_model.h5
# Then retrain using notebook
```

## 🐳 Docker Issues

### Issue: Docker build fails

**Solution:**

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose -f deployment/docker-compose.yml build --no-cache

# Check Docker is running
docker ps
```

### Issue: Docker container exits immediately

**Solution:**

```bash
# Check logs
docker-compose -f deployment/docker-compose.yml logs

# Common issue: Missing model files
# Make sure models/ directory has the trained model

# Run interactively to debug
docker run -it mlops_classifier_web /bin/bash
```

### Issue: Cannot access application at localhost:5000

**Solutions:**

1. **Check container is running:**

```bash
docker ps
# Should show mlops_classifier_web
```

2. **Check port mapping:**

```bash
docker port mlops_classifier_web
# Should show: 5000/tcp -> 0.0.0.0:5000
```

3. **Try different URL:**

```
http://127.0.0.1:5000
http://0.0.0.0:5000
http://localhost:5000
```

4. **Check Windows firewall:**

```powershell
# Allow port 5000
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

## 📊 Load Testing Issues

### Issue: Locust web interface won't start

**Solution:**

```bash
# Make sure locust is installed
pip install locust

# Specify web interface explicitly
locust -f locust/locustfile.py --web-host=127.0.0.1 --web-port=8089 --host=http://localhost:5000

# Check no other service is using port 8089
netstat -ano | findstr :8089
```

### Issue: All requests fail in load testing

**Solutions:**

1. **Make sure application is running:**

```bash
# Check application is accessible
curl http://localhost:5000/

# Or in PowerShell:
Invoke-WebRequest http://localhost:5000/
```

2. **Check correct host:**

```bash
# If using Docker:
locust -f locust/locustfile.py --host=http://localhost:5000

# If running locally:
locust -f locust/locustfile.py --host=http://127.0.0.1:5000
```

3. **Increase timeout:**

```python
# In locustfile.py
class ImageClassificationUser(HttpUser):
    network_timeout = 60.0  # Increase timeout
```

## 📓 Jupyter Notebook Issues

### Issue: Kernel keeps dying during training

**Solutions:**

1. **Increase system RAM allocation**
2. **Reduce batch size and image size**
3. **Use a cloud platform:**
   - Google Colab (free GPU)
   - Kaggle Kernels (free GPU)
   - AWS SageMaker

### Issue: Cannot connect to kernel

**Solution:**

```bash
# Restart Jupyter
jupyter notebook stop
jupyter notebook

# Or clear cache
jupyter notebook --clear-output notebook/image_classification.ipynb
```

### Issue: Notebook takes forever to save

**Solution:**

```bash
# Clear outputs before committing
jupyter nbconvert --clear-output --inplace notebook/image_classification.ipynb

# Then run cells again to generate outputs
```

## 🔄 Retraining Issues

### Issue: Retraining fails with "No images found"

**Solution:**

```bash
# Check data directory structure:
ls data/train/
# Should show class folders (e.g., cats, dogs)

ls data/train/cats/
# Should show image files

# Make sure images were uploaded correctly
# Go to /upload_data page and upload again
```

### Issue: Retraining progress stuck at 0%

**Solutions:**

1. **Check logs:**

```bash
# If using Docker:
docker-compose -f deployment/docker-compose.yml logs -f web

# If running locally:
# Check terminal where Flask is running
```

2. **Restart application:**

```bash
# Kill and restart the Flask app
```

3. **Check sufficient disk space:**

```bash
# Windows
Get-PSDrive C

# Linux/Mac
df -h
```

## 🎥 Video Recording Issues

### Issue: Video file too large to upload

**Solutions:**

1. **Compress video:**

   - Use HandBrake (free)
   - Or online: https://www.videosmaller.com/

2. **Reduce recording quality:**

   - Lower resolution (720p instead of 1080p)
   - Reduce frame rate (30fps instead of 60fps)

3. **Trim unnecessary parts:**
   - Use video editing software
   - Keep only essential demonstrations

### Issue: Audio quality is poor

**Solutions:**

1. **Use external microphone**
2. **Record in quiet environment**
3. **Test audio before full recording**
4. **Add subtitles if needed**

## 📦 GitHub Issues

### Issue: Push fails - file too large

**Solution:**

```bash
# Check what's large
du -sh * | sort -h

# Remove from git
git rm --cached models/image_classifier_model.h5

# Add to .gitignore
echo "models/*.h5" >> .gitignore

# Use Git LFS for large files
git lfs install
git lfs track "*.h5"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Issue: Repository not updating

**Solution:**

```bash
# Force push (be careful!)
git push -f origin main

# Or create new repository
# Delete old one and create fresh
```

## 💡 General Tips

### Performance Optimization

1. **For faster training:**

   - Use GPU if available
   - Reduce image size temporarily
   - Start with fewer epochs

2. **For faster application:**

   - Cache model in memory
   - Use production WSGI server (gunicorn)
   - Enable compression

3. **For smaller model files:**
   - Use quantization
   - Remove unnecessary layers
   - Use TFLite for mobile deployment

### Debugging Tips

1. **Enable debug mode:**

```python
# In app/app.py
app.run(debug=True)
```

2. **Add logging:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **Test components individually:**

```python
# Test preprocessing
from src.preprocessing import ImagePreprocessor
preprocessor = ImagePreprocessor()
img = preprocessor.preprocess_single_image('test.jpg')

# Test prediction
from src.prediction import PredictionService
service = PredictionService(...)
result = service.predict_image('test.jpg')
```

## 🆘 Still Having Issues?

If none of the above solutions work:

1. **Check error messages carefully** - they usually indicate the problem
2. **Search the error on Google/Stack Overflow**
3. **Review code comments** - they contain helpful hints
4. **Simplify** - Start with a minimal version that works
5. **Ask for help** - Share specific error messages

## 📞 Emergency Quick Fixes

If you're close to deadline:

1. **Model won't train?**

   - Use fewer images (20 per class)
   - Reduce epochs to 5-10
   - Use smaller image size (128x128)

2. **Application won't start?**

   - Comment out problematic features
   - Focus on core prediction functionality

3. **Docker won't work?**

   - Show local version instead
   - Provide clear local setup instructions

4. **Video issues?**
   - Record shorter video
   - Use phone camera if needed
   - Screenshots + voiceover works too

Remember: A working simple version is better than a broken complex one!

---

**Last Updated**: November 2025
**Need more help?** Check the main [README.md](README.md) for additional documentation.
