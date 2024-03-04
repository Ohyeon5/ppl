terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  skip_provider_registration = true # This is only required when the User, Service Principal, or Identity running Terraform lacks the permissions to register Azure Resource Providers.
  features {}
}

resource "azurerm_resource_group" "ppl-rg" {
  name     = "ppl-resources"
  location = "East US"
  tags = {
    environment = "dev"
  }
}

resource "azurerm_virtual_network" "ppl-vn" {
  name                = "ppl-network"
  location            = azurerm_resource_group.ppl-rg.location
  resource_group_name = azurerm_resource_group.ppl-rg.name
  address_space       = ["10.64.0.0/10"]

  tags = {
    environment = "dev"
  }
}

resource "azurerm_subnet" "ppl-sn" {
  name                 = "ppl-subnet-1"
  resource_group_name  = azurerm_resource_group.ppl-rg.name
  virtual_network_name = azurerm_virtual_network.ppl-vn.name
  address_prefixes     = ["10.64.1.0/24"]
}

resource "azurerm_network_security_group" "ppl-nsg" {
  name                = "ppl-nsg"
  location            = azurerm_resource_group.ppl-rg.location
  resource_group_name = azurerm_resource_group.ppl-rg.name

  tags = {
    environment = "dev"
  }
}

resource "azurerm_network_security_rule" "ppl-dev-rule" {
  name                        = "ppl-dev-rule"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.ppl-rg.name
  network_security_group_name = azurerm_network_security_group.ppl-nsg.name
}
