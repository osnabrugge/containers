target "docker-metadata-action" {}

variable "APP" {
  default = "netbox-diode"
}

variable "VERSION" {
  default = "4.7.4"
}

variable "SOURCE" {
  default = "https://github.com/netboxlabs/diode-netbox-plugin"
}

group "default" {
  targets = ["image-local"]
}

target "image" {
  inherits = ["docker-metadata-action"]
  args = {
    VERSION = "${VERSION}"
  }
  labels = {
    "org.opencontainers.image.source" = "${SOURCE}"
  }
}

target "image-local" {
  inherits = ["image"]
  output = ["type=docker"]
  tags = ["${APP}:${VERSION}"]
}

target "image-all" {
  inherits = ["image"]
  platforms = [
    "linux/amd64",
    "linux/arm64"
  ]
}
