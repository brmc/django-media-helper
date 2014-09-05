#from pillow import Image

from django.test import TestCase
from django.conf import settings
from django.db import models
from media_helper.models import TestModel
from .settings import Settings
#from football.models import Test

class HelpersTest(TestCase):
    def test_construct_paths(self):
        from media_helper.tools.helpers import construct_paths
        self.assertTrue(False)