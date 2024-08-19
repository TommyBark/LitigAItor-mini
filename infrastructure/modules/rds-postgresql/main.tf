resource "aws_db_subnet_group" "default" {
  name       = "${var.identifier}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.identifier}-subnet-group"
  }
}

resource "aws_security_group" "default" {
  name        = "${var.identifier}-sg"
  description = "Allow inbound traffic for PostgreSQL"
  vpc_id      = var.vpc_id

  ingress {
    description = "PostgreSQL from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.identifier}-sg"
  }
}

resource "aws_db_instance" "default" {
  identifier           = var.identifier
  instance_class       = var.instance_class
  allocated_storage    = var.allocated_storage
  engine               = "postgres"
  engine_version       = var.engine_version
  username             = var.username
  password             = var.password
  db_subnet_group_name = aws_db_subnet_group.default.name
  db_name = var.db_name
  vpc_security_group_ids = [aws_security_group.default.id]
  publicly_accessible  = false
  skip_final_snapshot  = true

  tags = {
    Name = var.identifier
  }
}