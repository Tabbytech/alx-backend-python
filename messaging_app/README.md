
# Messaging App (Dockerized)

A secure messaging application built with Django and Django REST Framework, now fully containerized with Docker & Docker Compose. Supports user registration, JWT-based authentication, real-time-like conversations, message handling, custom permissions, pagination, and filtering.

---

## Features

- **JWT Authentication** (using `djangorestframework-simplejwt`)
- Custom User Model (UUID-based)
- Conversations & Messaging System
- Fine-grained Permissions (only participants access conversations/messages)
- Pagination (20 messages per page)
- Filtering (filter messages by date range & conversation)
- Fully Dockerized (Docker & Docker Compose with MySQL)
- API tested with Postman

---

## Tech Stack

- Django 5.2
- Django REST Framework (DRF)
- SimpleJWT
- django-filter
- MySQL (via Docker)
- Docker & Docker Compose

---

## Local Setup (Dockerized)

### 1. Clone the Repository

```bash
git clone https://github.com/Tabbytech/alx-backend-python.git
cd alx-backend-python/messaging_app
```

### 2. Create `.env` File

```bash
cp .env.example .env
```

Fill in `.env`:

```env
MYSQL_DATABASE=messaging_db
MYSQL_USER=messaging_user
MYSQL_PASSWORD=messaging_password
MYSQL_ROOT_PASSWORD=rootpassword

DB_NAME=messaging_db
DB_USER=messaging_user
DB_PASSWORD=messaging_password
DB_HOST=db
DB_PORT=3306
```

### 3. Build Docker Containers

```bash
docker-compose build
```

### 4. Run Containers

```bash
docker-compose up
```

### 5. Apply Migrations

In a separate terminal, run:

```bash
docker-compose exec web python manage.py migrate
```

### 6. (Optional) Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Authentication Endpoints

### Register

`POST /api/auth/register/`

```json
{
  "email": "user@example.com",
  "username": "tee_ann",
  "password": "password123",
  "first_name": "Tee",
  "last_name": "Ann",
  "phone_number": "1236547890"
}
```

### Login (returns JWT tokens)

`POST /api/auth/login/`

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

---

## Conversations & Messages API

### Create Conversation

`POST /api/conversations/`

### Send Message

`POST /api/messages/`

```json
{
  "conversation": "uuid-of-conversation",
  "message_body": "Hello!"
}
```

### Get Messages (Paginated & Filtered)

`GET /api/messages/?conversation=<uuid>&sent_at__gte=2024-01-01&sent_at__lte=2024-12-31&page=1`

---

## configuration Highlights

### Django Settings (`settings.py`)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'chats.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

---

## Docker Setup Overview

### Dockerfile

- Based on `python:3.10-slim`
- Installs Python dependencies from `requirements.txt`
- Runs Django app on port 8000

### docker-compose.yml

- Defines two services:

  - `web`: Django app container.
  - `db`: MySQL 8.0 database container with persistent volume.

- Environment variables managed via `.env`.

---

## Persist Data with Docker Volumes

The MySQL service uses a Docker volume (`mysql_data`) to ensure that database data persists across container restarts.



## API Testing

Test API endpoints using Postman:

- Register/Login
- Use JWT in Authorization headers
- CRUD for Conversations & Messages
- Pagination & Filtering
