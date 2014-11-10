#!/usr/bin/env python
# -*- coding: utf-8 -*-
from media_helper import settings


def include_settings(request):
    return {
        'media_helper': settings
    }
