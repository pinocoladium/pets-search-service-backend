output "network_name" {
  description = "Имя Docker-сети"
  value       = docker_network.app_network.name
}

output "postgres_container_name" {
  description = "Имя контейнера PostgreSQL"
  value       = docker_container.postgres.name
}

output "postgres_external_port" {
  description = "Внешний порт PostgreSQL"
  value       = docker_container.postgres.ports[0].external
}

output "minio_container_name" {
  description = "Имя контейнера MinIO"
  value       = docker_container.minio.name
}

output "minio_api_url" {
  description = "URL MinIO API"
  value       = "http://localhost:${docker_container.minio.ports[0].external}"
}

output "minio_console_url" {
  description = "URL MinIO Console"
  value       = "http://localhost:${docker_container.minio.ports[1].external}"
}

output "django_container_names" {
  description = "Имена контейнеров Django-приложения"
  value       = docker_container.django[*].name
}

output "django_urls" {
  description = "URL всех реплик Django-приложения"
  value = [
    for container in docker_container.django :
    "http://localhost:${container.ports[0].external}"
  ]
}

output "telegram_bot_container_name" {
  description = "Имя контейнера Telegram-бота"
  value       = docker_container.telegram_bot.name
}

output "backend_image" {
  description = "Используемый backend-образ"
  value       = docker_image.backend.name
}

output "telegram_bot_image" {
  description = "Используемый образ Telegram-бота"
  value       = docker_image.telegram_bot.name
}