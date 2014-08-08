# coding: utf-8
import django
if django.VERSION >= (1, 7):

    from django.apps import AppConfig
    from .models import connect_signals
    from .resizer import resize_signals

    class CleanupConfig(AppConfig):
        name = 'media_helper'

        def ready(self):
            connect_signals()
            resize_signals()
            