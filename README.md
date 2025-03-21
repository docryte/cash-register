# Кассовый аппарат (Cash Register)

Веб-приложение для работы с кассовым аппаратом, позволяющее создавать чеки с QR-кодами. Код может выглядеть переусложнённым для такой задачи, но так я хотел показать понимание принципов и практик.

## Возможности

- Создание и управление товарами
- Генерация чеков с QR-кодами
- REST API для интеграции
- Документация API через Swagger
- Ограничение частоты запросов

## Требования

- Python 3.13+
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

5. Примените миграции:
```bash
python manage.py migrate
```
6. Запустите сервер разработки:
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

## API Документация

После запуска сервера, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
