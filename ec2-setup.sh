#!/bin/bash

# Update packages
sudo apt update -y
sudo apt install -y python3-pip git

# Clone your GitHub repo (update with your actual repo later)
git clone https://github.com/nick98555/flask-ec2-api.git
cd flask-ec2-api

# Install dependencies
pip3 install -r requirements.txt

# Run the Flask app
nohup python3 app.py &
