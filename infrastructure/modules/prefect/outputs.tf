output "prefect_server_public_ip" {
  description = "The public IP address of the Prefect Orion server"
  value       = "http://${module.prefect_server_ec2.public_ip}:4200"
}

output "prefect_worker_public_ip" {
  description = "The public IP address of the Prefect worker"
  value       = module.prefect_worker_ec2.public_ip
}

output "prefect_worker_private_ip" {
  description = "The private IP address of the Prefect worker"
  value       = module.prefect_worker_ec2.private_ip
}