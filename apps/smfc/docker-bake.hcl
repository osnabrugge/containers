target "docker-metadata-action" {}

variable "APP" {
  default = "smfc"
}

variable "VERSION" {
  default = "6.5.0-homeops.1"
}

variable "SOURCE" {
  default = "https://github.com/petersulyok/smfc"
}

group "default" {
  targets = ["image-local"]
}

target "image" {
  inherits = ["docker-metadata-action"]
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
  platforms = ["linux/amd64"]
}
