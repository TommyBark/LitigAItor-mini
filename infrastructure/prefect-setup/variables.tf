variable "prefect_ingress_cidr_blocks" {
  description = "List of allowed IPs for the security group"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}