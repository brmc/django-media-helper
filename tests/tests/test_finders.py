from django.test import TestCase
from django.db import models
from media_helper.models import TestModel
from media_helper.tools.finders import (
    find_models_with_field,
    find_field_attribute)


class FindersTest(TestCase):
    def test_find_models_with_field(self):

        m = TestModel
        n = find_models_with_field(models.ImageField)

        self.assertTrue(n.count(m) == 1)

    def test_find_field_attribute(self):

        self.assertTrue(["image"], find_field_attribute("name", TestModel))
