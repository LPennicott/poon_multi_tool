# _*_ coding: utf-8 _*_
from .base import *

import os
import dj_database_url
import django_heroku

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
    }
}

ALLOWED_HOSTS = ['*']

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

django_heroku.settings(locals())
