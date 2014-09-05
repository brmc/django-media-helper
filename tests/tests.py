#from pillow import Image

from django.test import TestCase
from django.conf import settings
from django.db import models
from media_helper.models import TestModel
from media_helper.tools.resizers import resize
from media_helper.settings import Settings
#from football.models import Test

class ResizersTest(TestCase):
    scaling_factors = {
            '2': 0.1,
            '10': 0.5,
            '20': 1.0
        }
    sizes = [2, 10, 20]
    image_path = "upload/image.jpg"

    def test_resize(self):
        import media_helper
        import os
        from PIL import Image
        from media_helper.tools.helpers import construct_paths
        
        settings.MEDIA_URL = '/test-files/'
        
        root = settings.MEDIA_ROOT = os.path.join(os.getcwd(), 'test-files')

        new_image_path = os.path.join(root, 'media-helper/upload/image.jpg/30.jpeg"',)
        image_path = os.path.join(root, "upload/image.jpg")
        paths = construct_paths(image_path)

        self.assertTrue(resize(image_path, 30))
        resized = os.path.join(paths['response_system_path'], '30.jpeg')
        
        self.assertTrue(os.path.isfile(resized))

        import shutil
        shutil.copy(paths['backup_path'], image_path)
        shutil.rmtree(paths['media_helper_root'])
    
    def test_move_original(self):
        import os
        from media_helper.tools.resizers import move_original
        settings.MEDIA_URL = '/test-files/'

        root = settings.MEDIA_ROOT = os.path.join(os.getcwd(), 'test-files')
        image_path = os.path.join(root, "upload/image.jpg")
        self.assertTrue(isinstance(move_original(image_path), str))


    def test_default_settings(self):
        from media_helper.settings import Settings
        
        settings = Settings()
        self.assertTrue(settings.auto)
        self.assertEqual(
            settings.sizes, 
            [0.3, 0.3125, 0.4, 0.426953125, 0.45, 0.5, 0.53125, 0.546875, 0.5625, 0.6, 0.625, 0.65625, 0.75, 0.8, 1.0]
        )

        self.assertEqual(settings.minimum, 800)
        self.assertEqual(settings.default, .5)
        self.assertEqual(settings.quality, 50)
        self.assertEqual(settings.allowed_encodings, ['jpg', 'jpeg', 'png'])



class HelpersTest(TestCase):
    def test_construct_paths(self):
        import os.path
        from media_helper.tools.helpers import construct_paths
        settings.MEDIA_URL = '/test-files/'
        settings.MEDIA_ROOT = '/junky-butter/peanuts/'

        paths = construct_paths("doo/1.jpg")

        self.assertEqual(paths['image_name'], 'doo/1.jpg')
        self.assertEqual(paths['request_path'], '/test-files/doo/1.jpg')
        self.assertEqual(paths['request_system_path'], '/junky-butter/peanuts/doo/1.jpg')
        self.assertEqual(paths['response_path'], '/test-files/media-helper/doo/1.jpg')
        self.assertEqual(paths['media_helper_root'], '/junky-butter/peanuts/media-helper')
        self.assertEqual(paths['backup_path'], '/junky-butter/peanuts/media-helper/doo/1.jpg/original.jpeg')
        self.assertEqual(paths['backup_response_path'], '/test-files/media-helper/doo/1.jpg/original.jpeg')
        self.assertEqual(paths['response_system_path'], '/junky-butter/peanuts/media-helper/doo/1.jpg')


    def test_check_encoding(self):
        from media_helper.tools.helpers import check_encoding
        
        self.assertEqual("jpeg", check_encoding('.jpg'))
        self.assertEqual('png', check_encoding('.png'))
        self.assertFalse(check_encoding(".joop"))

    def test_create_directories(self):
        import os
        import shutil
        from django.conf import settings
        from media_helper.tools.helpers import create_directories
        new = os.path.join(os.getcwd(), 'pathname')
        create_directories(os.getcwd(), "pathname")

        self.assertTrue(os.path.isdir(new))
        shutil.rmtree(new)
        

class FindersTest(TestCase):
    def test_find_models_with_field(self):
        from media_helper.tools.finders import find_models_with_field
    
        m = TestModel
        n = find_models_with_field(models.ImageField)

        self.assertTrue(n.count(m) == 1)

    def test_find_field_attribute(self):
        from media_helper.tools.finders import find_field_attribute
        
        self.assertTrue(["image"], find_field_attribute("name", TestModel))