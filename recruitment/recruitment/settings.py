"""
Django settings for recruitment project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import  urllib

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2rs$xqpskq7=shem)go3)6s=c=ubl1qj622zz7-5@x%_#eu-ng'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'channels',
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'django_eventstream',
    'django_celery_results',
    'rest_framework.authtoken',
    'session_security',
]

MEDIA_ROOT=os.path.join(BASE_DIR,'submission_files')

MEDIA_URL='/submission_files/'

DATA_UPLOAD_MAX_NUMBER_FILES=None

AUTH_USER_MODEL = 'main.Users'

LOGIN_URL = '/login'

LOGIN_REDIRECT_URL = '/browse'

MIDDLEWARE = [
    'django_grip.GripMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'recruitment.urls'

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
                'main.context_processors.sidebar',
            ],
        },
    },
]

WSGI_APPLICATION = 'recruitment.wsgi.application'
ASGI_APPLICATION = 'recruitment.asgi.application'

EVENTSTREAM_STORAGE_CLASS = 'django_eventstream.storage.DjangoModelStorage'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "dsats_db",
        'USER': "dsats_user@ptsg-5dsppsql01",
        'PASSWORD': "ds_dsats@2023",
        'HOST': "ptsg-5dsppsql01.postgres.database.azure.com",
        'PORT': "5432",  # 5432 by default
    }
}

# Celery settings
CELERY_BROKER_URL = f"sqla+postgresql://{str(DATABASES['default']['USER'])}:{urllib.parse.quote(str(DATABASES['default']['PASSWORD']), safe='')}@{str(DATABASES['default']['HOST'])}:{str(DATABASES['default']['PORT'])}/{str(DATABASES['default']['NAME'])}"
# CELERY_RESULT_BACKEND = 'db+sqlite:///' + str(DATABASES['default']['NAME'])
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True

# Session security
SESSION_SECURITY_INSECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER = 600
SESSION_SECURITY_EXPIRE_AFTER = 630


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

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
