# modules/dynamodb/main.tf

resource "aws_dynamodb_table" "mlflow_experiment_table" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "experiment_id"

  attribute {
    name = "experiment_id"
    type = "S"
  }
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.mlflow_experiment_table.name
}
