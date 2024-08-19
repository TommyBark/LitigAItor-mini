resource "aws_security_group" "mlflow_ec2_sg" {
  name        = "${var.name}-ec2-sg"
  description = "Security group for MLflow EC2 instance"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow inbound traffic on port 5000 for MLflow UI"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = var.ingress_cidr_blocks
  }

  ingress {
    description = "Allow SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ingress_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-mlflow-ec2-sg"
  }
}

# Create an IAM role for the EC2 instance
resource "aws_iam_role" "mlflow_ec2_role" {
  name = "${var.name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach policies to the IAM role
resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.mlflow_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Create an instance profile
resource "aws_iam_instance_profile" "mlflow_ec2_profile" {
  name = "${var.name}-ec2-profile"
  role = aws_iam_role.mlflow_ec2_role.name
}

# Create a key pair for SSH access
resource "aws_key_pair" "mlflow_key_pair" {
  key_name   = "${var.name}-mlflow-key"
  public_key = file(var.public_key_path)
}

# EC2 instance for MLflow tracking server
module "mlflow_tracking_server" {
  source        = "../ec2"
  name          = var.name
  instance_type = var.instance_type
  ami_id        = var.ami_id
  subnet_id     = var.subnet_id
  vpc_security_group_ids = [aws_security_group.mlflow_ec2_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.mlflow_ec2_profile.name
  key_name      = aws_key_pair.mlflow_key_pair.key_name
  user_data = file("user_data.sh")
}

# S3 bucket for MLflow artifact store
module "mlflow_artifact_store" {
  source        = "../s3"
  bucket_name   = "my-mlflow-artifacts-mlops2"
  force_destroy = true
  tags = {
    Environment = "Production"
    Project     = "MLOps"
  }
}

# RDS PostgreSQL instance for MLflow backend store
module "mlflow_db" {
  source            = "../rds-postgresql"
  identifier        = "mlflow-backend"
  username          = "mlflow"
  db_name           = "mlflow"
  password          = var.mlflow_backend_password
  vpc_id            = var.vpc_id
  vpc_cidr          = var.vpc_cidr
  subnet_ids        = var.subnet_ids
}