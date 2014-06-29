# coding: utf-8
import os
from PIL import Image

import django
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.conf import settings

def find_models_with_imagefield(): 
    '''
    Returns a list of models that have an image field
    '''
    result = []
    for model in models.get_models():
        for field in model._meta.fields:
            if isinstance(field, models.ImageField):
                result.append(model)
                break
    return result

def get_sizes():
    '''
    Tries to import the following user defined settings, 
    otherwise falls back to default.  Returns a list:
    
    MEDIA_HELPER_AUTO_SIZES: Bool
        Determines whether to use a list of pre-defined resolutions or,
        to have them automatically generated

    MEDIA_HELPER_SIZES: list of integers, floats, or strings
        These will be the resolutions to resize for

    MEDIA_HELPER_MAX, MEDIA_HELPER_MIN: integer
        These ranges will be used for the automatic generation of sizes
        * Max and Min are both inclusive

    MEDIA_HELPER_STEP_SIZE: integer
        Increments between minimum and maximum resolutions

        For example, if the user defines:
        MEDIA_HELPER_AUTO_SIZES= True
        MEDIA_HELPER_MIN = 1
        MEDIA_HELPER_MAX = 10
        MEDIA_HELPER_STEP_SIZE = 5

    get_sizes() will return [1, 5, 10]

    '''
    import settings as default_settings

    try:
        auto = settings.MEDIA_HELPER_AUTO_SIZES
    except AttributeError as e:
        auto = default_settings.MEDIA_HELPER_AUTO_SIZES
    except:
        print "Yo settins be all woogely-boogely.  Fix em so dat MEDIA_HELPER_AUTO_SIZES is troof oder not troof wit a big T and F"
        raise

    if not auto:
        try:
            sizes = settings.MEDIA_HELPER_SIZES
        except AttributeError:
            #default scaling factors for various screen widths
            sizes = default_settings.MEDIA_HELPER_SIZES
            print "poo"
    else:
        try:
            maximum = settings.MEDIA_HELPER_MAX
            minimum = settings.MEDIA_HELPER_MIN
            step_size = settings.MEDIA_HELPER_STEP_SIZE

        except AttributeError:
            maximum = default_settings.MEDIA_HELPER_MAX
            minimum = default_settings.MEDIA_HELPER_MIN
            step_size = default_settings.MEDIA_HELPER_STEP_SIZE

        if maximum < minimum:
            maximum, minimum = minimum, maximum

        if step_size > maximum - minimum:
            print 'yo step size b 2 big. lol. y u so dum?!?'
            raise

        sizes = range(minimum, maximum + 1, step_size)
        

    return generate_sizes(sizes)

def generate_sizes(resolutions):
    '''
    Accepts a list of resolutions to generate a dict of percentages
    that will be used to scale the image in resize()

    '''

    try:
        resolutions = map(float, resolutions)
    except ValueError:
        print 'dem aint numbers. fix em.'
        raise

    minimum, maximum = min(resolutions), max(resolutions)
    sizes = {str(i): i / maximum for i in resolutions}

    return sizes

def resize(sender, instance, *args, **kwargs):
    '''
    This resizes images for screen widths between 800 and 2560px.
    '''
    media_root = settings.MEDIA_ROOT
    encoding = instance.image.name.split('.')[-1]
    # set path for image upload directory
    #path = "%s/images/" % base_path
    sizes = get_sizes()

    # checks for folder directory.  Creates dirs if doesn't exist
    for key in sizes.iterkeys():
        new_dir = os.path.join(media_root,key, instance.image.field.upload_to)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    # sets full path of image to be opened
    item_path = os.path.join(media_root, instance.image.name)
    image = Image.open(item_path)

    width, height = image.size

    # iterates over sizes, scales, and saves accordingly.
    for key, val in sizes.iteritems():
        new_image = image.resize((int(width * val),int(height * val)) , Image.ANTIALIAS)  
     
        try:
            new_image.save(os.path.join(media_root, key, instance.image.name), encoding,  quality=85)

        except KeyError:
            print "Unknown encoding or bad file name"
            raise


def delete_resized_images(sender, instance, *args, **kwargs):
    '''
    Iterates over the defined sizes, and deletes images in those directories
    '''
    for key in get_sizes().iterkeys():
        image = os.path.join(settings.MEDIA_ROOT, key, instance.image.name)
        if os.path.isfile(image):
            os.remove(image)

def resize_signals():
    for model in find_models_with_imagefield():
        post_save.connect(resize, sender = model)
        pre_delete.connect(delete_resized_images, sender = model)

