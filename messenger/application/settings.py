"""
Django settings for messenger project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import json, os
from django.core.exceptions import ImproperlyConfigured

# JSON-based secrets module
with open('secrets.json') as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['reatlaz.pythonanywhere.com']

# CSRF_USE_SESSIONS = True
CSRF_TRUSTED_ORIGINS = [
    'https://reatlaz.pythonanywhere.com',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://reatlaz.github.io'
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://reatlaz.github.io',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000'
]


CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'

CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

LOGIN_URL = 'http://localhost:3000/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/login/'
LOGIN_REDIRECT_URL = 'http://localhost:3000/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/login/success/'
LOGOUT_URL = 'http://localhost:3000/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/'
LOGOUT_REDIRECT_URL = 'http://localhost:3000/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/login/'

# LOGIN_URL = 'https://reatlaz.github.io/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/login/'
# LOGIN_REDIRECT_URL = 'https://reatlaz.github.io/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/login/success/'
# LOGOUT_URL = 'https://reatlaz.github.io/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/'
# LOGOUT_REDIRECT_URL = 'https://reatlaz.github.io/2022-2-VK-EDU-FS-Frontend-R-AFIATULLOV#/login/'

CORS_ALLOW_HEADERS = [
    'Access-Control-Allow-Origin',
    'Content-Type',
    'Access-Control-Allow-Credentials',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'cookie',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ]
# }
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'social_django',
    'rest_framework',
    'users',
    'chats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'login_required.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_REQUIRED_IGNORE_PATHS = [
    r'/social-auth/login/google-oauth2/',
    r'/social-auth/complete/google-oauth2/$',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.linkedin.LinkedinOAuth2',
    # 'social_core.backends.instagram.InstagramOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# CELERY_IMPORTS = ("application.tasks", )

# sending emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
# administrator list
ADMINS = ["m3sseng3r@yandex.ru"]


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_secret('GOOGLE_OAUTH2_KEY')  # App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_secret('GOOGLE_OAUTH2_SECRET')  # App Secret
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('DATABASES_NAME'),
        'USER': get_secret('DATABASES_USER'),
        'PASSWORD': get_secret('DATABASES_PASSWORD'),
        'HOST': get_secret('DATABASES_HOST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

""" try:
    from .local_settings import *
except ImportError:
    pass """
