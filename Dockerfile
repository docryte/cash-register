FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"] 