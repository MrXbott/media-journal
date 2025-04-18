"""
Django settings for mediajournal project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import mimetypes
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("text/css", ".css", True)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-q5o+s6^hi9qqah13c35kv3zo8$lei*#3+krl)c-0$6z8g9%w3c')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = [ '127.0.0.1',
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]


AUTH_USER_MODEL = 'accounts.Staff'

AUTHENTICATION_BACKENDS = [ 
    'accounts.auth.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend', 
    
]

# Application definition

INSTALLED_APPS = [
    'web.apps.WebConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'articles.apps.ArticlesConfig',
    'news.apps.NewsConfig',
    'comments.apps.CommentsConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'debug_toolbar',
    'django_celery_beat',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mediajournal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'mediajournal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'NAME': os.environ.get('POSTGRES_NAME', 'mediajournal'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'PORT': int(os.environ.get('POSTGRES_PORT', '5432')),
    } 
}


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379) 
REDIS_DB = os.environ.get('REDIS_DB', 0) 
REDIS_USERNAME = os.environ.get('REDIS_USERNAME', '')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/')


CELERY_BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('RESULT_BACKEND', 'redis://localhost:6379')


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

FORMAT_MODULE_PATH = ['mediajournal.formats',]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = 'staticfiles/'
STATICFILES_DIRS = []

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_REDIRECT_URL = 'main_page' 
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'



# Email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'    # uncomment to use terminal
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST')                    
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')          
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  
# EMAIL_PORT = os.environ.get('EMAIL_PORT')                   
# EMAIL_USE_TLS = str(os.environ.get('EMAIL_USE_TLS')).lower() == 'true'
# EMAIL_USE_SSL = str(os.environ.get('EMAIL_USE_SSL')).lower() == 'true'


# Email subjects etc.
CONFIRM_EMAIL_SUBJECT = os.environ.get('CONFIRM_EMAIL_SUBJECT', 'Подтвердите ваш емейл')
WEEKLY_NEWSLETTER_SUBJECT = os.environ.get('WEEKLY_NEWSLETTER_SUBJECT', 'Новые статьи за неделю')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
DOMAIN_URL = os.environ.get('DOMAIN_URL', 'https://example.com')