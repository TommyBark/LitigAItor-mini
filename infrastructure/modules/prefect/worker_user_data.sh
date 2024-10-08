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

# Set Prefect API URL
echo 'export PREFECT_API_URL="${prefect_api_url}"' >> /home/ubuntu/.bashrc
export PREFECT_API_URL="${prefect_api_url}"
# sleep for 2 mins to make sure prefect server is up
sleep 120
nohup prefect worker start -q default -p EC2 > /home/ubuntu/worker.log 2>&1 &

echo "Prefect worker setup complete"
