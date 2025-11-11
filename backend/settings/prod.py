#  prod.py
from .base import *
from decouple import config

# Разрешённые хосты (обязательно указать явно)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])
DEBUG = False

# CORS (допускаем только известные источники, например фронтенд)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS").split(",")
CORS_ALLOW_ALL_ORIGINS = False


INSTALLED_APPS += [
    "axes",
]

MIDDLEWARE = [
    'axes.middleware.AxesMiddleware',
] + MIDDLEWARE

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AXES_FAILURE_LIMIT = 5 
AXES_COOLOFF_TIME = 1  # 1 hour

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("POSTGRES_DB"),
        'USER': config("POSTGRES_USER"),
        'PASSWORD': config("POSTGRES_PASSWORD"),
        'HOST': config("DB_HOST", default='localhost'),
        'PORT': config("DB_PORT", default='5432'),
    }
}

TIME_ZONE = 'Europe/Bratislava'
USE_TZ = True

#
# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки безопасности
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Позволяем Django понимать, что nginx уже использует HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Бот Telegram (если используется)
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID")

# Кэш
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'cache-for-ratelimiting': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ratelimit-cache',
    }
}
RATELIMIT_USE_CACHE = 'cache-for-ratelimiting'

# Логирование
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# ✅ ЧИТАЕМ из env и автоматически добавляем https:// для всех ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = _csv("CSRF_TRUSTED_ORIGINS")
for host in ALLOWED_HOSTS:
    url = f"https://{host}"
    if url not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(url)
