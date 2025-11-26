"""
Setup Script for MLOps Image Classification Project

This script automates the initial setup process.

Usage:
    python setup.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")

def print_step(step_num, text):
    """Print step information"""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 60)

def check_python_version():
    """Check Python version"""
    print_step(1, "Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print("Please install Python 3.8+ and try again")
        return False
    
    print("✓ Python version is compatible")
    return True

def create_directories():
    """Create necessary directories"""
    print_step(2, "Creating Directory Structure")
    
    directories = [
        'data/train/cats',
        'data/train/dogs',
        'data/test/cats',
        'data/test/dogs',
        'data/uploaded',
        'models',
        'logs'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
    
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    print_step(3, "Checking Virtual Environment")
    
    in_venv = hasattr(sys, 'real_prefix') or \
              (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✓ Running in virtual environment")
        return True
    else:
        print("⚠️  Not running in virtual environment")
        print("\nRecommendation:")
        print("  Create and activate a virtual environment:")
        print("\n  Windows:")
        print("    python -m venv venv")
        print("    .\\venv\\Scripts\\activate")
        print("\n  Linux/Mac:")
        print("    python3 -m venv venv")
        print("    source venv/bin/activate")
        print("\nThen run this script again.")
        
        response = input("\nContinue anyway? (y/n): ")
        return response.lower() == 'y'

def install_dependencies():
    """Install Python dependencies"""
    print_step(4, "Installing Dependencies")
    
    print("This may take 5-10 minutes...")
    print("Installing packages from requirements.txt...\n")
    
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            "requirements.txt",
            "--upgrade"
        ])
        print("\n✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Error installing dependencies")
        print("Try installing manually: pip install -r requirements.txt")
        return False

def check_dataset():
    """Check if dataset exists"""
    print_step(5, "Checking Dataset")
    
    train_cats = len(list(Path('data/train/cats').glob('*.jpg'))) + \
                 len(list(Path('data/train/cats').glob('*.png')))
    train_dogs = len(list(Path('data/train/dogs').glob('*.jpg'))) + \
                 len(list(Path('data/train/dogs').glob('*.png')))
    
    total = train_cats + train_dogs
    
    print(f"Training images found:")
    print(f"  Cats: {train_cats}")
    print(f"  Dogs: {train_dogs}")
    print(f"  Total: {total}")
    
    if total == 0:
        print("\n⚠️  No training data found!")
        print("\nYou need to add images to train the model.")
        print("See QUICK_START.md for instructions on getting data.")
        return False
    elif total < 100:
        print("\n⚠️  Dataset is very small. Recommend 200+ images.")
        return True
    else:
        print("\n✓ Dataset looks good!")
        return True

def check_docker():
    """Check if Docker is available"""
    print_step(6, "Checking Docker (Optional)")
    
    try:
        subprocess.check_output(['docker', '--version'])
        print("✓ Docker is installed")
        
        try:
            subprocess.check_output(['docker-compose', '--version'])
            print("✓ Docker Compose is installed")
            return True
        except:
            print("⚠️  Docker Compose not found")
            print("  Install: pip install docker-compose")
            return False
    except:
        print("⚠️  Docker not found")
        print("  Docker is optional but recommended for deployment")
        print("  Download from: https://www.docker.com/get-started")
        return False

def print_next_steps():
    """Print next steps"""
    print_header("Setup Complete!")
    
    print("📋 Next Steps:\n")
    
    print("1. Add Training Data:")
    print("   - Run: python scripts/download_sample_data.py")
    print("   - Or manually add images to data/train/ folders")
    print()
    
    print("2. Train the Model:")
    print("   - Run: jupyter notebook")
    print("   - Open: notebook/image_classification.ipynb")
    print("   - Execute all cells (takes 15-30 minutes)")
    print()
    
    print("3. Start the Application:")
    print("   - Run: python app/app.py")
    print("   - Open: http://localhost:5000")
    print()
    
    print("4. (Optional) Docker Deployment:")
    print("   - Run: docker-compose -f deployment/docker-compose.yml up -d")
    print()
    
    print("5. (Optional) Load Testing:")
    print("   - Run: cd locust && locust -f locustfile.py --host=http://localhost:5000")
    print()
    
    print("📚 Documentation:")
    print("   - Quick Start: QUICK_START.md")
    print("   - Full Guide: README.md")
    print("   - Troubleshooting: TROUBLESHOOTING.md")
    print("   - Submission Checklist: SUBMISSION_CHECKLIST.md")
    print()

def main():
    """Main setup function"""
    print_header("MLOps Image Classification - Setup Script")
    
    print("This script will:")
    print("  1. Check Python version")
    print("  2. Create directory structure")
    print("  3. Check virtual environment")
    print("  4. Install dependencies")
    print("  5. Check dataset")
    print("  6. Check Docker installation")
    print()
    
    response = input("Continue with setup? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return
    
    # Run setup steps
    steps_passed = []
    
    # Step 1: Check Python
    if check_python_version():
        steps_passed.append("Python version")
    else:
        print("\n❌ Setup failed: Python version incompatible")
        return
    
    # Step 2: Create directories
    if create_directories():
        steps_passed.append("Directory structure")
    
    # Step 3: Check virtual environment
    if not check_virtual_environment():
        print("\n❌ Setup cancelled")
        return
    steps_passed.append("Virtual environment check")
    
    # Step 4: Install dependencies
    install_response = input("\nInstall dependencies now? (y/n): ")
    if install_response.lower() == 'y':
        if install_dependencies():
            steps_passed.append("Dependencies")
        else:
            print("\n⚠️  Continuing despite dependency install failure")
    else:
        print("Skipping dependency installation")
        print("Remember to run: pip install -r requirements.txt")
    
    # Step 5: Check dataset
    if check_dataset():
        steps_passed.append("Dataset check")
    else:
        print("⚠️  No dataset found - add data before training")
    
    # Step 6: Check Docker
    if check_docker():
        steps_passed.append("Docker")
    
    # Print summary
    print_header("Setup Summary")
    print("✓ Completed steps:")
    for step in steps_passed:
        print(f"  • {step}")
    
    # Print next steps
    print_next_steps()
    
    print_header("Happy Coding! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        print("Please check TROUBLESHOOTING.md or run steps manually")
        sys.exit(1)
