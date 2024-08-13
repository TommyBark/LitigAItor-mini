# modules/vpc/main.tf

resource "aws_vpc" "mlflow_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "mlflow_subnet" {
  vpc_id     = aws_vpc.mlflow_vpc.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_internet_gateway" "mlflow_igw" {
  vpc_id = aws_vpc.mlflow_vpc.id
}

resource "aws_route_table" "mlflow_route_table" {
  vpc_id = aws_vpc.mlflow_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mlflow_igw.id
  }
}

resource "aws_route_table_association" "mlflow_route_table_association" {
  subnet_id      = aws_subnet.mlflow_subnet.id
  route_table_id = aws_route_table.mlflow_route_table.id
}

resource "aws_security_group" "mlflow_sg" {
  vpc_id = aws_vpc.mlflow_vpc.id

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

output "vpc_id" {
  value = aws_vpc.mlflow_vpc.id
}

output "subnet_id" {
  value = aws_subnet.mlflow_subnet.id
}

output "security_group_id" {
  value = aws_security_group.mlflow_sg.id
}

