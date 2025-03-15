# Кассовый аппарат (Cash Register)

Веб-приложение для работы с кассовым аппаратом, позволяющее создавать чеки с QR-кодами.

## Возможности

- Создание и управление товарами
- Генерация чеков с QR-кодами
- REST API для интеграции
- Документация API через Swagger
- Безопасная аутентификация
- Ограничение частоты запросов

## Требования

- Python 3.8+
- wkhtmltopdf
- uv

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/docryte/cash-register.git
cd cash-register
```

2. Создайте виртуальное окружение:
```
uv v
```

3. Установите зависимости:
```bash
uv sync
```

4. Настройте окружение на основе .env.example.

4. Примените миграции:
```bash
python manage.py migrate
```
5. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Развертывание

### Docker

1. Соберите образ:
```bash
docker build -t cash-register .
```

2. Запустите контейнер:
```bash
docker run -p 8000:8000 cash-register
```

### На продакшене

1. Установите и настройте PostgreSQL
2. Настройте Nginx
3. Настройте SSL-сертификаты
4. Используйте gunicorn или uwsgi

## API Документация

После запуска сервера, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
