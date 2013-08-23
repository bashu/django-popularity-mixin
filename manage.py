# -*- coding: utf-8 -*-

import os

from django.core.management import execute_manager

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
    'django.contrib.contenttypes',

    'djcelery',
    'hitcount',
    'django_jenkins',
    'discover_runner',
    ] + PROJECT_APPS

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'test_templates'),
    ]

ROOT_URLCONF = 'test_urls'

SITE_ID = 1

## Hitcount settings

USE_HITCOUNT = True
HITCOUNT_KEEP_HIT_ACTIVE = { 'hours': 24 }
HITCOUNT_HITS_PER_IP_LIMIT = 0

## Celery settings

CELERY_ALWAYS_EAGER = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

TEST_RUNNER = 'discover_runner.DiscoverRunner'

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.dir_tests',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
    )

COVERAGE_EXCLUDES_FOLDERS = ['popularity/tests/*']
PYLINT_RCFILE = os.path.join(PROJECT_ROOT, 'pylint.rc')

if __name__ == "__main__":
    from django.conf import settings
    settings.configure(
        DATABASES = DATABASES,
        INSTALLED_APPS = INSTALLED_APPS,
        ROOT_URLCONF = ROOT_URLCONF,
        SITE_ID = SITE_ID,
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES,
        USE_HITCOUNT = USE_HITCOUNT,
        TEMPLATE_DIRS = TEMPLATE_DIRS,
        HITCOUNT_KEEP_HIT_ACTIVE = HITCOUNT_KEEP_HIT_ACTIVE,
        HITCOUNT_HITS_PER_IP_LIMIT = HITCOUNT_HITS_PER_IP_LIMIT,
        CELERY_ALWAYS_EAGER = CELERY_ALWAYS_EAGER,
        CELERYBEAT_SCHEDULER = CELERYBEAT_SCHEDULER,
        PROJECT_APPS = PROJECT_APPS,
        TEST_RUNNER = TEST_RUNNER,
        JENKINS_TASKS = JENKINS_TASKS,
        COVERAGE_EXCLUDES_FOLDERS = COVERAGE_EXCLUDES_FOLDERS,
        PYLINT_RCFILE = PYLINT_RCFILE,
        TEMPLATE_DEBUG = TEMPLATE_DEBUG
        )
    execute_manager(settings)
