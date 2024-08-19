variable "ami_id" {
  description = "The ID of the AMI to use for the instance"
  type        = string
}

variable "instance_type" {
  description = "The type of instance to start"
  type        = string
  default     = "t2.micro"
}

variable "name" {
  description = "Name of the instance"
  type        = string
  default     = "mlflow-tracking-server"
}

variable "subnet_id" {
  description = "The VPC Subnet ID to launch in"
  type        = string
}

variable "subnet_ids" {
  description = "A list of VPC subnet IDs for the backend"
  type        = list(string)
}

variable "mlflow_backend_password" {
    description = "The password for the RDS instance"
    type        = string
}

variable "vpc_id" {
  description = "The VPC ID where the EC2 instance will be deployed"
  type        = string
}

variable "vpc_cidr" {
  description = "The CIDR block of the VPC"
  type        = string
}

variable "public_key_path" {
  description = "Path to the public key to be used for the EC2 instance"
  type        = string
}

variable "ingress_cidr_blocks" {
  description = "List of allowed IPs for the security group"
  type        = list(string)
  default = ["0.0.0.0/0"]
}