terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Define a dedicated local network for your ML studio stack
resource "docker_network" "enterprise_ml_network" {
  name   = "enterprise_ml_net"
  driver = "bridge"
}

output "network_name" {
  value       = docker_network.enterprise_ml_network.name
  description = "The name of the local Docker network managed by Terraform."
}