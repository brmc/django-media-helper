#!/usr/bin/env python
# -*- coding: utf-8 -*-
from media_helper import settings


def include_settings(request):

    encodings = settings.ALLOWED_ENCODINGS
    img_selectors = settings.IMAGE_SELECTORS.split(",")
    bkg_selectors = settings.BACKGROUND_SELECTORS
    i_selectors = []

    for encoding in encodings:
        for selector in img_selectors:
            i_selectors.append("{0}[src$='.{1}']".format(selector, encoding.decode('utf8')))


    return {
        'media_helper': settings,
        'selectors': ", ".join(i_selectors)
    }
