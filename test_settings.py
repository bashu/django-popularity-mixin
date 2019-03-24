# -*- coding: utf-8 -*-

import os, sys

import djcelery
djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

PROJECT_APPS = [
    'popularity',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'hitcount',
    'cacheback',
] + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

MIDDLEWARE_CLASSES = MIDDLEWARE

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'test_templates'),
        ],
        'APP_DIRS': True,
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

ROOT_URLCONF = 'test_urls'

SITE_ID = 1


## Hitcount settings

USE_HITCOUNT = True
HITCOUNT_KEEP_HIT_ACTIVE = { 'hours': 24 }
HITCOUNT_HITS_PER_IP_LIMIT = 0


## Cacheback settings

CACHEBACK_TASK_QUEUE = 'celery'


## Celery settings

CELERY_ALWAYS_EAGER = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
