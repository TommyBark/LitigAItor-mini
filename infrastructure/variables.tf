# variables.tf

variable "region" {
  description = "The AWS region to deploy resources to"
  type        = string
  default     = "eu-west-1"
}

variable "s3_bucket_name" {
  description = "S3 bucket name for MLflow artifacts"
  type        = string
  default     = "mlflow-artifacts"
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name for MLflow experiment tracking"
  type        = string
  default     = "mlflow-experiments"
}
