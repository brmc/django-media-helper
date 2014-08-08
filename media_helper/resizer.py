# coding: utf-8
import os
from PIL import Image

import django
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
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

def find_upload_dirs(*model_list):
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

def find_field_attribute(attribute, *model_list):
    """ Returns ImageField attributes

    So far this is just used to return the upload paths or field names.

    :param attribute: 

    """

    attributes = []
    for model in model_list:
        for field in model._meta.fields:
            if isinstance(field, models.ImageField) and field.upload_to is not '.':
                attributes.append(getattr(field, attribute))

    return attributes

def create_directories(media_root, sizes, *upload_to):
    """ Creates new directories in the media directory

    Duplicates the directory structure of each upload_to for a series
    of sizes or screen widths

    Arguments:
    :param sizes: a list of screen widths
    :type sizes: list of strings or ints
    :param media_root: MEDIA_ROOT directory defined in settings
    :type media_root: string
    :param upload_to: upload directory defined in field definition
    :type upload_to: string
    """

    for key in sizes.iterkeys():
        for directory in upload_to:
            new_dir = os.path.join(media_root,key, directory)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

def resize(media_root, folder, scaling_factor, image_path):
    """ A single image is resized and saved to a new directory.

    Arguments:
    :param media_root: the root path where the image will be saved
    :type media_root: string
    :param: folder: the new folder 
    :type  folder: string
    :param scaling_factor: factor by which the image will be scaled
    :type scaling_factor: float
    :param image_path: the upload_to directory and the file name 
    :type image_path: string
    :returns: None
    """

    from PIL import Image

    image_name = image_path.split(settings.MEDIA_URL)[-1]
    encoding = image_name.split('.')[-1]

    if encoding.lower() == "jpg":
        encoding = "jpeg"

    if encoding not in Settings().allowed_encodings:
        return

    image = Image.open(image_path)
    
    width, height = image.size

    new_image = image.resize((int(width * scaling_factor),int(height * scaling_factor)) , Image.ANTIALIAS)

    try:
        new_image.save(os.path.join(media_root, folder, image_name), encoding,  quality=85)
    
    except KeyError:
        print "Unknown encoding or bad file name"
        raise

def resize_exact(image_path, new_width):
    """ A single image is resized and saved to a new directory.

    Arguments:
    :param media_root: the root path where the image will be saved
    :type media_root: string
    :param: folder: the new folder 
    :type  folder: string
    :param scaling_factor: factor by which the image will be scaled
    :type scaling_factor: float
    :param image_path: the upload_to directory and the file name 
    :type image_path: string
    :returns: None
    """

    from PIL import Image

    image_name = image_path.split(settings.MEDIA_URL)[-1]
    encoding = image_name.split('.')[-1]
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)

    # Accomodating for PIL's shortcoming
    if encoding.lower() == "jpg":
        encoding = "jpeg"

    if encoding not in Settings().allowed_encodings:
        return False

    image = Image.open(image_path)
    
    width, height = image.size
    scaling_factor = float(new_width) / float(width)

    new_image = image.resize((new_width, int(height * scaling_factor)) , Image.ANTIALIAS)
    create_directories(settings.MEDIA_ROOT, {str(new_width): new_width}, *find_field_attribute("upload_to", *find_models_with_field(models.ImageField)))

    try:
        new_image.save(os.path.join(settings.MEDIA_ROOT, str(new_width), image_name), encoding,  quality=85)
        return True
    except KeyError:
        print "Unknown encoding or bad file name"
        return False



def resize_on_save(sender, instance, *args, **kwargs):
    """ Resizes an image when a model field is saved according to user-defined settings.
    """
    
    media_root = settings.MEDIA_ROOT

    sizes = Settings().generate_scaling_factors()

    for directory in find_field_attribute("upload_to", instance):
        create_directories(media_root, sizes, directory)
    
    # sets full path of image to be opened
    for name in find_field_attribute("name", instance):
        image_path = getattr(instance, name).file.name
        
        # iterates over sizes, scales, and saves accordingly.
        for key, val in sizes.iteritems():
            resize(media_root, key, val, image_path)



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
            create_directories(media_root, new_size, upload_dir)
            
            for subdir, dirs, files in os.walk(source_dir):
                for file in files:
                    new_file = os.path.join(resize_dir, upload_dir, file)
                    
                    if not os.path.isfile(new_file):
                        image_path = os.path.join(subdir, file)
                        
                        resize(media_root, new_size.keys()[0], new_size.values()[0], image_path)

    
def delete_resized_images(sender, instance, *args, **kwargs):
    """ Deletes all scaled images """
    
    for key in Settings().get_sizes():
        for name in find_field_attribute("name", instance): 
            image = os.path.join(settings.MEDIA_ROOT, str(key), getattr(instance, name).name)
            if os.path.isfile(image):
                os.remove(image)

def resize_signals():
    """Connects signals for resizing and deletion"""

    for model in find_models_with_field(models.ImageField):
        post_save.connect(resize_on_save, sender = model)
        pre_delete.connect(delete_resized_images, sender = model)

