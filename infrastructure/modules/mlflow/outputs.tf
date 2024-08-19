output "mlflow_tracking_uri" {
  value = "http://${module.mlflow_tracking_server.public_ip}:5000"
}

output "mlflow_s3_artifact_uri" {
  value = "s3://${module.mlflow_artifact_store.bucket_id}/"
}