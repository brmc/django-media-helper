#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings as django_settings
from media_helper import settings
import os


def check_encoding(image_name):
    ''' Checks for valid image encodings

    if the file extension is allowed, returns the encoding
    otherwise, returns false

    Arguments:
    :param image_name: file name, can be relative or absolute
    :type image_name: str
    :returns: str or False
    '''
    encoding = image_name.split('.')[-1]

    # Accomodating for PIL's shortcoming
    if encoding.lower() == "jpg":
        encoding = "jpeg"

    if encoding not in settings.ALLOWED_ENCODINGS:
        return False

    return encoding


def construct_paths(image_name):
    ''' Construcs a dict of commonly used paths

    These are a series of similar paths used and translated during the request
    and response process.  It creates paths for the
       - location on disc,
       - the URL it was requested by
       - the media-helper equivalents of both
       - the physical backup/master-image path
       - and URL path for the backup

    :param image_name: the name of the image with the upload_to dir prepended
    :type image_name: string
    :returns: dict
    '''
    image_name = image_name.split(django_settings.MEDIA_URL)[-1]
    encoding = check_encoding(image_name)

    return {
        'image_name': image_name,
        'request_path': os.path.join(django_settings.MEDIA_URL, image_name),
        'request_system_path': os.path.join(
            django_settings.MEDIA_ROOT,
            image_name),
        'response_path': os.path.join(
            django_settings.MEDIA_URL,
            'media-helper',
            image_name),
        'media_helper_root': os.path.join(
            django_settings.MEDIA_ROOT,
            'media-helper'),
        'backup_path': os.path.join(
            django_settings.MEDIA_ROOT,
            'media-helper',
            image_name,
            "original.%s" % encoding),
        'backup_response_path': os.path.join(
            django_settings.MEDIA_URL,
            'media-helper',
            image_name,
            'original.%s' % encoding),
        'response_system_path': os.path.join(
            django_settings.MEDIA_ROOT,
            'media-helper',
            image_name)
    }


def create_directories(directory, image_name):
    """ Creates new directories in the media-helper directory

    Arguments:
    :param directory: root directory
    :type directory: str
    :param image_name: the name of the image including the upload_to dir
    type image_name: str
    """

    new_dir = os.path.join(directory, image_name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
