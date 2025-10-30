from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

ALLOWED_ORIGINS = config("ALLOWED_ORIGINS", default="", cast=lambda v: [s.strip() for s in v.split(",")])



INSTALLED_APPS = [
    
    "django_filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    
    'rest_framework',
    'corsheaders',
#  'ratelimit',
    
    'tailwind',
    'theme',
    'widget_tweaks',
    
    'contact_form',
    
    'accounting',
    'csm',
    'core',
    
    'properties',
    'orders',
    'dashboard',
    'apps.contact_messages',
]

TAILWIND_APP_NAME = 'theme'


PRIVACY_POLICY_VERSION = "2025-10-01"
PRIVACY_POLICY_UPDATED = "2025-10-01"

FERNET_KEYS = [k for k in [
    config("FERNET_KEY_CURRENT", default=None),
    config("FERNET_KEY_OLD1", default=None),
    config("FERNET_KEY_OLD2", default=None),
] if k]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    
    
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'csm.context_processor.company_info',

            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_USER_MODEL = "accounting.CustomUser"


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard:home"

LOGOUT_REDIRECT_URL = "/"


REQUIRE_VERIFIED_EMAIL_FOR_ORDER = True
