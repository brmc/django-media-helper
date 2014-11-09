# coding: utf-8
import django
if django.VERSION >= (1, 7):

    from django.apps import AppConfig
    from .tools.cleanup import connect_signals
    from .tools.resizers import resize_signals

    class MediaHelperConfig(AppConfig):
        name = 'media_helper'

        def ready(self):
            connect_signals()
            resize_signals()
