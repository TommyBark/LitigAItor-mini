# # Use the aws-base module
module "base" {
  source = "../modules/aws-base"  # Adjust this path to where your aws-base module is located

  region               = "eu-west-1"
  project_name         = "LitigAItor-mini"
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zones   = ["eu-west-1a", "eu-west-1b"]
}

module "prefect" {
  source = "../modules/prefect"

  # EC2
  instance_type = "t2.micro"
  ami_id = "ami-0c38b837cd80f13bb"

  # Networking
  subnet_id = module.base.public_subnet_ids[0]
  vpc_cidr = module.base.vpc_cidr
  vpc_id = module.base.vpc_id
  # SSH authentication
  public_key_path = "~/.ssh/prefect_key.pub"
  prefect_ingress_cidr_blocks = var.prefect_ingress_cidr_blocks 
}

output "prefect_server_public_ip" {
  description = "The public IP address of the Prefect Orion server"
  value       = module.prefect.prefect_server_public_ip
}

output "prefect_worker_public_ip" {
  description = "The public IP address of the Prefect worker"
  value       = module.prefect.prefect_worker_public_ip
}
