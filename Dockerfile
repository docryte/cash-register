FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY uv.lock .

RUN uv v && uv sync --frozen

COPY . .

RUN mkdir -p /app/logs

CMD ["uv", "run", "project/manage.py", "runserver", "0.0.0.0:8000"] 