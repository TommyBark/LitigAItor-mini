# main.tf

provider "aws" {
  region                      = "us-west-1"
  access_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true

#   endpoints {
#     s3    = "http://localhost:4566"
#     dynamodb = "http://localhost:4566"
#   }
}

resource "aws_s3_bucket" "mlflow_artifact_bucket" {
  bucket = "mlflow-artifacts"
  force_destroy = true
}

resource "aws_dynamodb_table" "mlflow_experiment_table" {
  name         = "mlflow-experiments"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "experiment_id"

  attribute {
    name = "experiment_id"
    type = "S"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.mlflow_artifact_bucket.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.mlflow_experiment_table.name
}