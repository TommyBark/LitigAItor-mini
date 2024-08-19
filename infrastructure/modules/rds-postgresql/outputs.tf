output "db_instance_endpoint" {
  description = "The connection endpoint"
  value       = aws_db_instance.default.endpoint
}

output "db_instance_name" {
  description = "The database name"
  value       = aws_db_instance.default.db_name
}

output "db_instance_username" {
  description = "The master username for the database"
  value       = aws_db_instance.default.username
}

output "db_instance_port" {
  description = "The database port"
  value       = aws_db_instance.default.port
}