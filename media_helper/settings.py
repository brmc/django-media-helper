from django.conf import settings


class Settings(object):
    def __init__(
            self,
            auto = True,
            sizes = [
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
            ],
            default = .5,
            quality = 50,
            minimum = 800,
            default_folder = 'media-helper',
            allowed_encodings = ['jpg', 'jpeg', 'png'],
            round_to = 10,
            *args,
            **kwargs
        ):

        try:
            self.default = settings.MEDIA_HELPER_DEFAULT
        except:
            self.default = default

        try:
            self.quality = settings.MEDIA_HELPER_QUALITY
        except:
            self.quality = quality

        try:
            self.default_folder = settings.MEDIA_HELPER_DEFAULT_FOLDER
        except:
            self.default_folder = default_folder
        try:
            self.auto = settings.MEDIA_HELPER_AUTO
        except AttributeError:
            self.auto = auto

        try:
            self.sizes = settings.MEDIA_HELPER_SIZES
        except AttributeError:
            self.sizes = sizes

        try:
            self.minimum = settings.MEDIA_HELPER_MIN

        except AttributeError:
            self.minimum = minimum

        try:
            self.allowed_encodings = settings.MEDIA_HELPER_ALLOWED_ENCODINGS
        except AttributeError:
            self.allowed_encodings = allowed_encodings

        try:
            self.round_to = settings.MEDIA_HELPER_ROUND_TO
        except AttributeError:
            self.round_to = round_to
