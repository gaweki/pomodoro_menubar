#!/bin/bash

# Pomodoro Terminal - Manual Run Script
# This script handles both first-time setup and regular running

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Virtual environment not found. Creating..."
    python3 -m venv venv
    print_success "Virtual environment created."
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Installing dependencies..."
    pip install --upgrade pip
    pip install rumps pyobjc
    print_success "Dependencies installed."
else
    print_status "Virtual environment found. Activating..."
    source venv/bin/activate
fi

# Check if main script exists and is executable
if [ ! -f "main.py" ]; then
    print_error "main.py not found in current directory!"
    exit 1
fi

if [ ! -x "main.py" ]; then
    print_status "Making main.py executable..."
    chmod +x main.py
fi

# Check if required data directories exist
if [ ! -d "data" ]; then
    print_status "Creating data directory..."
    mkdir -p data
fi

print_success "Starting Pomodoro Menu Bar Application..."
print_status "The timer icon (🍅) should appear in your menu bar."
print_warning "Press Ctrl+C to stop the application."

# Run the application
./main.py
