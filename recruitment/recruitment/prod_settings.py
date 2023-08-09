from .settings import *
import urllib
import os

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'channels',
    'whitenoise.runserver_nostatic',
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

hostname = os.environ['DBHOST']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'USER': os.environ['DBUSER'] + "@" + hostname,
        'PASSWORD': os.environ['DBPASS'] ,
        'HOST': hostname + ".postgres.database.azure.com",
        'PORT': "5432",  # 5432 by default
    }
}

CELERY_BROKER_URL = f"sqla+postgresql://{str(DATABASES['default']['USER'])}:{urllib.parse.quote(str(DATABASES['default']['PASSWORD']), safe='')}@{str(DATABASES['default']['HOST'])}:{str(DATABASES['default']['PORT'])}/{str(DATABASES['default']['NAME'])}"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

