resource "null_resource" "remote_exec_from_github" {

  connection {
    host = "${var.host}"
    type = "ssh"
    user = "ec2-user"
    private_key = "${file("/Users/mac/Desktop/NEU/Csye7220/midterm/terraform/frontend/id_rsa")}"
  }

  provisioner "file" {
    source = "/Users/mac/Desktop/NEU/Csye7220/midterm/terraform/frontend/resources/chore-frontend"
    destination = "/home/ec2-user"
  }

}
