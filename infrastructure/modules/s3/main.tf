# modules/s3/main.tf

resource "aws_s3_bucket" "mlflow_artifact_bucket" {
  bucket        = var.s3_bucket_name
  force_destroy = true
}

output "bucket_name" {
  value = aws_s3_bucket.mlflow_artifact_bucket.bucket
}
