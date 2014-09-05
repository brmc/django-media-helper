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
from .helpers import construct_paths, check_encoding, create_directories

def resize(image_path, new_width):
    """ A single image is resized and saved to a new directory.

    It will be rounded up according to the settings.

    Arguments:
    :param image_path: the upload_to directory and the file name. extra path
                       info is ok too.  absolute paths will be stripped. 
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
        resize_original(paths['request_system_path'], paths['backup_path'])

    image = Image.open(paths['backup_path'])
    
    width, height = image.size
    round_to = Settings().round_to

    # Round up
    if new_width % round_to != 0:
        new_width += round_to - new_width % round_to
    
    # Don't resize larger than the original size
    if new_width > width:
        return paths['backup_response_path']

    scaling_factor = float(new_width) / float(width)

    new_image = image.resize((new_width, int(height * scaling_factor)), Image.ANTIALIAS)
    create_directories(paths['media_helper_root'], image_name)

    try:
        new_image.save(os.path.join(paths['response_system_path'], str(new_width) + "." + encoding,), encoding,  quality=85, optimize = True)
        return True
    except KeyError:
        print "Unknown encoding or bad file name"
    except (IOError, SystemError):
        print "Corrupt data.  Check yo nuts: %s " % paths['backup_path']

    return False

def move_original(image_path):
    ''' Copies the original image to a backup directory 

    This image will be the image used when resizing.

    :param image_path: absolute or relative path of image
    :type image_path: str
    :returns: path of backup image.
    '''

    import shutil

    try:
        paths = construct_paths(image_path)
        image = Image.open(image_path)
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

    This will be delivered by the initial request and will be replaced via ajax
    :param image_path: absolute location of image.

    If this resizing fails, it will do so silently and use the original
    :type image_path: str
    '''
    default_size = Settings().default
    default_quality = Settings().quality
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
        image.save(image_path, encoding,  quality=default_quality, optimize = True)
        return True
    except:
        warnings.warn(
            "The image couldn't be resized.  The original is being used",
            Warning
        )
        return False

def resize_on_save(sender, instance, *args, **kwargs):
    """ Resizes an image when a model field is saved according to user-defined settings.
    """
    from .finders import find_field_attribute
    
    if not Settings().auto:
        return
        
    default_size = Settings().default

    sizes = Settings().sizes
    
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

def resize_all(media_root, width):
    """ Resizes all images in upload directories for a new screen width

    :param root MEDIA_ROOT
    :param width: a string representation of an integer
    """

    new_size = Settings().generate_scaling_factors([width,]) 
    upload_dirs = find_field_attribute("upload_to", *find_models_with_field(models.ImageField))
    
    # This block iterates through upload_to directories, each sub directory,
    # and finally resizes each file.
    for upload_dir in upload_dirs:
        # Source dir from which images will be resized
        source_dir = os.path.join(media_root, upload_dir)
        
        if os.path.isdir(source_dir):
            # The directory for the newly scaled images
            resize_dir = os.path.join(media_root, width, upload_dir)
            create_directories(media_root, upload_dir)
            
            for subdir, dirs, files in os.walk(source_dir):
                for file in files:
                    new_file = os.path.join(resize_dir, upload_dir, file)
                    
                    if not os.path.isfile(new_file):
                        image_path = os.path.join(subdir, file)
                        
                        resize(media_root, new_size.keys()[0], new_size.values()[0], image_path)

    
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

