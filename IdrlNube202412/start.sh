#!/bin/bash
# Update the package list
sudo apt-get update

# Install Python3 and pip
sudo apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
venv/bin/pip install -r requirements.txt

# Run the Flask application
flask run --host=0.0.0.0 --port=8080