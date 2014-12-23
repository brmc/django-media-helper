#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

DEFAULT = getattr(settings, "MEDIA_HELPER_DEFAULT", .1)  # % of original size
QUALITY = getattr(settings, "MEDIA_HELPER_QUALITY", 50)  # Pillow quality kwarg
AUTO = getattr(settings, "MEDIA_HELPER_AUTO", True)      # Re-size on save
MINIMUM = getattr(settings, "MEDIA_HELPER_MIN", 20)      # Smallest image
ROUND_TO = getattr(settings, "MEDIA_HELPER_ROUND_TO", 10)  # nearest pixel
GENERATE_STATIC = getattr(settings, "MEDIA_HELPER_GENERATE_STATIC", True)
STATIC_SIZE = getattr(settings, "MEDIA_HELPER_STATIC_SIZE", 1366)
STATIC_NAME = getattr(settings, "MEDIA_HELPER_STATIC_NAME", 'static')

# jQuery selectors for img elements
IMAGE_SELECTORS = getattr(settings, "MEDIA_HELPER_IMAGE_SELECTORS", "img")
# jQuery selectors for elements with background-images
BACKGROUND_SELECTORS = getattr(
    settings,
    "MEDIA_HELPER_BACKGROUND_SELECTORS",
    "div")

# currently not  being used
IMAGE_EXCLUDES = getattr(settings, "MEDIA_HELPER_IMAGE_EXCLUDES", None)

DEFAULT_FOLDER = getattr(         # where images will be saved under MEDIA_ROOT
    settings,
    "MEDIA_HELPER_DEFAULT_FOLDER",
    'media-helper')

ALLOWED_ENCODINGS = getattr(      # filetypes of images to be resized
    settings,
    "MEDIA_HELPER_ALLOWED_ENCODINGS",
    ['jpg', 'jpeg', 'png'])

# Sizes to be used when an image is saved.  % of original size
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
