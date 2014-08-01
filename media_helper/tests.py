#from pillow import Image

from django.test import TestCase
from django.conf import settings
#from football.models import Test

class ResizerTest(TestCase):
    scaling_factors = {
            '2': 0.1,
            '10': 0.5,
            '20': 1.0
        }
    sizes = [2, 10, 20]

    def test_get_sizes(self):
        from media_helper.settings import Settings
        
        settings.MEDIA_HELPER_SIZES =[2, 10, 20]
        
        sizes = Settings().get_sizes()

        self.assertEqual(sizes, self.sizes)

    def test_get_scaling_factors(self):
        from media_helper.settings import Settings
        
        scaling_factors = Settings(maximum = 200, sizes = self.sizes).generate_scaling_factors(widths = self.sizes)
        scaling_factors
        self.assertEqual(scaling_factors, self.scaling_factors)

    def test_find_models_with_imagefield(self):
        from django_cleanup.resizer import find_models_with_imagefield
        from django_cleanup.models import TestModel
        
        m = [TestModel,]
        n = find_models_with_imagefield()

        self.assertEqual(m,n)

    def test_create_directories(self):
        import os
        import shutil
        from django.conf import settings
        from resizer import create_directories
        create_directories(self.sizes, settings.MEDIA_ROOT, "pathname")

        for size in self.sizes.iterkeys():
            path = os.path.join(settings.MEDIA_ROOT, size, "pathname")
            self.assertTrue(os.path.isdir(path))
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, size))

    def test_detault_settings(self):
        import settings
        
        self.assertFalse(settings.MEDIA_HELPER_AUTO_SIZES)
        self.assertEqual(
            settings.MEDIA_HELPER_SIZES, 
            [2560, 1920, 1366, 1280, 1024, 800]
        )

        self.assertEqual(settings.MEDIA_HELPER_MAX, 2560)
        self.assertEqual(settings.MEDIA_HELPER_MIN, 800)
        self.assertEqual(settings.MEDIA_HELPER_STEP_SIZE, 320)
