#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from media_helper import settings


def include_settings(request):

    encodings = settings.ALLOWED_ENCODINGS
    img_selectors = settings.IMAGE_SELECTORS.split(",")

    i_selectors = []

    for encoding in encodings:

        for selector in img_selectors:
            i_selectors.append("{0}[src$='.{1}']".format(selector, encoding))

    return {
        'media_helper': settings,
        'SELECTORS': ", ".join(i_selectors),
        'encodings': "|".join(encodings)
    }
