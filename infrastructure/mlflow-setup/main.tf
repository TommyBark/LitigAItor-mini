module "base" {
  source       = "../modules/aws-base"

  project_name = "LitigAItor-mini"
  region       = "eu-west-1"
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zones   = ["eu-west-1a", "eu-west-1b"]
}

module "mlflow" {
  source = "../modules/mlflow"

  #EC2
  name = "mlflow-prod"
  instance_type = "t2.micro"
  ami_id = "ami-0c38b837cd80f13bb"

  # Networking
  subnet_id = module.base.public_subnet_ids[0]
  vpc_id = module.base.vpc_id
  vpc_cidr = module.base.vpc_cidr
  subnet_ids = module.base.private_subnet_ids

  # DB
  mlflow_backend_password = var.mlflow_db_password

  # Artifact bucket
  artifact_bucket_name = "mlflow-litigator-mlflow-artifacts"
  # SSH authentication
  public_key_path = "~/.ssh/mlflow_key.pub"

}

output "mlflow_tracking_uri" {
  value = module.mlflow.mlflow_tracking_uri
}

output "mlflow_s3_artifact_uri" {
  value = module.mlflow.mlflow_s3_artifact_uri
}
