# main.tf

provider "aws" {
  region = var.region
}

module "vpc" {
  source = "./modules/vpc"
}

module "s3" {
  source = "./modules/s3"
  s3_bucket_name = var.s3_bucket_name
}

module "dynamodb" {
  source = "./modules/dynamodb"
  dynamodb_table_name = var.dynamodb_table_name
}

module "ec2" {
  source = "./modules/ec2"
  vpc_id            = module.vpc.vpc_id
  subnet_id         = module.vpc.subnet_id
  security_group_id = module.vpc.security_group_id
  s3_bucket_name    = module.s3.bucket_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
}

output "mlflow_server_public_ip" {
  value = module.ec2.mlflow_server_public_ip
}
