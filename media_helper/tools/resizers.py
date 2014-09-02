#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import warnings
from PIL import Image

import django
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from media_helper.settings import Settings

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

    if encoding not in Settings().allowed_encodings:
        return False

    return encoding

def create_directories(directory, image_name):
    """ Creates new directories in the media-helper directory

    This creates an additional directory from the image name underwhich
    corresponding resized images with be saved.

    Arguments:
    :param directory: root directory
    :type directory: str
    :param image_name: the name of the image including the upload_to dir
    type image_name: str
    """

    # This needs to be optimized after the path schema changed.  It works, but
    # is wasteful
    
    new_dir = os.path.join(directory, image_name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    

def resize(image_path, new_width):
    """ A single image is resized and saved to a new directory.

    Arguments:
    :param image_path: the upload_to directory and the file name 
    :type image_path: string
    :param new_width: new width in px
    :type new_width: int
    :returns: None
    """
    from PIL import Image

    paths = construct_paths(image_path)
    image_name = paths['image_name']
 
    encoding = check_encoding(image_name)
    if not encoding:
        return False

    if not os.path.isfile(paths['backup_path']):
        move_original(paths['request_system_path'])
        resize_original(paths['request_system_path'])

    image = Image.open(paths['backup_path'])
    
    width, height = image.size
    scaling_factor = float(new_width) / float(width)

    new_image = image.resize((new_width, int(height * scaling_factor)), Image.ANTIALIAS)
    create_directories(paths['media_helper_root'], image_name)

    try:
        new_image.save(os.path.join(paths['response_system_path'], str(new_width) + "." + encoding,), encoding,  quality=85, optimize = True)
        return True
    except KeyError:
        print "Unknown encoding or bad file name"
        return False
    except IOError:
        return False


def construct_paths(image_name):
    ''' Construcs a dict of commonly used paths 

    :param image_name: the name of the image with the upload_to dir prepended
    :type image_name: string
    :returns: dict
    '''
    image_name = image_name.split(settings.MEDIA_URL)[-1]
    encoding = check_encoding(image_name)

    return {
        'image_name': image_name,
        'request_path': os.path.join(settings.MEDIA_URL, image_name),
        'request_system_path': os.path.join(settings.MEDIA_ROOT, image_name),
        'response_path': os.path.join(settings.MEDIA_URL, 'media-helper', image_name),
        'media_helper_root': os.path.join(settings.MEDIA_ROOT, 'media-helper'),
        'backup_path': os.path.join(settings.MEDIA_ROOT, 'media-helper', image_name, "original.%s" % encoding),
        'response_system_path': os.path.join(settings.MEDIA_ROOT, 'media-helper', image_name)

    }



def move_original(image_path):
    ''' Copies the original image to a backup directory 

    This image will be the image used when resizing.

    :param image_path: absolute or relative path of image
    :type image_path: str
    :returns: True or False depending on success.
    '''

    import shutil
    
    paths = construct_paths(image_path)
    
    try:
        image = Image.open(image_path)
    except IOError:
        return False
    encoding = check_encoding(paths['image_name'])

    if not encoding:
        return False

    # create original path in media-helper
    create_directories(paths['media_helper_root'], paths['image_name'],)
    try:
        shutil.copy(paths['request_system_path'], paths['backup_path'])
    except:
        return True

    return True

def resize_original(image_path):
    ''' Creates a low-quality version of the original image

    This will be delivered by the initial request and will be replaced via ajax
    :param image_path: absolute location of image.

    If this resizing fails, it will do so silently and use the original
    :type image_path: str
    '''
    default_size = Settings().default

    try:
        image = Image.open(image_path)
    except IOError:
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
        image.save(image_path, encoding,  quality=85, optimize = True)
    except:
        warnings.warn(
        "The image couldn't be resized.  The original is being used",
        DeprecationWarning
    )

def resize_on_save(sender, instance, *args, **kwargs):
    """ Resizes an image when a model field is saved according to user-defined settings.
    """
    default_size = Settings().default

    sizes = Settings().get_sizes()
    maximum = Settings().maximum
   
    # sets full path of image to be opened
    for name in find_field_attribute("name", instance):
        image_instance = getattr(instance, name)
        move_original(image_instance.file.name)

        image_path = image_instance.file.name

        image = Image.open(image_path)
       
        width, height = image.size
        # iterates over sizes, scales, and saves accordingly.
        for size in sizes:
            resize(image_path, int(size * maximum))

        resize_original(image_path)


    
def delete_resized_images(sender, instance, *args, **kwargs):
    """ Deletes all scaled images folder when image is deleted """
    from .finders import find_field_attribute
    import shutil
    
    for name in find_field_attribute("name", instance):
        directory = os.path.join(settings.MEDIA_ROOT, 'media-helper', getattr(instance, name).name)
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    

def resize_signals():
    """Connects signals for resizing and deletion"""
    from .finders import find_models_with_field
    for model in find_models_with_field(models.ImageField):
        post_save.connect(resize_on_save, sender = model)
        pre_delete.connect(delete_resized_images, sender = model)

