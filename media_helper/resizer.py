# coding: utf-8
import os
from PIL import Image

import django
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from .settings import Settings

def find_models_with_field(field_type): 
    """Returns a list of models that have the specified field type.

    Arguments:
    :param field_type: the type of field to search for
    :type field_type: a field from django.db.models

    :returns: list of models from installed apps
    """
    result = []
    for model in models.get_models():
        for field in model._meta.fields:
            if isinstance(field, field_type):
                result.append(model)
                break
    return result

def find_upload_dirs(model_list):
    """Finds all upload_to directories for ImageFields

    Arguments:
    :param model_list: a list of models from installed apps
    :type model_list: a list of models
    :returns: list of upload paths 
    """
    dirs = []
    for model in model_list:
        for field in model._meta.fields:
            if isinstance(field, models.ImageField) and field.upload_to is not '.':
                dirs.append(field.upload_to)

    return dirs

def create_directories(media_root, sizes, upload_to):
    ''' Creates new directories in the media directory

    Duplicates the directory structure of each upload_to for a series
    of sizes or screen widths

    Arguments:
    :param sizes: a list of screen widths
    :type sizes: list of strings or ints
    :param media_root: MEDIA_ROOT directory defined in settings
    :type media_root: string
    :param upload_to: upload directory defined in field definition
    :type upload_to: string
    '''

    for key in sizes.iterkeys():
        new_dir = os.path.join(media_root,key, upload_to)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

def resize(media_root, folder, scaling_factor, image_path):
    from PIL import Image

    image = Image.open(image_path)

    # This is necessary because django prepends upload_to to the filename when saving
    image_name = image_path.split(settings.MEDIA_URL)[-1]
    width, height = image.size
    encoding = image_name.split('.')[-1]

    if encoding.lower() == "jpg":
        encoding = "jpeg"

    new_image = image.resize((int(width * scaling_factor),int(height * scaling_factor)) , Image.ANTIALIAS)

    try:
        print os.path.join(media_root, folder, image_name)
        new_image.save(os.path.join(media_root, folder, image_name), encoding,  quality=85)
        #print os.path.join(media_root, folder, image_name)
    except KeyError:
        print "Unknown encoding or bad file name"
        raise

def resize_multiple(sender, instance, *args, **kwargs):
    '''
    This resizes images based on user-defined settings.
    '''
    
    # Root path in which to create directories for different
    # resolutions
    media_root = settings.MEDIA_ROOT

    # This assumes too much.  I should make this a bit more idiot-proof
    # In an ideal situation, this strips the filetype from the end of
    # the file name to be used later when encoding the scaled images
    # hrm...now that I think of it, this might actually be ok.  I should
    # check to see how ImageField validates filenames.
    
    
    sizes = Settings().generate_scaling_factors()
    create_directories(media_root, sizes, instance.image.field.upload_to)
    
    # sets full path of image to be opened
    item_path = os.path.join(media_root, instance.image.name)
    image = Image.open(item_path)

    #width, height = image.size

    # iterates over sizes, scales, and saves accordingly.
    for key, val in sizes.iteritems():
        resize(media_root, key, val, item_path)



def resize_all(media_root, width):
    ''' Resizes all images in upload directories for a new screen width

    :param root MEDIA_ROOT
    :param width: a string representation of an integer
    '''

    new_size = Settings().generate_scaling_factors([width,]) 
    upload_dirs = find_upload_dirs(find_models_with_field(models.ImageField))
    
    for upload_dir in upload_dirs:
        # Source dir from which images will be resized
        source_dir = os.path.join(media_root, upload_dir)
        
        if os.path.isdir(source_dir):
            resize_dir = os.path.join(media_root, width, upload_dir)
            create_directories(media_root, new_size, upload_dir)
            
            for subdir, dirs, files in os.walk(source_dir):
                for file in files:
                    new_file = os.path.join(resize_dir, upload_dir, file)
                    
                    if not os.path.isfile(new_file):
                        image_path = os.path.join(subdir, file)
                        
                        resize(media_root, new_size.keys()[0], new_size.values()[0], image_path)

    
def delete_resized_images(sender, instance, *args, **kwargs):
    '''
    Iterates over the defined sizes, and deletes images in those directories
    '''
    
    for key in Settings().get_sizes():
        image = os.path.join(settings.MEDIA_ROOT, str(key), instance.image.name)
        if os.path.isfile(image):
            os.remove(image)

def resize_signals():
    """Connects signals for resizing and deletion"""

    for model in find_models_with_field(models.ImageField):
        post_save.connect(resize_multiple, sender = model)
        pre_delete.connect(delete_resized_images, sender = model)

