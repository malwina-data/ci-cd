packer {
  required_plugins {
    ansible = {
      version = ">= 1.0.0"
      source = "github.com/hashicorp/ansible"
    }
  }
}

variable "region" {}
variable "az" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "vpc_id" {}
variable "igw_id" {}
variable "db_subnet_id" {}
variable "web_subnet_id" {}
variable "db_route_table_id" {}
variable "web_route_table_id" {}
variable "security_group_id" {}

# Define source block
source "amazon-ebs" "example" {
  region                  = var.region
  instance_type           = "t3.micro"
  ami_name                = "db-amiii"
  source_ami              = "ami-04eeb630f180cea95"
  ssh_username            = "ec2-user"
  associate_public_ip_address = true
  vpc_id                  = var.vpc_id
  subnet_id               = var.db_subnet_id
  security_group_ids      = [var.security_group_id]
}

build {
  sources = [
    "source.amazon-ebs.example"
  ]

  provisioner "ansible" {
    playbook_file = "Packer_db_set_up.yaml"
    
  }
}