resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  vpc_security_group_ids = var.vpc_security_group_ids
  iam_instance_profile   = var.iam_instance_profile
  user_data = var.user_data
  key_name = var.key_name
  tags = merge(
    {
      Name = var.name
    },
    var.tags
  )
}