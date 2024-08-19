output "prefect_server_public_ip" {
  description = "The public IP address of the Prefect Orion server"
  value       = "http://${module.prefect_ec2.public_ip}:4200"
}