variable "instance_name" {
    description = "Value of the Name tag for the EC2 instance"
    type = string
    default = "AndreasWebsite"
}

variable "ec2_instance_type"{
    description = "AWS EC2 instance type"
    type = string
    default = "t2.micro"
}

variable "ami_key"{
    description = "Ami-key for the OS to run."
    type = string
    default = "ami-09e1162c87f73958b"
}

variable "cprovider" {
    description = "Cloud provider to deploy to"
    type = string
    default = "aws"
}

variable "region" {
    description = "Server region"
    type = string
    default = "eu-north-1"
}
