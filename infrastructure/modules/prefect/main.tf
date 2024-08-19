# Create a security group for Prefect
resource "aws_security_group" "prefect_sg" {
  name        = "${var.project_name}-prefect-sg"
  description = "Security group for Prefect Orion server"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.prefect_ingress_cidr_blocks
  }

  ingress {
    from_port   = 4200
    to_port     = 4200
    protocol    = "tcp"
    cidr_blocks = var.prefect_ingress_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-prefect-sg"
  }
}

resource "aws_key_pair" "prefect_key_pair" {
  key_name   = "${var.project_name}-prefect-key"
  public_key = file(var.public_key_path)
}

# Use the EC2 module
module "prefect_ec2" {
  source = "../ec2"  # Adjust this path to where your EC2 module is located

  name                    = "${var.project_name}-prefect-orion-server"
  ami_id                  = var.ami_id
  instance_type           = var.instance_type
  subnet_id               = var.subnet_id
  vpc_security_group_ids  = [aws_security_group.prefect_sg.id]
  key_name                = aws_key_pair.prefect_key_pair.key_name
  user_data               = file("${path.module}/user_data.sh")
  
  tags = {
    Project = var.project_name
  }
}