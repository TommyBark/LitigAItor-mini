variable "mlflow_db_password" {
  description = "Password for the MLflow backend database"
  type        = string
  sensitive   = true
}