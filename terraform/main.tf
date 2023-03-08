
provider "aws" {
    profile = "default"
    region = "eu-north-1"
}
resource "aws_instance" "flask_server" {
    ami           = var.ami_key
    instance_type = var.ec2_instance_type
    
    tags = {
        Name=var.instance_name
    }
}
resource "aws_security_group" "example" {
  name_prefix = "Website security group"
  description = "Opens port 80, 443 and 22"

  ingress {
    from_port=80
    to_port=80
    protocol="tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port=443
    to_port=443
    protocol="tcp"
    cidr_blocks=["0.0.0.0/0"]
  }
  ingress {
    from_port=22
    to_port=22
    protocol="tcp"
    cidr_blocks=["0.0.0.0/0"]
  }
}