# modules/ec2/variables.tf

variable "vpc_id" {
  description = "The VPC ID where the EC2 instance will be deployed"
  type        = string
}

variable "subnet_id" {
  description = "The Subnet ID where the EC2 instance will be deployed"
  type        = string
}

variable "security_group_id" {
  description = "The Security Group ID for the EC2 instance"
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket for MLflow artifacts"
  type        = string
}

variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table for MLflow experiment tracking"
  type        = string
}
