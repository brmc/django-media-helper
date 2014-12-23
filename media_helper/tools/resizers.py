#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import warnings
from PIL import Image

from django.conf import settings as django_settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from media_helper import settings
from .helpers import construct_paths, check_encoding, create_directories


def resize(image_path, new_width, filename=None):
    """ A single image is resized and saved to a new directory.

    This is the cornerstone of the app where all resizing actually happens.
    This function receives the image path (relative or absolute with the
    upload_to folder prepended) and the new size of the image.

    Using the image path as a guide, the master copy of the image is loaded,
    and if the encoding is allowed by the settings, a resized image will be
    created. To avoid too many images being created, images will be rounded up
    to a value determined by the setting `MEDIA_HELPER_ROUND_TO`

    If no backup image is found, one will be created, and a low-res placeholder
    image to go with it.

    Arguments:
    :param image_path: the upload_to directory and the file name. extra path
                       info is ok too.  absolute paths will be stripped.
    :type image_path: string
    :param new_width: new width in px
    :type new_width: int
    :returns: True or False
    """

    paths = construct_paths(image_path)
    image_name = paths['image_name']

    encoding = check_encoding(image_name)
    if not encoding:
        return False

    if not os.path.isfile(paths['backup_path']):
        move_original(paths['request_system_path'])
        resize_original(paths['request_system_path'], paths['backup_path'])

    try:
        image = Image.open(paths['backup_path'])
    except (OSError, IOError):
        return paths['backup_response_path']

    width, height = image.size
    round_to = settings.ROUND_TO

    # Round up
    if new_width % round_to != 0:
        new_width += round_to - new_width % round_to

    # Don't resize larger than the original size
    if new_width > width:
        return paths['backup_response_path']
    if new_width < settings.MINIMUM:
        new_width = settings.MINIMUM

    scaling_factor = float(new_width) / float(width)

    new_image = image.resize(
        (new_width, int(height * scaling_factor)),
        Image.ANTIALIAS)

    quality = 'keep' if new_image.format == 'JPEG' else 85

    create_directories(paths['media_helper_root'], image_name)
    filename = str(new_width) if filename is None else filename

    try:
        new_image.save(
            os.path.join(
                paths['response_system_path'],
                filename + "." + encoding,
            ),
            encoding,
            quality=quality,
            optimize=True)
        return True
    except KeyError:
        print("Unknown encoding or bad file name")
    except (IOError, SystemError):
        print("Corrupt data.  Check yo nuts: %s " % paths['backup_path'])

    return False


def move_original(image_path):
    ''' Copies the original image to a backup directory

    This image will be the master copy used when resizing, and it will be
    stored in <MEDIA_ROOT>/media-helper/<imagename>/original.ext

    It is called on saving, when no backup image is found, and when using the
    `media_helper` commands.

    :param image_path: absolute or relative path of image
    :type image_path: str
    :returns: True, False, or the path of the backup image.
    '''

    import shutil

    try:
        paths = construct_paths(image_path)
        encoding = check_encoding(paths['image_name'])
    except IOError:
        return False

    if not encoding:
        return False

    # create original path in media-helper
    create_directories(paths['media_helper_root'], paths['image_name'],)
    try:
        shutil.copy(paths['request_system_path'], paths['backup_path'])
    except:
        return True

    return paths['backup_path']


def resize_original(image_path, backup_path):
    ''' Creates a low-quality version of the original image

    This image will be the placeholder image first rendered by the template and
    will be replaced via ajax once an appropriate image is found or created.

    It is called when a model is saved, when an image is resized and no backup
    copy is found, or from the the `mediahelper` management command.

    Arguments:
    :param image_path: absolute location of image.
    :type image_path: str
    :param backup_path: path of the backup copy of the time
    :type backup_path: str
    If this resizing fails, it will do so silently and use the original
    :returns: True or False, depending on success
    '''
    default_size = settings.DEFAULT
    default_quality = settings.QUALITY
    try:
        image = Image.open(backup_path)
    except IOError:
        warnings.warn(
            "The image couldn't be resized.  The original is being used",
            Warning
        )
        return False

    width, height = image.size
    encoding = check_encoding(image_path)
    if not encoding:
        return False

    try:
        image = image.resize(
            (int(width * default_size), int(height * default_size)),
            Image.ANTIALIAS
        )
        image.save(
            image_path,
            encoding,
            quality=default_quality,
            optimize=True
        )
        return True
    except:
        warnings.warn(
            "The image couldn't be resized.  The original is being used",
            Warning
        )
        return False


def resize_on_save(sender, instance, *args, **kwargs):
    """ Resizes an image when a model field is saved

    If the `MEDIA_HELPER_AUTO` setting is True, a series of images will be
    generated when a model field is saved.  The images will be scaled down
    according to the `MEDIA_HELPER_SIZES` setting.

    Obviously this is called when the model is saved.
    """
    from .finders import find_field_attribute

    if not settings.AUTO:
        return

    sizes = settings.SIZES

    # sets full path of image to be opened
    for name in find_field_attribute("name", instance):
        image_instance = getattr(instance, name)
        backup_path = move_original(image_instance.file.name)

        image_path = image_instance.file.name

        image = Image.open(image_path)

        width, height = image.size
        # iterates over sizes, scales, and saves accordingly.
        for size in sizes:
            resize(image_path, int(size * width))

        resize_original(image_path, backup_path)


def delete_resized_images(sender, instance, *args, **kwargs):
    """ Deletes all scaled images folder when image is deleted

    When an image is changed or deleted, the corresponding directory tree in
    <MEDIA_ROOT>/media-helper will be also removed.
    """
    from .finders import find_field_attribute
    import shutil

    for name in find_field_attribute("name", instance):
        directory = os.path.join(
            django_settings.MEDIA_ROOT,
            'media-helper',
            getattr(instance, name).name
        )
        if os.path.isdir(directory):
            shutil.rmtree(directory)


def resize_signals():
    """Connects signals for resizing and deletion"""
    from .finders import find_models_with_field
    for model in find_models_with_field(models.ImageField):
        post_save.connect(resize_on_save, sender=model)
        pre_delete.connect(delete_resized_images, sender=model)
