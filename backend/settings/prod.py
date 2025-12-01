from .base import *
from decouple import config

# --- helpers ----------------------------------------------------------
def _csv(name: str, default: str = "") -> list[str]:
    val = config(name, default=default)
    return [s.strip() for s in val.split(",") if s.strip()]

def _as_https(origin_or_host: str) -> str:
    if origin_or_host.startswith("http://"):
        return "https://" + origin_or_host[7:]
    if origin_or_host.startswith("https://"):
        return origin_or_host
    return f"https://{origin_or_host}"

# --- core -------------------------------------------------------------
DEBUG = False
ALLOWED_HOSTS = _csv("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1")

CORS_ALLOWED_ORIGINS = _csv("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = False

# CSRF: читаем из env и добавляем https:// для всех ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = _csv("CSRF_TRUSTED_ORIGINS")
for host in ALLOWED_HOSTS:
    https_origin = _as_https(host)
    if https_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(https_origin)

INSTALLED_APPS += ["axes"]
MIDDLEWARE = ["axes.middleware.AxesMiddleware"] + MIDDLEWARE
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hours

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

TIME_ZONE = "Europe/Bratislava"
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 1 year; adjust if you need a gradual rollout
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False  # set to True only after confirming preload readiness
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID", default="")

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "cache-for-ratelimiting": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "ratelimit-cache",
    },
}
RATELIMIT_USE_CACHE = "cache-for-ratelimiting"

from apps.site_logging.config import get_logging_config

LOGGING = get_logging_config(debug=DEBUG)
