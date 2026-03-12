from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

ALLOWED_ORIGINS = config("ALLOWED_ORIGINS", default="", cast=lambda v: [s.strip() for s in v.split(",")])



INSTALLED_APPS = [
    
    "django_filters",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    
    'rest_framework',
    'corsheaders',
#  'ratelimit',
    
    'tailwind',
    'theme',
    'widget_tweaks',
    
    'contact_form',
    
    'accounting',
    'csm.apps.CsmConfig',
    'core',
    
    'apps.properties',
    'orders',
    'apps.company.apps.CompanyConfig',
    'apps.dashboard',
    'apps.contact_messages',
    'apps.site_email',
    'apps.site_logging',
    'apps.site_seo',
    "apps.core_images",
    "apps.hotdeal",
    
    
    "cookie_consent",
]

TAILWIND_APP_NAME = 'theme'


# --- Jazzmin minimal ---
JAZZMIN_SETTINGS = {
    "site_title": "Deilmann Admin",
    "site_header": "Deilmann Admin",
    "site_brand": "Deilmann",
    "welcome_sign": "Управление контентом",
    "copyright": "Deilmann s.r.o.",
    "show_ui_builder": True,  # включи лайв-кастомайзер в правом верхнем углу
    "topmenu_links": [
        # ссылка на твой кастомный дашборд
        {"name": "Dashboard", "url": "dashboard:index", "permissions": ["auth.view_user"]},
        # ссылка на публичный сайт
        {"name": "Site", "url": "/", "new_window": True},
    ],
    "icons": {
        # Иконки для ключевых моделей
        "csm.HeroSection": "fas fa-bullhorn",
        "csm.HeaderSection": "fas fa-layer-group",
        "csm.FooterInfo": "fas fa-shoe-prints",
        "csm.CompanyInfo": "fas fa-building",
        "apps_properties.Property": "fas fa-city",
        "apps_properties.PropertyImage": "far fa-image",
        "orders.Order": "fas fa-shopping-cart",
        "hotdeal.HotDealSection": "fas fa-fire",
        "hotdeal.HotDealItem": "fas fa-percent",
        # по умолчанию
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
}
# опционально — быстрые твики UI (темы/шапка/сайдбар)
JAZZMIN_UI_TWEAKS = {
    "theme": "cosmo",  # потом подберёшь через UI Builder
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_flat_style": True,
}



PRIVACY_POLICY_VERSION = "2025-10-01"
PRIVACY_POLICY_UPDATED = "2025-10-01"


# Email configuration (overridable via .env)
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@example.com")
SITE_EMAIL_RECIPIENTS = config(
    "SITE_EMAIL_RECIPIENTS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", default=10, cast=int)
ADMIN_EMAILS = config(
    "ADMIN_EMAILS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)

ADMIN_NAME = config("ADMIN_NAME", default="Site Admin")
ADMINS = [(ADMIN_NAME, email) for email in ADMIN_EMAILS]
SERVER_EMAIL = config("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
SITE_URL = config("SITE_URL", default="http://localhost:8000").rstrip("/")
SITE_OG_IMAGE = config("SITE_OG_IMAGE", default="")
SITE_SEO_ENABLED = config("SITE_SEO_ENABLED", default=False, cast=bool)

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

MIDDLEWARE += ["apps.dashboard.middleware.DashboardCompanyMiddleware"]


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
                'apps.site_seo.context_processors.seo_settings',
                

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
