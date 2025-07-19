#!/bin/bash

# Trust the repo directory
sudo git config --system --add safe.directory /home/ubuntu/flask-ec2-api

# Tell Git to use your GitHub SSH key
export GIT_SSH_COMMAND="ssh -i /home/ubuntu/.ssh/id_rsa -o StrictHostKeyChecking=no"

cd /home/ubuntu/flask-ec2-api || { echo "Failed to cd into repo directory"; exit 1; }

echo "Current branch:"
git branch

echo "Fetching latest code..."
git fetch origin || { echo "git fetch failed"; exit 1; }

echo "Resetting to origin/main..."
git reset --hard origin/main || { echo "git reset failed"; exit 1; }

echo "Restarting Flask service..."
sudo systemctl restart flask-api || { echo "service restart failed"; exit 1; }

echo "Deployment complete"
