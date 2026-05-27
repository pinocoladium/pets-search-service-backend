# Pets Search Service Backend

Backend-сервис для поиска, размещения и сопоставления объявлений о домашних животных.

Проект включает Django API, PostgreSQL/PostGIS, MinIO для хранения файлов, Telegram-бота, Docker Compose, мониторинг и security-проверки в CI/CD.

## Стек

- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL + PostGIS
- MinIO / S3-compatible storage
- Telegram bot на aiogram
- Docker / Docker Compose
- GitHub Actions
- Trivy, Gitleaks, Syft
- Ollama для AI-функций

## Возможности проекта

- регистрация и работа с пользователями;
- объявления о потерянных животных;
- объявления о найденных животных;
- объявления о животных для пристройства;
- коммуникации между пользователями;
- жалобы;
- Telegram-бот;
- загрузка и хранение файлов через MinIO;
- AI-функции через Ollama:
  - ответ на вопрос пользователя;
  - описание животного по изображению;
  - улучшение текста объявления;
  - генерация заголовка объявления;
  - проверка объявления на полноту.

## Структура проекта

```text
.
├── api/                    # API-слой: views, serializers, urls
├── apps/                   # Бизнес-логика приложения
├── pets_search_service/    # Django settings и корневой роутинг
├── telegram/               # Telegram bot
├── tests/                  # Тесты
├── monitoring/             # Мониторинг
├── terraform/              # Terraform-инфраструктура
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── .environment.example
```

## Быстрый запуск

### 1. Склонировать репозиторий

```bash
git clone https://github.com/pinocoladium/pets-search-service-backend.git
cd pets-search-service-backend
```

### 2. Создать файл окружения

```bash
cp .environment.example .environment
```

Заполните значения в `.environment`.

Минимальные переменные:

```env
SECRET_KEY=secret_key
DEBUG=True
SERVER_HOST=*

POSTGRES_DB=postgres
POSTGRES_USER=username
POSTGRES_PASSWORD=password
DEFAULT_DB_HOST=postgres-main
DEFAULT_DB_PORT=5432

MINIO_ENDPOINT=http://minio:9000
MINIO_BUCKET_NAME=pets-search-bucket-minio
MINIO_ROOT_USER=miniousername
MINIO_ROOT_PASSWORD=miniopassword

TELEGRAM_BOT_TOKEN=telegram_bot_token
DJANGO_BASE_API_URL=http://django:8000/api
```

Если используется Ollama:

```env
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_VISION_MODEL=qwen2.5vl:3b
```

### 3. Собрать и запустить контейнеры

```bash
docker compose up -d --build
```

Или через Makefile:

```bash
make build
make up
```

### 4. Применить миграции

```bash
make migrate
```

Или напрямую:

```bash
docker compose exec django python manage.py migrate
```

### 5. Открыть API-документацию

```text
http://localhost:8000/api/docs/
```

Схема OpenAPI:

```text
http://localhost:8000/api/schema/
```

## Основные сервисы Docker Compose

| Сервис | Назначение | Порт |
|---|---|---:|
| `django` | Backend API | 8000 |
| `postgres-main` | PostgreSQL/PostGIS | 5432 |
| `minio` | S3-compatible storage | 9000, 9001 |
| `telegram-bot` | Telegram bot | — |
| `ollama` | Локальная LLM-модель | 11434 |

## Ollama

Ollama используется для AI-функций проекта.

### Скачать текстовую модель

```bash
docker compose exec ollama ollama pull qwen2.5:3b
```

### Скачать vision-модель

```bash
docker compose exec ollama ollama pull qwen2.5vl:3b
```

### Проверить список моделей

```bash
docker compose exec ollama ollama list
```

Чтобы модели не скачивались заново при каждом запуске, для Ollama должен использоваться постоянный volume:

```yaml
volumes:
  - ollama_data:/root/.ollama
```

## AI endpoints

Если AI-роуты подключены в `api/urls.py`, доступны следующие endpoint-ы:

```text
POST /api/ai/ollama/ask/
POST /api/ai/ollama/pet-description/
POST /api/ai/ollama/improve-announcement/
POST /api/ai/ollama/generate-title/
POST /api/ai/ollama/check-announcement/
```

### Пример запроса к текстовой модели

```http
POST /api/ai/ollama/ask/
Content-Type: application/json

{
  "question": "Как правильно составить объявление о найденной собаке?"
}
```

### Пример ответа

```json
{
  "result": "Укажите место, дату, внешний вид животного, особые приметы и способ связи."
}
```

### Пример запроса на описание изображения

Endpoint принимает `multipart/form-data`:

```text
image: файл изображения
```

Ответ:

```json
{
  "description": "На фото рыжая собака среднего размера. Видны короткая шерсть и ошейник."
}
```

## Полезные команды

### Логи

```bash
make logs
```

Логи конкретного контейнера:

```bash
make logs c=django
make logs c=telegram-bot
```

### Войти в контейнер

```bash
make exec
```

Или:

```bash
docker compose exec django bash
```

### Создать миграции

```bash
make migrations
```

### Применить миграции

```bash
make migrate
```

### Django shell

```bash
make shell
```

### Остановить проект

```bash
make down
```

Или:

```bash
docker compose down
```

## Тесты

Запуск тестов:

```bash
docker compose exec django pytest
```

Запуск конкретного теста:

```bash
docker compose exec django pytest tests/path/to/test_file.py
```

## Pre-commit

В проекте используется pre-commit.

Запуск всех проверок:

```bash
make pre-commit
```

Или:

```bash
pre-commit run --all-files
```

## Security

В проекте настроен security pipeline.

Проверки:

- Gitleaks — поиск секретов;
- Trivy FS — проверка зависимостей и файлов проекта;
- Syft — генерация SBOM;
- Trivy Image Scan — проверка Docker-образов;
- Bandit — SAST для Python;
- pip-audit — проверка Python-зависимостей.

Security workflow находится в:

```text
.github/workflows/ci-security.yml
```

Отчёты сохраняются как GitHub Actions artifacts:

```text
gitleaks-report.json
trivy-fs-report.json
trivy-image-report-backend.json
trivy-image-report-telegram-bot.json
sbom.json
```

## Мониторинг

В проекте предусмотрен monitoring stack:

- Prometheus;
- Grafana;
- Loki;
- Promtail;
- Alertmanager;
- Node Exporter.

Если monitoring stack запущен, основные сервисы доступны по адресам:

```text
Prometheus:   http://localhost:9090
Grafana:      http://localhost:3000
Alertmanager: http://localhost:9093
```

## Работа с MinIO

MinIO console:

```text
http://localhost:9001
```

Данные для входа задаются в `.environment`:

```env
MINIO_ROOT_USER=miniousername
MINIO_ROOT_PASSWORD=miniopassword
```

## Важные замечания

- Не храните реальные секреты в Git.
- Не коммитьте `.environment`.
- Для локальной разработки используйте `.environment.example` как шаблон.
- Для production-запуска лучше использовать `gunicorn`, а не `runserver`.
- Для Ollama-моделей используйте volume, чтобы модели не скачивались повторно.
- Если используется `ImageField`, в зависимостях должен быть установлен `Pillow`.

## Лицензия

Учебный проект.
