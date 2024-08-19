#!/bin/bash
set -e

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt install -y python3.12-venv
sudo apt install -y python3-pip
cd /home/ubuntu
python3 -m venv prefect-env
source prefect-env/bin/activate
pip3 install --upgrade pip
pip3 install prefect==2.20.2

# Start Prefect Orion server
nohup prefect server start --host 0.0.0.0 > /var/log/prefect.log 2>&1 &

echo "Prefect Orion server setup complete"