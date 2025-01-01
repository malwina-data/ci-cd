provider "aws" {
  region = "sa-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  tags = {
    Name = "Simple-VPC"
  }
}

resource "aws_internet_gateway" "main" {
    vpc_id = aws_vpc.main.id
    tags = {
        Name = "MainInternetGateway"
    }
}


resource "aws_subnet" "main"{
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "sa-east-1a"
    tags = {
      Name = "subnet_1a"
    }
}

resource "aws_route_table" "main"{
    vpc_id = aws_vpc.main.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.main.id
    }
}

resource "aws_route_table_association" "main" {
  subnet_id = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

resource "aws_security_group" "main" {
  vpc_id = aws_vpc.main.id
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 0
    to_port = 65535
    protocol = "tcp"
  }
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 22
    to_port = 22
    protocol = "tcp"
  }
  tags = {
    Name = "security_group"
  }
}
resource "aws_instance" "main" {
  ami           = "ami-015f3596bb2ef1aaa"  # ubuntu distribution
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.main.id
  associate_public_ip_address = true
  security_groups = [aws_security_group.main.id]
  key_name      = "key-pair"
  tags = {
    Name = "Instance"
  }

}
output "subnet_id" {
  value = aws_subnet.main.id
}

output "vpc_id" {
  value = aws_vpc.main.id
}
output "security_group_id" {
  value = aws_security_group.main.id
}
output "instance" {
  value = aws_instance.main.id
}
output "instance_public_ip" {
  value = aws_instance.main.public_ip
  description = "Public IP of the EC2 instance"
}
