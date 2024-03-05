terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.0.0"
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
  location = "westus2"
  tags = {
    environment = "dev"
  }
}

resource "azurerm_static_site" "ppl-swa" {
  name                = "ppl-swa"
  resource_group_name = azurerm_resource_group.ppl-rg.name
  location            = azurerm_resource_group.ppl-rg.location
  sku_tier            = "Free"
  sku_size            = "Free"

  tags = {
    environment = "dev"
  }
}

output "resource_group_name" {
  description = "The name of the Resource Group."
  value       = azurerm_resource_group.ppl-rg.name
}

output "static_web_app_id" {
  description = "The ID of the Static Web App."
  value       = azurerm_static_site.ppl-swa.id
}

output "static_web_app_default_hostname" {
  description = "The default hostname associated with the Static Web App."
  value       = azurerm_static_site.ppl-swa.default_host_name
}

output "static_web_app_api_key" {
  description = "The API key of the Static Web App."
  value       = azurerm_static_site.ppl-swa.api_key
}

resource "azurerm_service_plan" "ppl-sp" {
  name                = "ppl-sp"
  resource_group_name = azurerm_resource_group.ppl-rg.name
  location            = azurerm_resource_group.ppl-rg.location
  os_type             = "Linux"
  sku_name            = "P1v2"

  tags = {
    environment = "dev"
  }
}

resource "azurerm_linux_web_app" "ppl-api" {
  name                = "ppl-api"
  resource_group_name = azurerm_resource_group.ppl-rg.name
  location            = azurerm_service_plan.ppl-sp.location
  service_plan_id     = azurerm_service_plan.ppl-sp.id

  site_config {}

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://utils.azurecr.io/",
  }
}

output "web_app_name" {
  description = "The name of the Web App."
  value       = azurerm_linux_web_app.ppl-api.name
}
