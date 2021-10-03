output "public_ip_address_id" {
  value = "${azurerm_public_ip.test.id}"
}
output "ip_address" {
  value = "${azurerm_public_ip.test.ip_address}"
}
