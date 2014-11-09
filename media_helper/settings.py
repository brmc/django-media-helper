from django.conf import settings

default = getattr(settings, "MEDIA_HELPER_DEFAULT", .5)
quality = getattr(settings, "MEDIA_HELPER_QUALITY", 50)
auto = getattr(settings, "MEDIA_HELPER_AUTO", True)
minimum = getattr(settings, "MEDIA_HELPER_MIN", 20)
round_to = getattr(settings, "MEDIA_HELPER_ROUND_TO", 10)

default_folder = getattr(
    settings,
    "MEDIA_HELPER_DEFAULT_FOLDER",
    'media-helper')

allowed_encodings = getattr(
    settings,
    "MEDIA_HELPER_ALLOWED_ENCODINGS",
    ['jpg', 'jpeg', 'png'])

sizes = getattr(settings, "MEDIA_HELPER_SIZES", [
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
