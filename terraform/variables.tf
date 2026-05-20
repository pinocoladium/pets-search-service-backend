variable "docker_host" {
  description = "Docker daemon host"
  type        = string
  default     = "unix:///var/run/docker.sock"
}

variable "ghcr_username" {
  description = "GitHub username для доступа к GHCR"
  type        = string
}

variable "ghcr_token" {
  description = "GitHub Personal Access Token с правом read:packages"
  type        = string
  sensitive   = true
}

variable "network_name" {
  description = "Имя Docker-сети приложения"
  type        = string
  default     = "pets-search-service-network"
}

variable "app_replicas" {
  description = "Количество реплик Django-приложения"
  type        = number
  default     = 1
}

variable "backend_image_tag" {
  description = "Тег Docker-образа backend из GHCR"
  type        = string
  default     = "latest"
}

variable "telegram_bot_image_tag" {
  description = "Тег Docker-образа Telegram-бота из GHCR"
  type        = string
  default     = "latest"
}

variable "postgres_image_tag" {
  description = "Тег Docker-образа PostgreSQL/PostGIS"
  type        = string
  default     = "16-3.4-alpine"
}

variable "minio_image_tag" {
  description = "Тег Docker-образа MinIO"
  type        = string
  default     = "latest"
}

variable "app_internal_port" {
  description = "Внутренний порт Django-контейнера"
  type        = number
  default     = 8000
}

variable "app_external_port" {
  description = "Внешний порт первой реплики Django. Для следующих реплик порт увеличивается на 1"
  type        = number
  default     = 8000
}

variable "postgres_external_port" {
  description = "Внешний порт PostgreSQL"
  type        = number
  default     = 5432
}

variable "minio_api_external_port" {
  description = "Внешний порт MinIO API"
  type        = number
  default     = 9000
}

variable "minio_console_external_port" {
  description = "Внешний порт MinIO Console"
  type        = number
  default     = 9001
}

variable "django_secret_key" {
  description = "Секретный ключ Django"
  type        = string
  sensitive   = true
}

variable "django_debug" {
  description = "Режим debug для Django"
  type        = string
  default     = "False"
}

variable "django_allowed_hosts" {
  description = "Разрешённые хосты Django"
  type        = string
  default     = "*"
}

variable "postgres_db" {
  description = "Название базы данных"
  type        = string
}

variable "postgres_user" {
  description = "Пользователь PostgreSQL"
  type        = string
}

variable "postgres_password" {
  description = "Пароль PostgreSQL"
  type        = string
  sensitive   = true
}

variable "minio_root_user" {
  description = "Пользователь MinIO"
  type        = string
}

variable "minio_root_password" {
  description = "Пароль MinIO"
  type        = string
  sensitive   = true
}

variable "minio_bucket_name" {
  description = "Bucket для файлов приложения"
  type        = string
}

variable "telegram_bot_token" {
  description = "Токен Telegram-бота"
  type        = string
  sensitive   = true
}