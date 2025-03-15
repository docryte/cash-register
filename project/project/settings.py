from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"  # По умолчанию True для разработки
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Настройки безопасности
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False") == "True"
)
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "False") == "True"
SECURE_BROWSER_XSS_FILTER = os.getenv("SECURE_BROWSER_XSS_FILTER", "True") == "True"
SECURE_CONTENT_TYPE_NOSNIFF = os.getenv("SECURE_CONTENT_TYPE_NOSNIFF", "True") == "True"
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False

# Настройки сессии
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    CSRF_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = None
    CSRF_COOKIE_SAMESITE = None

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_yasg",
    "store",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
]

if not DEBUG:
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        *MIDDLEWARE,
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WKHTMLTOPDF_PATH = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

# Настройки статических файлов
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

# Настройки медиафайлов
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Настройки логирования
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Настройки кэширования
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Настройки REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "100/day",
    },
}
