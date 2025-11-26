#!/bin/bash

# Build and Deploy Script for MLOps Image Classification

echo "======================================"
echo "MLOps Image Classification Deployment"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build the Docker image
echo ""
echo "Building Docker image..."
docker-compose -f deployment/docker-compose.yml build

if [ $? -ne 0 ]; then
    echo "Error: Docker build failed."
    exit 1
fi

echo ""
echo "Docker image built successfully!"

# Start the containers
echo ""
echo "Starting containers..."
docker-compose -f deployment/docker-compose.yml up -d

if [ $? -ne 0 ]; then
    echo "Error: Failed to start containers."
    exit 1
fi

echo ""
echo "======================================"
echo "Deployment successful!"
echo "======================================"
echo ""
echo "Application is running at:"
echo "  - Direct access: http://localhost:5000"
echo "  - Via Nginx: http://localhost:80"
echo ""
echo "To view logs:"
echo "  docker-compose -f deployment/docker-compose.yml logs -f"
echo ""
echo "To stop containers:"
echo "  docker-compose -f deployment/docker-compose.yml down"
echo ""
echo "To restart containers:"
echo "  docker-compose -f deployment/docker-compose.yml restart"
echo ""
