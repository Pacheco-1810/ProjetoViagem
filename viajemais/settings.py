import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# em produção, defina a variável de ambiente SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
<<<<<<< HEAD
    "rest_framework",
    "drf_spectacular",
=======
    'rest_framework',
    'drf_spectacular',
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "viajemais.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "viajemais.wsgi.application"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "pacotes"
LOGOUT_REDIRECT_URL = "index"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "ViajeMais API",
<<<<<<< HEAD
    "DESCRIPTION": "API para consulta de pacotes turísticos e reservas.",
    "VERSION": "1.0.0",
}

JAZZMIN_SETTINGS = {
    "site_title": "ViajeMais",
    "site_header": "ViajeMais",
    "site_brand": "ViajeMais",
    "site_logo": "imgs/logo.png.jpeg",
    "welcome_sign": "Painel administrativo do ViajeMais",
    "copyright": "ViajeMais Turismo",
    "search_model": ["core.Pacote", "core.Compra"],
    "topmenu_links": [
        {"name": "Início", "url": "index", "new_window": True},
        {"name": "Gestão", "url": "gestao_pacotes", "new_window": True},
        {"name": "API (Swagger)", "url": "api-docs", "new_window": True},
    ],
    "order_with_respect_to": ["core.Pacote", "core.Hotel", "core.Compra", "core.Orcamento", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Pacote": "fas fa-suitcase-rolling",
        "core.Hotel": "fas fa-hotel",
        "core.Compra": "fas fa-receipt",
        "core.Orcamento": "fas fa-envelope-open-text",
    },
    "related_modal_active": True,
    "changeform_format": "horizontal_tabs",
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-dark",
    "navbar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_fixed": True,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "sidebar_nav_child_indent": True,
    "actions_sticky_top": True,
}
=======
    "DESCRIPTION": "API para gerenciamento de pacotes turísticos e reservas.",
    "VERSION": "1.0.0",
}
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
