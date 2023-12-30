#!/bin/bash

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing Git..."
    sudo apt-get install git -y
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt-get install python3 -y
fi

# Clone the repository
git clone https://github.com/scapekambing/esp32e-switch-python.git

# Navigate to the project directory
cd esp32e-switch-python

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the Python script
python spray.py
