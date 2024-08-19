#!/bin/bash
sudo apt update
sudo apt install -y python3.12-venv
sudo apt install -y python3-pip
cd /home/ubuntu
python3 -m venv mlflow-env
source mlflow-env/bin/activate
pip3 install --upgrade pip
pip3 install mlflow psycopg2-binary boto3 setuptools
echo "Setting up MLFlow env vars"
export MLFLOW_S3_ENDPOINT_URL=https://${module.mlflow_artifact_store.bucket_regional_domain_name}
export MLFLOW_TRACKING_URI=postgresql://${module.mlflow_db.db_instance_username}:${var.mlflow_backend_password}@${module.mlflow_db.db_instance_endpoint}/${module.mlflow_db.db_instance_name}
nohup mlflow server \
--backend-store-uri $MLFLOW_TRACKING_URI \
--default-artifact-root s3://${module.mlflow_artifact_store.bucket_id}/ \
--host 0.0.0.0 \
> mlflow.log 2>&1 &
