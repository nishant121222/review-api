"""
Django settings for backend project.
"""
import os
from pathlib import Path
from datetime import timedelta
import pymysql
from dotenv import load_dotenv  # ✅ Import load_dotenv

pymysql.install_as_MySQLdb()
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Load environment variables from .env file
# -----------------------
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")  # ✅ Use .env value
DEBUG = True  # Change to False in production

# -----------------------
# Allowed Hosts
# -----------------------
ALLOWED_HOSTS = [
    '10.142.138.25',
    '10.142.138.5',
    '127.0.0.1',
    'localhost',
    '69.62.72.122',
    'miramata.tech',
    'www.miramata.tech',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",        # Angular dev server
    "http://127.0.0.1:4200",        # Localhost for dev
    "http://10.142.138.25:4200",    # Angular served on LAN (PC1)
    "http://10.142.138.5:4200",     # Angular served on LAN (PC2)
    "https://miramata.tech",        # Production
    "https://www.miramata.tech",
    "http://10.142.138.25:8000",    # API direct
    "http://10.142.138.5:8000", 
    "https://api.lemiroir.miramata.tech",
    "https://lemiroir.miramata.tech"   # ✅ removed `/user`
]



CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://miramata.tech",
    "http://localhost:4200",
    "http://10.142.138.25:4200",
    "http://10.142.138.5:4200",
    "https://api.lemiroir.miramata.tech",
    "https://lemiroir.miramata.tech/user"  # Remove trailing slash
]





# -----------------------
# Application definition
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',

    # Local apps
    'accounts',
    'reviews',
    'games',
    'whatsapp',
    'businesses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',   # must be just after SecurityMiddleware
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

WSGI_APPLICATION = 'backend.wsgi.application'

# -----------------------
# Database
# -----------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'review_user',      # Database name
        'USER': 'review_user',      # MySQL user
        'PASSWORD': 'Nishant@2002', # Password
        'HOST': '118.139.179.98',  # Server IP
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'connect_timeout': 30,
            'autocommit': True,
        },
        'CONN_MAX_AGE': 3600,
    }
}


# -----------------------
# Custom AdminUser
# -----------------------
AUTH_USER_MODEL = 'accounts.User'

# -----------------------
# REST Framework & JWT
# -----------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# -----------------------
# Password validation
# -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------
# Internationalization
# -----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------
# Static files
# -----------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# -----------------------
# CORS (if frontend uses different domain)
# -----------------------
CORS_ALLOW_ALL_ORIGINS = True  # For testing only. Use CORS_ALLOWED_ORIGINS in production.

# -----------------------
# Celery / Redis
# -----------------------
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# -----------------------
# Twilio WhatsApp
# -----------------------
TWILIO_ACCOUNT_SID = "AC633788f6bd76658fd83fef9989c93c45"
TWILIO_AUTH_TOKEN = "b5e542d925c68b5bf9006689357fe047"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# -----------------------
# Redis Cache & Session
# -----------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": 3600,
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": 3600,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"


