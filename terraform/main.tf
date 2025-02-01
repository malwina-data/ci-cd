variable "db_username" {}
variable "db_password" {}
variable "secret_1" {}
variable "secret_2" {}

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

resource "aws_subnet" "main_1"{
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.3.0/24"
    availability_zone = "sa-east-1a"
    tags = {
      Name = "subnet_1a"
    }
}
resource "aws_subnet" "main_2"{
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.4.0/24"
    availability_zone = "sa-east-1b"
    tags = {
      Name = "subnet_1b"
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
  subnet_id = aws_subnet.main_1.id
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
    ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
  }
     ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
  }
  tags = {
    Name = "security_group"
  }
}

output "subnet_id_1" {
  value = aws_subnet.main_1.id
}
output "subnet_id_2" {
  value = aws_subnet.main_2.id
}
resource "aws_db_subnet_group" "db_subnet_group"{
  name = "db-subnet-group"
  subnet_ids = [
    aws_subnet.main_1.id,
    aws_subnet.main_2.id
  ]
  tags = {
    name = "DB Subnet Group"
  }
}
resource "aws_secretsmanager_secret" "db_secret" {
  name        = var.secret_1
}

resource "aws_secretsmanager_secret_version" "db_secret_credentials" {
  secret_id     = aws_secretsmanager_secret.db_secret.id  # Odwołanie do ID sekretu
  secret_string = jsonencode({
    dbname   = "db_postgres"  # Nazwa bazy danych
    username = var.db_username
    password = var.db_password
  })
}
  resource "aws_db_instance" "db_postgres" {
    allocated_storage    = 10
    db_name              = "db_postgres"
    engine               = "postgres"
    engine_version       = "16.3"
    instance_class       = "db.t3.micro"
    skip_final_snapshot  = true
    iam_database_authentication_enabled = true
    db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
    vpc_security_group_ids = [aws_security_group.main.id]
    username             = jsondecode(aws_secretsmanager_secret_version.db_secret_credentials.secret_string)["username"]
    password             = jsondecode(aws_secretsmanager_secret_version.db_secret_credentials.secret_string)["password"]
    port                 = 5432
  }
resource "aws_secretsmanager_secret" "db_connection_secret" {
  name        = var.secret_2
}
resource "aws_secretsmanager_secret_version" "db_secret_string" {
  secret_id     = aws_secretsmanager_secret.db_connection_secret.id
  secret_string = jsonencode({
    connection_string = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.db_postgres.endpoint}:${aws_db_instance.db_postgres.port}/${aws_db_instance.db_postgres.db_name}"
  })
  }
/*
resource "null_resource" "app_start" {
  provisioner "local-exec" {
    command = <<EOT
      export DB_CONNECTION_STRING=$(aws ssm get-parameter --name "/myapp/db_connection_string" --query "Parameter.Value" --output text)
    EOT
  }
}*/
resource "aws_iam_role" "db_iam_role" {
  name = "db-iam-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = ["rds.amazonaws.com", "ec2.amazonaws.com"]
        }
      }
    ]
  })
}
resource "aws_iam_policy" "policy" {
  name        = "my-rds-policy"
  description = "Polityka dostępu do RDS"

  policy = <<EOT
  {
    "Version": "2012-10-17",
    "Statement": [
      {
      "Action": "rds-db:connect",
      "Effect": "Allow",
      "Resource": "*"
      },
      {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "*"
      },
      {
      "Effect": "Allow",
      "Action": "secretsmanager:ListSecrets",
      "Resource": "*"
      }
    ]
  }
  EOT
} 
resource "aws_iam_role_policy_attachment" "policy_attachment" {
  role       = aws_iam_role.db_iam_role.name
  policy_arn = aws_iam_policy.policy.arn
}
resource "aws_iam_instance_profile" "db_instance_profile" {
  name = "db-instance-profile"
  role = aws_iam_role.db_iam_role.name
}
resource "aws_instance" "main" {
  ami           = "ami-015f3596bb2ef1aaa"  # ubuntu distribution
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.main_1.id
  associate_public_ip_address = true
  security_groups = [aws_security_group.main.id]
  iam_instance_profile = aws_iam_instance_profile.db_instance_profile.name
  key_name      = "key-pair"
  tags = {
    Name = "Instance"
  }
}

output "secret01" {
  value = aws_secretsmanager_secret.db_secret.id
}
output "secret_string" {
  value = aws_secretsmanager_secret.db_connection_secret.id
}

output "db_endpoint" {
  value = aws_db_instance.db_postgres.endpoint
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
