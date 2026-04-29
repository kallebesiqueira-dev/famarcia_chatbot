"""
Django settings for Farmacia Chatbot project.
Configurazione professionale con supporto per sviluppo e produzione.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev-key-change-in-production-farmacia-2024'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'corsheaders',
    # Local apps
    'chatbot.apps.ChatbotConfig',
    'pharmacy.apps.PharmacyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',       # CORS - prima di CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# Database - SQLite per sviluppo, PostgreSQL per produzione
# ---------------------------------------------------------------------------
if os.getenv('DATABASE_URL'):
    # Produzione: PostgreSQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    # Sviluppo: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Aperto per sviluppo
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Solo in sviluppo
    ],
}

# ---------------------------------------------------------------------------
# CORS - Consenti frontend React in sviluppo
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------------------------
# WhatsApp Configuration
# ---------------------------------------------------------------------------
WHATSAPP_DEFAULT_NUMBER = os.getenv('WHATSAPP_NUMBER', '393331234567')

# ---------------------------------------------------------------------------
# AI Configuration (predisposto per integrazione futura)
# ---------------------------------------------------------------------------
AI_PROVIDER = os.getenv('AI_PROVIDER', 'mock')  # 'mock', 'openai', 'anthropic'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4')
AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '500'))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'chatbot': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'pharmacy': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
