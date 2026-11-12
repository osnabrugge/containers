target "docker-metadata-action" {}

variable "APP" {
  default = "printstash-api"
}

variable "VERSION" {
  default = "0.15.1-homeops.2"
}

variable "SOURCE" {
  default = "https://github.com/xiao-villamor/PrintStash"
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
