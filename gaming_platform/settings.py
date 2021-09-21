"""
Django settings for gaming_platform project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

import dj_database_url
import django_heroku


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3dm+(x4-rthm^q6@=^z5tu_t@-&9cnkp=jl+9t9c-rs=pi=m4&'
SOCIAL_SECRET = 'fz#uwn3pffmphqgua(d4sj2thhp*%l!m5(wy3e7=jxw84b1285'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',

    'fcm_django',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_yasg',
    'corsheaders',

    #####apps#####
    'accounts',
    'cashbox',
    'main'
]

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAef__KYI:APA91bH0DP1oGdH5lNjFEQXIq3K4BqNlY5mMKd8gLsrpJRhT69hTPeOJR-_nvgWSxhNCE0IjwXSAt1NrfBLOjh4pACyk9VpmIpEf1l6KczQmyFRcL4xtjEm3jDjXLQaurBvVBWXOoG6H"
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gaming_platform.urls'

CORS_ORIGIN_ALLOW_ALL = True

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

WSGI_APPLICATION = 'gaming_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT')
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd7sij1d6jsn21i',
        'USER': 'zvjokdjkouavjl',
        'PASSWORD': 'c6d17f2c9ced63942dda83478b4876181a8b73405de0bf86765a959ed3d2a85e',
        'HOST': 'ec2-54-73-152-36.eu-west-1.compute.amazonaws.com',
        'PORT': '5432'
    }
}

# NIKITA_LOGIN = 


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

AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'gaming_platform/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=12),

    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=24),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=14),
}

EMAIL_FROM = 'some.email634@gmail.com'
EMAIL_BCC = 'Qualle'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'some.email634@gmail.com'
EMAIL_HOST_PASSWORD = 'some_password'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SERVER_EMAIL = 'some.email634@gmail.com'
