provider "aws" {
  region = "us-east-1"
}

resource aws_key_pair "one_click_react" {
  key_name = "id_rsa_reaft"
  public_key = "${file("${var.path_to_public_key}")}"
}

resource "aws_instance" "react-client" {
  ami = "ami-0947d2ba12ee1ff75"
  instance_type = "t2.micro"
  key_name = "${aws_key_pair.one_click_react.key_name}"

  vpc_security_group_ids = ["${aws_security_group.allow_react_and_ssh.id}"]
}

resource "aws_security_group" "allow_react_and_ssh" {
  name = "allow_react_and_ssh"

  ingress {
    protocol = "tcp"
    from_port = 80
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
}

  ingress {
    protocol = "tcp"
    from_port = 22
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol = "tcp"
    from_port = 3000
    to_port = 3000
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "provision_project" {
  source = "./provision_project"

  host = "${aws_instance.react-client.public_dns}"
  path_to_private_key = "${var.path_to_private_key}"
  base_directory = "/Users/mac/Desktop/NEU/Csye7220/midterm/terraform/frontend/provision_project"
  project_link_or_path = "foo"
  image_version = "bar"
  use_github = "nope"
  use_local = "yep"
  public_ip = "${aws_instance.react-client.public_dns}"
}
