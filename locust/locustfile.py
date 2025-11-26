"""
Locust Load Testing Script for Image Classification API

This script simulates multiple users making concurrent requests to the
image classification API to test performance, latency, and response times.

Usage:
    locust -f locustfile.py --host=http://localhost:5000

Web UI:
    locust -f locustfile.py --host=http://localhost:5000 --web-host=127.0.0.1 --web-port=8089

Headless (command-line):
    locust -f locustfile.py --host=http://localhost:5000 --users 100 --spawn-rate 10 --run-time 5m --headless
"""

from locust import HttpUser, task, between, events
import io
import random
import time
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global statistics
request_stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'total_response_time': 0,
    'min_response_time': float('inf'),
    'max_response_time': 0
}


def create_test_image(width=224, height=224):
    """
    Create a random test image for prediction
    
    Args:
        width: Image width
        height: Image height
    
    Returns:
        BytesIO object containing the image
    """
    # Create random RGB image
    img = Image.new('RGB', (width, height), 
                    color=(random.randint(0, 255), 
                          random.randint(0, 255), 
                          random.randint(0, 255)))
    
    # Add some random pixels for variation
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (random.randint(0, 255), 
                           random.randint(0, 255), 
                           random.randint(0, 255))
    
    # Save to BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """
    Event listener to track request statistics
    """
    request_stats['total_requests'] += 1
    
    if exception:
        request_stats['failed_requests'] += 1
    else:
        request_stats['successful_requests'] += 1
        request_stats['total_response_time'] += response_time
        request_stats['min_response_time'] = min(request_stats['min_response_time'], response_time)
        request_stats['max_response_time'] = max(request_stats['max_response_time'], response_time)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Print statistics when test stops
    """
    logger.info("\n" + "=" * 60)
    logger.info("LOAD TEST STATISTICS")
    logger.info("=" * 60)
    logger.info(f"Total Requests: {request_stats['total_requests']}")
    logger.info(f"Successful Requests: {request_stats['successful_requests']}")
    logger.info(f"Failed Requests: {request_stats['failed_requests']}")
    
    if request_stats['successful_requests'] > 0:
        avg_response_time = request_stats['total_response_time'] / request_stats['successful_requests']
        logger.info(f"Average Response Time: {avg_response_time:.2f} ms")
        logger.info(f"Min Response Time: {request_stats['min_response_time']:.2f} ms")
        logger.info(f"Max Response Time: {request_stats['max_response_time']:.2f} ms")
        
        success_rate = (request_stats['successful_requests'] / request_stats['total_requests']) * 100
        logger.info(f"Success Rate: {success_rate:.2f}%")
    
    logger.info("=" * 60 + "\n")


class ImageClassificationUser(HttpUser):
    """
    Simulated user for image classification service
    """
    
    # Wait time between tasks (1-3 seconds)
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Called when a simulated user starts
        """
        logger.info(f"User {self.id} started")
    
    @task(5)
    def predict_image(self):
        """
        Test the /api/predict endpoint (highest weight - most common task)
        """
        # Create a test image
        img = create_test_image()
        
        # Prepare the file for upload
        files = {'file': ('test_image.png', img, 'image/png')}
        
        # Make the request
        with self.client.post("/api/predict", files=files, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('success'):
                        response.success()
                    else:
                        response.failure(f"Prediction failed: {result.get('error')}")
                except Exception as e:
                    response.failure(f"Failed to parse response: {str(e)}")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def view_home(self):
        """
        Test the home page
        """
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def view_visualizations(self):
        """
        Test the visualizations page
        """
        with self.client.get("/visualizations", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def view_monitoring(self):
        """
        Test the monitoring page
        """
        with self.client.get("/monitoring", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def get_metrics(self):
        """
        Test the metrics API endpoint
        """
        with self.client.get("/api/metrics", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    response.json()
                    response.success()
                except Exception as e:
                    response.failure(f"Failed to parse metrics: {str(e)}")
            else:
                response.failure(f"Got status code {response.status_code}")


class HeavyLoadUser(HttpUser):
    """
    Simulated user with heavier load (for stress testing)
    """
    
    # Shorter wait time for stress testing
    wait_time = between(0.5, 1.5)
    
    @task
    def rapid_predictions(self):
        """
        Make rapid consecutive predictions
        """
        for _ in range(5):
            img = create_test_image()
            files = {'file': ('test_image.png', img, 'image/png')}
            
            self.client.post("/api/predict", files=files)
            time.sleep(0.1)  # Small delay between requests


# Custom Locust shape for ramping up users (COMMENTED OUT to enable manual control)
# Uncomment this class if you want automated step-load testing
# from locust import LoadTestShape

# class StepLoadShape(LoadTestShape):
#     """
#     A step load shape to gradually increase load
#     
#     Step 1: 10 users for 60 seconds
#     Step 2: 25 users for 60 seconds
#     Step 3: 50 users for 60 seconds
#     Step 4: 100 users for 60 seconds
#     Step 5: 200 users for 60 seconds
#     """
#     
#     step_time = 60
#     step_load = [10, 25, 50, 100, 200]
#     
#     def tick(self):
#         run_time = self.get_run_time()
#         
#         if run_time > self.step_time * len(self.step_load):
#             return None
#         
#         current_step = int(run_time // self.step_time)
#         return (self.step_load[current_step], self.step_load[current_step] // 10)


if __name__ == "__main__":
    """
    Instructions for running the load test
    """
    print("""
    ============================================
    Image Classification Load Testing with Locust
    ============================================
    
    To run the load test:
    
    1. Web Interface (Recommended):
       locust -f locustfile.py --host=http://localhost:5000
       
       Then open http://localhost:8089 in your browser
    
    2. Headless Mode (No UI):
       locust -f locustfile.py --host=http://localhost:5000 \\
              --users 100 --spawn-rate 10 --run-time 5m --headless
    
    3. Custom Configuration:
       locust -f locustfile.py --host=http://localhost:5000 \\
              --users 50 --spawn-rate 5 --run-time 2m
    
    Parameters:
      --users: Total number of concurrent users
      --spawn-rate: Rate at which to spawn users (users per second)
      --run-time: Duration of test (e.g., 5m, 30s, 1h)
      --headless: Run without web interface
    
    Test Scenarios:
      - ImageClassificationUser: Normal load testing
      - HeavyLoadUser: Stress testing with rapid requests
      - StepLoadShape: Gradual ramp-up of users
    
    ============================================
    """)
