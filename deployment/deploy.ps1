# Build and Deploy Script for MLOps Image Classification (PowerShell)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MLOps Image Classification Deployment" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is installed
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Build the Docker image
Write-Host "`nBuilding Docker image..." -ForegroundColor Yellow
docker-compose -f deployment/docker-compose.yml build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker build failed." -ForegroundColor Red
    exit 1
}

Write-Host "`nDocker image built successfully!" -ForegroundColor Green

# Start the containers
Write-Host "`nStarting containers..." -ForegroundColor Yellow
docker-compose -f deployment/docker-compose.yml up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to start containers." -ForegroundColor Red
    exit 1
}

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "Deployment successful!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "`nApplication is running at:" -ForegroundColor White
Write-Host "  - Direct access: http://localhost:5000" -ForegroundColor Yellow
Write-Host "  - Via Nginx: http://localhost:80" -ForegroundColor Yellow
Write-Host "`nTo view logs:" -ForegroundColor White
Write-Host "  docker-compose -f deployment/docker-compose.yml logs -f" -ForegroundColor Cyan
Write-Host "`nTo stop containers:" -ForegroundColor White
Write-Host "  docker-compose -f deployment/docker-compose.yml down" -ForegroundColor Cyan
Write-Host "`nTo restart containers:" -ForegroundColor White
Write-Host "  docker-compose -f deployment/docker-compose.yml restart" -ForegroundColor Cyan
Write-Host ""
