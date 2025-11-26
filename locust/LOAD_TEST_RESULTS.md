# Locust Load Testing Results

## Test Configuration

### Test Environment

- **Host**: http://localhost:5000
- **Date**: [To be filled after running tests]
- **Docker Containers**: [Specify number of containers tested]

### Test Scenarios

#### Scenario 1: Light Load

- **Users**: 10
- **Spawn Rate**: 2 users/second
- **Duration**: 2 minutes
- **Expected**: Baseline performance metrics

#### Scenario 2: Normal Load

- **Users**: 50
- **Spawn Rate**: 5 users/second
- **Duration**: 5 minutes
- **Expected**: Typical production load

#### Scenario 3: Heavy Load

- **Users**: 100
- **Spawn Rate**: 10 users/second
- **Duration**: 5 minutes
- **Expected**: Stress test under high load

#### Scenario 4: Peak Load

- **Users**: 200
- **Spawn Rate**: 20 users/second
- **Duration**: 3 minutes
- **Expected**: Maximum capacity testing

## Results Summary

### Single Container Performance

| Metric                     | Light Load | Normal Load | Heavy Load | Peak Load |
| -------------------------- | ---------- | ----------- | ---------- | --------- |
| Total Requests             | -          | -           | -          | -         |
| Successful Requests        | -          | -           | -          | -         |
| Failed Requests            | -          | -           | -          | -         |
| Success Rate (%)           | -          | -           | -          | -         |
| Average Response Time (ms) | -          | -           | -          | -         |
| Min Response Time (ms)     | -          | -           | -          | -         |
| Max Response Time (ms)     | -          | -           | -          | -         |
| Requests per Second        | -          | -           | -          | -         |
| 50th Percentile (ms)       | -          | -           | -          | -         |
| 95th Percentile (ms)       | -          | -           | -          | -         |
| 99th Percentile (ms)       | -          | -           | -          | -         |

### Multiple Container Performance (2 Containers)

| Metric                     | Light Load | Normal Load | Heavy Load | Peak Load |
| -------------------------- | ---------- | ----------- | ---------- | --------- |
| Total Requests             | -          | -           | -          | -         |
| Successful Requests        | -          | -           | -          | -         |
| Failed Requests            | -          | -           | -          | -         |
| Success Rate (%)           | -          | -           | -          | -         |
| Average Response Time (ms) | -          | -           | -          | -         |
| Min Response Time (ms)     | -          | -           | -          | -         |
| Max Response Time (ms)     | -          | -           | -          | -         |
| Requests per Second        | -          | -           | -          | -         |
| 50th Percentile (ms)       | -          | -           | -          | -         |
| 95th Percentile (ms)       | -          | -           | -          | -         |
| 99th Percentile (ms)       | -          | -           | -          | -         |

### Multiple Container Performance (4 Containers)

| Metric                     | Light Load | Normal Load | Heavy Load | Peak Load |
| -------------------------- | ---------- | ----------- | ---------- | --------- |
| Total Requests             | -          | -           | -          | -         |
| Successful Requests        | -          | -           | -          | -         |
| Failed Requests            | -          | -           | -          | -         |
| Success Rate (%)           | -          | -           | -          | -         |
| Average Response Time (ms) | -          | -           | -          | -         |
| Min Response Time (ms)     | -          | -           | -          | -         |
| Max Response Time (ms)     | -          | -           | -          | -         |
| Requests per Second        | -          | -           | -          | -         |
| 50th Percentile (ms)       | -          | -           | -          | -         |
| 95th Percentile (ms)       | -          | -           | -          | -         |
| 99th Percentile (ms)       | -          | -           | -          | -         |

## Analysis

### Performance Insights

1. **Latency Analysis**

   - [To be filled after tests]
   - Impact of concurrent users on response time
   - Bottlenecks identified

2. **Scalability**

   - [To be filled after tests]
   - Performance improvement with multiple containers
   - Linear scalability assessment

3. **Resource Utilization**

   - CPU usage patterns
   - Memory consumption
   - Network bandwidth

4. **Error Analysis**
   - Types of errors encountered
   - Error rates under different loads
   - Failure patterns

### Recommendations

1. **Optimal Configuration**

   - [To be filled after tests]
   - Recommended number of containers
   - Resource allocation suggestions

2. **Performance Optimization**

   - Identified optimization opportunities
   - Caching strategies
   - Database optimization

3. **Scaling Strategy**
   - Horizontal scaling recommendations
   - Load balancing configuration
   - Auto-scaling triggers

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
