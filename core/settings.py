"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DOCKER = False

INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'social_django',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    "corsheaders",

    'channels',
    "debug_toolbar",
    'django_filters',
    'drf_yasg',
    'ordered_model',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'silk',

    'users.apps.UsersConfig',
    'cottages',
    'relations',
    'towns',
    'chats',
    'payments',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',

    "corsheaders.middleware.CorsMiddleware",
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(
                str(os.getenv('REDIS_HOST_DOCKER')) if DOCKER else str(os.getenv('REDIS_HOST')),
                str(os.getenv('REDIS_PORT'))
            )],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv('DATABASE_NAME')),
        'USER': str(os.getenv('DATABASE_USER')),
        'PASSWORD': str(os.getenv('DATABASE_PASSWORD')),
        'HOST': str(os.getenv('DATABASE_HOST_DOCKER')) if DOCKER else str(os.getenv('DATABASE_HOST')),
        'PORT': int(os.getenv('DATABASE_PORT')),
    } if DOCKER else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f"{str(os.getenv('ELASTIC_HOST_DOCKER' if DOCKER else 'ELASTIC_HOST'))}:"
                 f"{str(os.getenv('ELASTIC_PORT'))}",
        'http_auth': (str(os.getenv('ELASTIC_USER')), str(os.getenv('ELASTIC_PASSWORD'))),
        'verify_certs': False,
    },
}

# For localhost
CELERY_BROKER_URL = (f"{str(os.getenv('REDIS_HOST_DOCKER')) if DOCKER else str(os.getenv('REDIS_HOST'))}:"
                     f"{str(os.getenv('REDIS_PORT'))}")
CELERY_RESULT_BACKEND = (f"{str(os.getenv('REDIS_HOST_DOCKER')) if DOCKER else str(os.getenv('REDIS_HOST'))}:"
                         f"{str(os.getenv('REDIS_PORT'))}")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{str(os.getenv('REDIS_HOST_DOCKER')) if DOCKER else str(os.getenv('REDIS_HOST'))}:"
                    f"{str(os.getenv('REDIS_PORT'))}",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User settings

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.yandex.YandexOAuth2',
)

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

# Email
#
# EMAIL_HOST = 'sm12.hosting.reg.ru'
# SMTP_PORT = 587
# EMAIL_HOST_USER = 'admin@beiron.org'
# EMAIL_HOST_PASSWORD = ///
# EMAIL_USE_TLS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# OAuth

LOGIN_REDIRECT_URL = "http://127.0.0.1:8000/auth/get_tokens/"

SOCIAL_AUTH_VK_OAUTH2_KEY = str(os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY'))
SOCIAL_AUTH_VK_OAUTH2_SECRET = str(os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET'))
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', "first_name", "last_name"]
SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = str(os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_KEY'))
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = str(os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_SECRET'))
SOCIAL_AUTH_YANDEX_OAUTH2_REDIRECT_URI = str(os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_REDIRECT_URI'))

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'core.urls.api_info',
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

# YooMoney
YOOMONEY_SHOP_ID = str(os.getenv('YOOMONEY_SHOP_ID'))
YOOMONEY_SHOP_SECRET = str(os.getenv('YOOMONEY_SHOP_SECRET'))
