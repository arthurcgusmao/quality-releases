variable "application_type" {}
variable "location" {}
variable "resource_group" {}
variable "resource_type" {}
variable "subnet_id" {}
variable "public_ip_address_id" {}
variable "vm_size" {}
variable "ssh_public_key_path" {
  default = "~/.ssh/id_rsa.pub"
}
