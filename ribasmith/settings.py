"""
Django settings for ribasmith project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import pymysql as php
php.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d!@_iqve!bw^fdd5i8jl%e4@$3@djpz)@i%%yh$lou22i-9=#+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'compressor',
    'store', #app wev
    'category',
    'Cart',
    'Departamento',
    'Grupo',
    'Account',
]
TE_URL = 'node_modules/'
STATICFILES_DIRS = [
  BASE_DIR / "static",
  BASE_DIR.parent / "node_modules",
]
TAILWIND_APP_NAME="theme"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ribasmith.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Departamento.context_processors.menu_links',
                'Cart.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'ribasmith.wsgi.application'

AUTH_USER_MODEL='Account.Account'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
 'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fastdeli',
        'USER': 'root',  # El usuario por defecto de MySQL en XAMPP es "root".
        'PASSWORD': '',  # Deja la contraseña en blanco si no la configuraste.
        'HOST': '127.0.0.1',  # Utiliza la dirección IP en lugar de 'localhost'.
        'PORT': '3306',  # El puerto MySQL por defecto en XAMPP es 3306.
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'

# STATIC_ROOT=BASE_DIR /'static'
STATICFILES_DIRS=[
   BASE_DIR / 'static'
]

MEDIA_ROOT=BASE_DIR / 'media'

MEDIA_URL='/media/'

from django.contrib.messages import constants as messages

MESSAGE_TAGS={
    messages.ERROR:'danger'
}

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='jetveces@gmail.com'
EMAIL_HOST_PASSWORD='kcpghbionvunfmhj'
EMAIL_USE_TLS=True

EMAIL_USE_TLS=True

STATIC_ROOT = BASE_DIR / 'staticfiles'

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
GOOGLE_MAPS_API_KEY = 'AIzaSyCdjCuB5DCVSeqwvAbek3aEpWB2tFTnMRU'