import os
import shutil
from django.test import TestCase
from django.conf import settings as django_settings

from media_helper.tools.helpers import (
    create_directories,
    check_encoding,
    construct_paths)


class HelpersTest(TestCase):
    def test_construct_paths(self):

        django_settings.MEDIA_URL = '/test-files/'
        django_settings.MEDIA_ROOT = '/junky-butter/peanuts/'

        paths = construct_paths("doo/1.jpg")

        self.assertEqual(
            paths['image_name'],
            'doo/1.jpg')
        self.assertEqual(
            paths['request_path'],
            '/test-files/doo/1.jpg')
        self.assertEqual(
            paths['request_system_path'],
            '/junky-butter/peanuts/doo/1.jpg')
        self.assertEqual(
            paths['response_path'],
            '/test-files/media-helper/doo/1.jpg')
        self.assertEqual(
            paths['media_helper_root'],
            '/junky-butter/peanuts/media-helper')
        self.assertEqual(
            paths['backup_path'],
            '/junky-butter/peanuts/media-helper/doo/1.jpg/original.jpeg')
        self.assertEqual(
            paths['backup_response_path'],
            '/test-files/media-helper/doo/1.jpg/original.jpeg')
        self.assertEqual(
            paths['response_system_path'],
            '/junky-butter/peanuts/media-helper/doo/1.jpg')

    def test_check_encoding(self):
        self.assertEqual("jpeg", check_encoding('.jpg'))
        self.assertEqual('png', check_encoding('.png'))
        self.assertFalse(check_encoding(".joop"))

    def test_create_directories(self):
        new = os.path.join(os.getcwd(), 'pathname')
        create_directories(os.getcwd(), "pathname")

        self.assertTrue(os.path.isdir(new))
        shutil.rmtree(new)
