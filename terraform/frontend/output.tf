output "public_dns" {
  value = "${aws_instance.react-client.public_dns}"
}
