import os
import shutil
from django.test import TestCase
from django.conf import settings as django_settings

from media_helper import settings
from media_helper.tools.resizers import resize, move_original
from media_helper.tools.helpers import construct_paths


project_dir = os.path.abspath(os.path.dirname(__name__))

if 'tests' in project_dir:
    PROJECT_ROOT = os.path.join(os.getcwd(), 'test-files')
else:
    PROJECT_ROOT = os.path.join(
        os.path.abspath(os.path.dirname(__name__)),
        'tests',
        'test-files')


class ResizersTest(TestCase):
    scaling_factors = {
        '2': 0.1,
        '10': 0.5,
        '20': 1.0
    }
    sizes = [2, 10, 20]
    image_path = "upload/image.jpg"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))

    def test_resize(self):
        django_settings.MEDIA_URL = '/test-files/'

        root = django_settings.MEDIA_ROOT = PROJECT_ROOT

        image_path = os.path.join(root, "upload/image.jpg")
        paths = construct_paths(image_path)

        self.assertTrue(resize(image_path, 30))
        resized = os.path.join(paths['response_system_path'], '30.jpeg')

        self.assertTrue(os.path.isfile(resized))

        shutil.copy(paths['backup_path'], image_path)
        shutil.rmtree(paths['media_helper_root'])

    def test_move_original(self):
        django_settings.MEDIA_URL = '/test-files/'

        root = django_settings.MEDIA_ROOT = PROJECT_ROOT

        image_path = os.path.join(root, "upload/image.jpg")
        self.assertTrue(isinstance(move_original(image_path), str))

    def test_default_settings(self):
        self.assertTrue(settings.AUTO)
        self.assertEqual(
            settings.SIZES,
            [0.3, 0.3125, 0.4, 0.426953125, 0.45, 0.5, 0.53125, 0.546875,
                0.5625, 0.6, 0.625, 0.65625, 0.75, 0.8, 1.0])

        self.assertEqual(settings.MINIMUM, 20)
        self.assertEqual(settings.DEFAULT, .1)
        self.assertEqual(settings.QUALITY, 50)
        self.assertEqual(settings.ROUND_TO, 10)
        self.assertEqual(settings.ALLOWED_ENCODINGS, ['jpg', 'jpeg', 'png'])
        self.assertEqual(settings.IMAGE_SELECTORS, "img")
        self.assertEqual(settings.BACKGROUND_SELECTORS, "div")
