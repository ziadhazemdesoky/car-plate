#!/bin/bash

# Update and upgrade system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python3 and pip
echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

# Install virtualenv (optional but recommended)
echo "Installing virtualenv..."
pip3 install virtualenv

# Create and activate a virtual environment
echo "Setting up a virtual environment..."
virtualenv venv
source venv/bin/activate

# Install required Python libraries
echo "Installing Python dependencies..."
pip install flask boto3 numpy

# Export environment variables (Optional: Replace with actual keys or load from a secure file)
echo "Setting AWS credentials as environment variables..."
export AWS_ACCESS_KEY_ID="AKIAXWMA6DHLMPZP6R3D"
export AWS_SECRET_ACCESS_KEY="oiLj+JJH26Jh4YvqgDy7k4ZNnqOEgWhZYJaAjOSG"
export AWS_REGION="us-east-1"

# Run the Flask server
echo "Starting the Flask server..."
python3 main.py
