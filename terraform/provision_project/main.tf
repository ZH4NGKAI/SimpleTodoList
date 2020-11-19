resource "null_resource" "remote_exec_from_github" {

  connection {
    host = "${var.host}"
    type = "ssh"
    user = "ec2-user"
    private_key = "${file("/Users/mac/.ssh/id_rsa")}"
  }

  provisioner "file" {
    source = "/Users/mac/Desktop/NEU/Csye7220/midterm/terraform/resources/app"
    destination = "/home/ec2-user"
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir /home/ec2-user/app2",
      "sudo yum install git -y",
      "git clone https://github.com/dinorows/rxshell.git /home/ec2-user/app2",
    ]
  }
}
