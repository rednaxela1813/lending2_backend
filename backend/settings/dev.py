from .base import *


ALLOWED_HOSTS = ['*']
DEBUG = True

#CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=True, cast=bool)


if DEBUG:
    # Add django_browser_reload only in DEBUG mode
    INSTALLED_APPS += ['django_browser_reload']
    
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]
    

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("POSTGRES_DB"),
        'USER': config("POSTGRES_USER"),
        'PASSWORD': config("POSTGRES_PASSWORD"),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Статика (CSS, JS и т.п.)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # куда collectstatic положит статику
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # где лежит твоя пользовательская статика
]

# Медиа (загружаемые пользователем изображения и т.п.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID")

from apps.site_logging.config import get_logging_config

LOGGING = get_logging_config(debug=DEBUG)

# settings.py

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






