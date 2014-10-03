# -*- coding: utf-8 -*-

import os, sys

from django.core.management import ManagementUtility

import djcelery
djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
        }
    }

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]

PROJECT_APPS = [
    'popularity',
    ]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.contenttypes',

    'hitcount',
    'django_jenkins',
    'djcelery',
    ] + PROJECT_APPS

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'test_templates'),
    ]

SITE_ID = 1

## Hitcount settings

USE_HITCOUNT = True
HITCOUNT_KEEP_HIT_ACTIVE = { 'hours': 24 }
HITCOUNT_HITS_PER_IP_LIMIT = 0

## Celery settings

CELERY_ALWAYS_EAGER = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

JENKINS_TASKS = (
    'django_jenkins.tasks.run_flake8',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    )

COVERAGE_EXCLUDES_FOLDERS = ['popularity/tests/*']
PYLINT_RCFILE = os.path.join(PROJECT_ROOT, 'pylint.rc')

if __name__ == "__main__":
    from django.conf import settings
    settings.configure(
        DATABASES = DATABASES,
        INSTALLED_APPS = INSTALLED_APPS,
        SITE_ID = SITE_ID,
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES,
        USE_HITCOUNT = USE_HITCOUNT,
        TEMPLATE_DIRS = TEMPLATE_DIRS,
        HITCOUNT_KEEP_HIT_ACTIVE = HITCOUNT_KEEP_HIT_ACTIVE,
        HITCOUNT_HITS_PER_IP_LIMIT = HITCOUNT_HITS_PER_IP_LIMIT,
        CELERY_ALWAYS_EAGER = CELERY_ALWAYS_EAGER,
        CELERYBEAT_SCHEDULER = CELERYBEAT_SCHEDULER,
        PROJECT_APPS = PROJECT_APPS,
        JENKINS_TASKS = JENKINS_TASKS,
        COVERAGE_EXCLUDES_FOLDERS = COVERAGE_EXCLUDES_FOLDERS,
        PYLINT_RCFILE = PYLINT_RCFILE,
        TEMPLATE_DEBUG = TEMPLATE_DEBUG
        )
    utility = ManagementUtility(sys.argv)
    utility.execute()
