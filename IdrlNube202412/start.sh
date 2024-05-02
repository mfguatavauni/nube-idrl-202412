#!/bin/bash

# Update the package list
sudo apt-get update

gcloud sql connect db --user=postgres
export DATABASE_URL=postgresql://postgres:postgres@23.251.146.53:5432/idrl

# Install Python3 and pip
sudo apt-get install -y python3 python3-pip python3-venv libpq-dev libjpeg-dev git

sudo git clone https://github.com/mfguatavauni/nube-idrl-202412.git

cd nube-idrl-202412/IdrlNube202412/

# Create a virtual environment
sudo python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
sudo venv/bin/pip install -r requirements.txt

# Run the Flask application
flask run --host=0.0.0.0 --port=8080