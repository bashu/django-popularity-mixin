# -*- coding: utf-8 -*-

import importlib

from django.apps import AppConfig as DefaultAppConfig


class AppConfig(DefaultAppConfig):
    name = 'popularity'

    def ready(self):
        # Ensure everything below is only ever run once
        if getattr(AppConfig, 'has_run_ready', False):
            return
        AppConfig.has_run_ready = True

        importlib.import_module('popularity.receivers')
