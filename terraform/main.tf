locals {
  backend_image       = "ghcr.io/pinocoladium/pets-search-service-backend:${var.backend_image_tag}"
  telegram_bot_image  = "ghcr.io/pinocoladium/pets-search-service-telegram-bot:${var.telegram_bot_image_tag}"
  postgres_image      = "postgis/postgis:${var.postgres_image_tag}"
  minio_image         = "minio/minio:${var.minio_image_tag}"

  common_env = [
    "DJANGO_SECRET_KEY=${var.django_secret_key}",
    "DJANGO_DEBUG=${var.django_debug}",
    "DJANGO_ALLOWED_HOSTS=${var.django_allowed_hosts}",

    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_HOST=pets-search-service-postgres-main",
    "POSTGRES_PORT=5432",

    "MINIO_ENDPOINT=http://pets-search-service-minio:9000",
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}",
    "MINIO_BUCKET_NAME=${var.minio_bucket_name}",

    "PYTHONUNBUFFERED=1"
  ]
}

resource "docker_network" "app_network" {
  name = var.network_name
}

resource "docker_volume" "postgres_data" {
  name = "pets-search-service-postgres-data"
}

resource "docker_volume" "minio_data" {
  name = "pets-search-service-minio-data"
}

resource "docker_image" "backend" {
  name         = local.backend_image
  keep_locally = true
}

resource "docker_image" "telegram_bot" {
  name         = local.telegram_bot_image
  keep_locally = true
}

resource "docker_image" "postgres" {
  name         = local.postgres_image
  keep_locally = true
}

resource "docker_image" "minio" {
  name         = local.minio_image
  keep_locally = true
}

resource "docker_container" "postgres" {
  name  = "pets-search-service-postgres-main"
  image = docker_image.postgres.image_id

  restart = "unless-stopped"

  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}"
  ]

  ports {
    internal = 5432
    external = var.postgres_external_port
  }

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

resource "docker_container" "minio" {
  name  = "pets-search-service-minio"
  image = docker_image.minio.image_id

  restart = "unless-stopped"

  command = [
    "server",
    "--console-address",
    ":9001",
    "/data"
  ]

  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]

  ports {
    internal = 9000
    external = var.minio_api_external_port
  }

  ports {
    internal = 9001
    external = var.minio_console_external_port
  }

  volumes {
    volume_name    = docker_volume.minio_data.name
    container_path = "/data"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

resource "docker_container" "django" {
  count = var.app_replicas

  name  = "pets-search-service-backend-${count.index + 1}"
  image = docker_image.backend.image_id

  restart = "unless-stopped"

  env = local.common_env

  ports {
    internal = var.app_internal_port
    external = var.app_external_port + count.index
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [
    docker_container.postgres,
    docker_container.minio
  ]
}

resource "docker_container" "telegram_bot" {
  name  = "pets-search-service-telegram-bot"
  image = docker_image.telegram_bot.image_id

  restart = "unless-stopped"

  env = concat(
    local.common_env,
    [
      "TELEGRAM_BOT_TOKEN=${var.telegram_bot_token}",
      "DJANGO_BASE_API_URL=http://pets-search-service-backend-1:8000/api"
    ]
  )

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [
    docker_container.django
  ]
}