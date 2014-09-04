from django.conf import settings

#sizes = [768, 800, 1024, 1093, 1152, 1280, 1360, 1400, 1440, 1536, 1600, 1680, 1920, 2048, 2560], 
            
class Settings(object):
    def __init__(
            self,
            auto = True, 
            sizes = [0.3, 0.3125, 0.4, 0.426953125, 0.45, 0.5, 0.53125, 0.546875, 0.5625, 0.6, 0.625, 0.65625, 0.75, 0.8, 1.0],
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
            self.default_folder = settings.MEDIA_HELPER_DEFAULT_FOLDER
            self.quality = settings.MEDIA_HELPER_QUALITY
        except:
            self.default = default
            self.default_folder = default_folder
            self.quality = quality
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

        
'''
    def get_sizes(self, *args, **kwargs):
        """ Returns user defined sizes or an automatically generated list

        Arguments:
        :returns: list of ints
        """
        
        if self.auto:
            return range(self.minimum, self.maximum + 1, self.step_size)
        else:
            return self.sizes

    def generate_scaling_factors(self, widths = None):
        """ Returns a dict of screen widths with their scaling factors

        Takes the maximum screen width defined in the settings, and for 
        each screen widths, calculates its percentage in relation to 
        the maximum allowed width. 

        Arguments:

        :param widths: screen widths
        :type widths: list of ints or strings
        :returns: dict
        """
        import warnings

        warnings.warn("This is deprecated.  

            ")
        if widths == None:
            widths = self.get_sizes()
        try:
            widths = map(float, widths)
        except ValueError:
            print 'dem aint numbers. fix em.'
            raise

        
        return {str(int(round(i, 0))): i / self.maximum for i in widths}
'''