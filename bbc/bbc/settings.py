"""
Django settings for bbc project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import smtplib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6*23oj2o%)6s650*r)xw$ofe(tqv#!oeyui=c1z$1wf+$)d-1b'

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
    'phonenumber_field',
    'rest_framework',
    'corsheaders',  # cors
    'func',
    'member',
    'booking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # csrf
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    # test
    # 'func.disable.DisableCSRF',
]


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'rest_framework.authentication.TokenAuthentication',
#         # 'rest_framework.authentication.SessionAuthentication',
#         # 'rest_framework.authentication.BasicAuthentication',
#     ]
# }

ROOT_URLCONF = 'bbc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['template'],
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

WSGI_APPLICATION = 'bbc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'HOST': '',
        'USER': 'root',
        'PASSWORD': '',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME' : 'ite60010062_dbname',
#         'HOST' : '172.18.0.4',
#         'USER' : 'ite60010062_user',
#         'PASSWORD' : '',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ite60010062_dbname',
#         'USER': 'ite60010062_user',
#         'PASSWORD': '123456',
#         'HOST': '172.18.0.4',
#         'PORT': '22',
#     }
# }

# DATABASES = {
#     'default': {
#             'ENGINE': 'djongo',
#             'NAME': 'bbc_db',
#             'CLIENT': {
#                 'host': 'mongodb+srv://myproject1:myproject1@cluster0.zo39s.gcp.mongodb.net/test?retryWrites=true&w=majority'
#             },
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1:3000',
#     'http://localhost:3000',
# )


CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:3000'
]

# CORS_ORIGIN_REGEX_WHITELIST = [
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
# ]

CORS_ALLOW_CREDENTIALS = True

# SESSION_COOKIE_SAMESITE = 'Strict'  # 'Lax'

#SESSION_COOKIE_DOMAIN = ['http://127.0.0.1:3000', 'http://localhost:3000']

#SESSION_COOKIE_DOMAIN = 'http://localhost:8000'

# SESSION_COOKIE_SAMESITE = None
# CSRF_COOKIE_SAMESITE = None
# CSRF_TRUSTED_ORIGINS = ['127.0.0.1:3000']
CSRF_COOKIE_SECURE = True


# DataFlair
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bbctesting01'
EMAIL_HOST_PASSWORD = 'bbc*6263'
