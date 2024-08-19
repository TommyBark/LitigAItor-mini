resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  force_destroy = var.force_destroy
  tags = merge(
    {
      Name = var.bucket_name
    },
    var.tags
  )
}
