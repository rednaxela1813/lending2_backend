from .base import *

# Dedicated test settings keep pytest self-contained (no external Postgres).

DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

# Fast hashers keep the suite nimble.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Keep emails and media local to the test run.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "test_media"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
