#!/bin/bash

cd /home/ubuntu/flask-ec2-api
git fetch origin
git reset --hard origin/main
sudo systemctl restart flask-api
