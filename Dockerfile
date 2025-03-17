FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV DJANGO_SECRET_KEY="your-secret-key-here"
ENV DEBUG="True"
ENV ALLOWED_HOSTS="localhost,127.0.0.1"
ENV DATABASE_URL=sqlite:///db.sqlite3
ENV SECURE_SSL_REDIRECT="False"
ENV SECURE_HSTS_SECONDS="31536000"
ENV SECURE_HSTS_INCLUDE_SUBDOMAINS="True"
ENV SECURE_HSTS_PRELOAD="True"
ENV SECURE_BROWSER_XSS_FILTER="True"
ENV SECURE_CONTENT_TYPE_NOSNIFF="True"

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