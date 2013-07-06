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

PROJECT_APPS = [
    'popularity',
    ]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',

    'djcelery',
    'hitcount',
    'django_jenkins',
    ] + PROJECT_APPS

ROOT_URLCONF = 'test_urls'

## Hitcount settings

USE_HITCOUNT = True
HITCOUNT_KEEP_HIT_ACTIVE = { 'hours': 24 }
HITCOUNT_HITS_PER_IP_LIMIT = 0

## Celery settings

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    )

COVERAGE_EXCLUDES_FOLDERS = ['popularity/tests/*']
PYLINT_RCFILE = os.path.join(PROJECT_ROOT, 'pylint.rc')

if __name__ == "__main__":
    from django.conf import settings
    settings.configure(
        DATABASES = DATABASES,
        INSTALLED_APPS = INSTALLED_APPS,
        ROOT_URLCONF = ROOT_URLCONF,
        USE_HITCOUNT = USE_HITCOUNT,
        HITCOUNT_KEEP_HIT_ACTIVE = HITCOUNT_KEEP_HIT_ACTIVE,
        HITCOUNT_HITS_PER_IP_LIMIT = HITCOUNT_HITS_PER_IP_LIMIT,
        CELERYBEAT_SCHEDULER = CELERYBEAT_SCHEDULER,
        PROJECT_APPS = PROJECT_APPS,
        JENKINS_TASKS = JENKINS_TASKS,
        COVERAGE_EXCLUDES_FOLDERS = COVERAGE_EXCLUDES_FOLDERS,
        PYLINT_RCFILE = PYLINT_RCFILE,
        TEMPLATE_DEBUG = TEMPLATE_DEBUG
        )
    execute_manager(settings)
