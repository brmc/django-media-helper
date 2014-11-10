#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

DEFAULT = getattr(settings, "MEDIA_HELPER_DEFAULT", .5)
QUALITY = getattr(settings, "MEDIA_HELPER_QUALITY", 50)
AUTO = getattr(settings, "MEDIA_HELPER_AUTO", True)
MINIMUM = getattr(settings, "MEDIA_HELPER_MIN", 20)
ROUND_TO = getattr(settings, "MEDIA_HELPER_ROUND_TO", 10)
IMAGE_SELECTORS = getattr(settings, "MEDIA_HELPER_IMAGE_SELECTORS", "img")
BACKGROUND_SELECTORS = getattr(
    settings,
    "MEDIA_HELPER_BACKGROUND_SELECTORS",
    "div")

IMAGE_EXCLUDES = getattr(settings, "MEDIA_HELPER_IMAGE_EXCLUDES", None)

DEFAULT_FOLDER = getattr(
    settings,
    "MEDIA_HELPER_DEFAULT_FOLDER",
    'media-helper')

ALLOWED_ENCODINGS = getattr(
    settings,
    "MEDIA_HELPER_ALLOWED_ENCODINGS",
    ['jpg', 'jpeg', 'png'])

SIZES = getattr(settings, "MEDIA_HELPER_SIZES", [
    0.3,
    0.3125,
    0.4,
    0.426953125,
    0.45,
    0.5,
    0.53125,
    0.546875,
    0.5625,
    0.6,
    0.625,
    0.65625,
    0.75,
    0.8,
    1.0
])
