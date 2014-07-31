from django.conf import settings

class Settings(object):
    def __init__(
            self, 
            auto = False, 
            sizes = [768, 800, 1024, 1093, 1152, 1280, 1360, 1400, 1440, 1536, 1600, 1680, 1920, 2048, 2560], 
            maximum = 2560, 
            minimum = 800, 
            step_size = 220,
            default = 1920,
            *args, 
            **kwargs
        ):

        try:
            self.default = settings.MEDIA_HELPER_DEFAULT
        except:
            sekf.default = default
        try:
            self.auto = settings.MEDIA_HELPER_AUTO_SIZES
        except AttributeError:
            self.auto = auto

        try:
            self.sizes = settings.MEDIA_HELPER_SIZES
        except AttributeError:
            self.sizes = sizes

        try:
            self.maximum = settings.MEDIA_HELPER_MAX
            self.minimum = settings.MEDIA_HELPER_MIN
            self.step_size = settings.MEDIA_HELPER_STEP_SIZE
         
        except AttributeError:
            self.maximum = maximum
            self.minimum = minimum
            self.step_size = step_size

        if self.maximum < self.minimum:
             self.maximum, self.minimum = minimum, maximum
        
        if self.step_size > self.maximum - self.minimum:
                print 'yo step size b 2 big. lol. y u so dum?!?'

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

        if widths == None:
            widths = self.get_sizes()
        try:
            widths = map(float, widths)
        except ValueError:
            print 'dem aint numbers. fix em.'
            raise

        
        return {str(int(round(i, 0))): i / self.maximum for i in widths}