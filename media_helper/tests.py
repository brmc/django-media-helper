#from pillow import Image

from django.test import TestCase
from django.conf import settings
from django.db import models
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
        
        scaling_factors = Settings(maximum = 20, minimum = 1, sizes = self.sizes).generate_scaling_factors(widths = self.sizes)
        scaling_factors
        self.assertEqual(scaling_factors, self.scaling_factors)

    def test_find_models_with_field(self):
        from media_helper.resizer import find_models_with_field
        from media_helper.models import TestModel
        
        m = [TestModel,]
        n = find_models_with_field(models.ImageField)

        self.assertEqual(m,n)

    def test_find_field_attribute(self):
        from media_helper.models import TestModel
        from media_helper.resizer import find_field_attribute
        
        self.assertTrue(["image"], find_field_attribute("name", TestModel))

    def test_resize(self):
        import media_helper
        import os
        from PIL import Image
        
        media_root = os.path.join(media_helper.__path__[0], "test-files/")

        settings.MEDIA_URL = '/test-files/'
        
        image_path = os.path.join(media_root, "upload/image.png")
        media_helper.resizer.resize(media_root, "path", .75, image_path)
        image = Image.open(os.path.join(media_root, "path/upload/image.png"))
        self.assertEqual((40, 40), image.size)
        os.remove(os.path.join(media_root, "path/upload/image.png"))
        
        image_path = os.path.join(media_root, "upload/image.txt")
        media_helper.resizer.resize(media_root, "path", .75, image_path)
        self.assertFalse(os.path.isfile(os.path.join(media_root, "path/upload/image.txt")))
    
    def test_resize_on_save(self):
        import os
        
        from django.core.files import File
        from django.db.models.signals import post_save
        
        import media_helper 
        from .settings import Settings
        from media_helper.resizer import resize_on_save
        from media_helper.models import TestModel
        

        settings.MEDIA_ROOT = os.path.join(media_helper.__path__[0], "test-files/")
        settings.MEDIA_URL = '/test-files/'
        #settings.MEDIA_HELPER_SIZES = [200, 300]
        #settings.MEDIA_HELPER_AUTO = False
        #settings.MEDIA_HELPER_STEP_SIZE = [100]


        image_path = os.path.join(settings.MEDIA_ROOT, "upload/image.png")
        #image = Image.open(os.path.join(settings.MEDIA_ROOT, "path/upload/image.png"))
        image = open(image_path)

        test = TestModel()
        #post_save.connect(resize_on_save, sender = TestModel)
        
        test.image.save(image_path, File(image))
        test.save()
        post_save.send(instance = test)
        

        self.assertTrue(True)

    def test_create_directories(self):
        import os
        import shutil
        from django.conf import settings
        from .resizer import create_directories
        create_directories(settings.MEDIA_ROOT, self.scaling_factors, "pathname")

        for size in self.scaling_factors.iterkeys():
            path = os.path.join(settings.MEDIA_ROOT, size, "pathname")
            self.assertTrue(os.path.isdir(path))
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, size))

    def test_default_settings(self):
        from settings import Settings
        
        
        settings = Settings()
        self.assertFalse(settings.auto)
        self.assertEqual(
            settings.sizes, 
            [768, 800, 1024, 1093, 1152, 1280, 1360, 1400, 1440, 1536, 1600, 1680, 1920, 2048, 2560]
        )

        self.assertEqual(settings.maximum, 2560)
        self.assertEqual(settings.minimum, 800)
        self.assertEqual(settings.step_size, 220)
        self.assertEqual(settings.default, 1920)
        self.assertEqual(settings.allowed_encodings, ['jpg', 'jpeg', 'png'])

