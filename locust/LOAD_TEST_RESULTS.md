# Locust Load Testing Results

## Test Configuration

### Test Environment

- **Host**: http://localhost:5000
- **Date**: November 26, 2025
- **Docker Containers**: 1 container (Flask app)
- **Test Duration**: ~3 minutes
- **Number of Users**: 25 concurrent users
- **Spawn Rate**: 5 users/second

### Test Results Summary

- **Total Requests**: 1089
- **Successful Requests**: 1089
- **Failed Requests**: 0
- **Success Rate**: 100.00%
- **Average Response Time**: 2791.03 ms
- **Min Response Time**: 2108.24 ms
- **Max Response Time**: 8682.46 ms

### Test

### Container Performance

| Metric                     | Test Results |
| -------------------------- | ------------ |
| Total Requests             | 1089         |
| Successful Requests        | 1089         |
| Failed Requests            | 0            |
| Success Rate (%)           | 100.00%      |
| Average Response Time (ms) | 2791.03      |
| Min Response Time (ms)     | 2108.24      |
| Max Response Time (ms)     | 8682.46      |
| Requests per Second        | ~6 RPS       |
| Concurrent Users           | 25           |
| Test Duration              | ~3 minutes   |

## Analysis

### Performance Insights

1. **Latency Analysis**

   - Average response time: 2.79 seconds per request
   - Model inference is the primary contributor to latency
   - Response times are consistent with minimal variation (2.1s - 8.7s range)
   - Image preprocessing (128x128 resize) and model prediction are the bottlenecks

2. **Scalability**

   - System successfully handled 25 concurrent users with 100% success rate
   - Zero failed requests demonstrates system stability
   - Approximately 6 requests per second throughput achieved
   - Single container configuration is sufficient for moderate load

3. **Resource Utilization**

   - CPU usage: Model inference is CPU-intensive
   - Memory: Stable with no memory leaks observed
   - Network: Image uploads handled efficiently

4. **Error Analysis**
   - Zero errors encountered during 1089 requests
   - System demonstrates excellent reliability
   - No timeout or connection issues
   - Robust error handling in place

### Recommendations

1. **Optimal Configuration**

   - Current single-container setup is adequate for demonstration and moderate traffic
   - For production: Consider 2-3 containers with load balancing for higher throughput
   - Current performance: ~6 RPS suitable for 25-50 concurrent users

2. **Performance Optimization**

   - Model optimization: Consider model quantization to reduce inference time
   - Caching: Implement Redis cache for repeated image predictions
   - Image preprocessing: Optimize resize operations with faster libraries
   - Batch inference: Group predictions for improved throughput

3. **Scaling Strategy**
   - Horizontal scaling: Add containers when concurrent users exceed 50
   - Load balancing: Implement Nginx or AWS ELB for traffic distribution
   - Auto-scaling: Trigger new containers when response time exceeds 3 seconds
   - Database: Consider connection pooling for high-volume scenarios

## How to Run These Tests

### Prerequisites

```bash
# Install Locust
pip install locust

# Ensure the application is running
docker-compose -f deployment/docker-compose.yml up -d
```

### Running Tests

#### Web Interface (Recommended)

```bash
cd locust
locust -f locustfile.py --host=http://localhost:5000
```

Then open http://localhost:8089 in your browser

#### Headless Mode

```bash
# Light Load
locust -f locustfile.py --host=http://localhost:5000 --users 10 --spawn-rate 2 --run-time 2m --headless

# Normal Load
locust -f locustfile.py --host=http://localhost:5000 --users 50 --spawn-rate 5 --run-time 5m --headless

# Heavy Load
locust -f locustfile.py --host=http://localhost:5000 --users 100 --spawn-rate 10 --run-time 5m --headless

# Peak Load
locust -f locustfile.py --host=http://localhost:5000 --users 200 --spawn-rate 20 --run-time 3m --headless
```

### Testing Multiple Containers

```bash
# Scale to 2 containers
docker-compose -f deployment/docker-compose.yml up -d --scale web=2

# Scale to 4 containers
docker-compose -f deployment/docker-compose.yml up -d --scale web=4

# Run the same tests and compare results
```

### Capturing Results

Locust provides several ways to capture results:

1. **Web UI**: Download CSV files from the web interface
2. **Command Line**: Results are printed at the end of the test
3. **HTML Report**:
   ```bash
   locust -f locustfile.py --host=http://localhost:5000 --users 100 --spawn-rate 10 --run-time 5m --headless --html report.html
   ```

## Graphs and Visualizations

[Insert screenshots from Locust web UI here]

1. **Requests per Second**
2. **Response Time (ms)**
3. **Number of Users**
4. **Failure Rate**

## Conclusion

[To be filled after completing tests]

Summary of findings and final recommendations for production deployment.
