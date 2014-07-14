#from pillow import Image

from django.test import TestCase

#from football.models import Test

class ResizerTest(TestCase):
    sizes = {
            '2': 0.1,
            '10': 0.5,
            '20': 1.0
        }

    def test_get_sizes(self):
        from django_cleanup.resizer import get_sizes

        settings.MEDIA_HELPER_SIZES =[2, 10, 20]
        
        sizes = get_sizes()

        self.assertEqual(sizes, self.sizes)

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
