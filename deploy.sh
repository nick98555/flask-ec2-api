#!/bin/bash

cd /home/ubuntu/flask-ec2-api || { echo "❌ Failed to cd into repo directory"; exit 1; }

echo "📦 Current branch:"
git branch

echo "🔄 Fetching latest code..."
git fetch origin || { echo "❌ git fetch failed"; exit 1; }

echo "🚨 Resetting to origin/main..."
git reset --hard origin/main || { echo "❌ git reset failed"; exit 1; }

echo "🔁 Restarting Flask service..."
sudo systemctl restart flask-api || { echo "❌ service restart failed"; exit 1; }

echo "✅ Deployment complete"
