# modules/ec2/main.tf

resource "aws_security_group" "mlflow_sg" {
  vpc_id = var.vpc_id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "mlflow_instance" {
  ami                         = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type               = "t2.micro"
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.security_group_id]
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install python3 -y
              pip3 install mlflow boto3
              
              # Set environment variables
              export MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com
              export AWS_DEFAULT_REGION=us-east-1
              export MLFLOW_TRACKING_URI=http://0.0.0.0:5000

              # Start MLflow server
              mlflow server --backend-store-uri dynamodb://${var.dynamodb_table_name} \
                            --default-artifact-root s3://${var.s3_bucket_name} \
                            --host 0.0.0.0 --port 5000
              EOF

  tags = {
    Name = "MLflow-Server"
  }
}

output "mlflow_server_public_ip" {
  value = aws_instance.mlflow_instance.public_ip
}
