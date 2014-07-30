# coding: utf-8
import os
from PIL import Image

import django
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.conf import settings

def find_models_with_field(field_type): 
    '''
    Returns a list of models that have an image field
    '''
    result = []
    for model in models.get_models():
        for field in model._meta.fields:
            if isinstance(field, field_type):
                result.append(model)
                break
    return result

def find_upload_dirs(model_list):
    dirs = []
    for model in model_list:
        for field in model._meta.fields:
            if isinstance(field, models.ImageField) and field.upload_to is not '.':
                dirs.append(field.upload_to)

    return dirs

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

def generate_sizes(widths):
    '''
    Accepts a list of screen widths to generate a dict of percentages
    that will be used to scale the image in resize()

    '''
    try:
        from media_helper.settings import MEDIA_HELPER_MAX as maximum
        from media_helper.settings import MEDIA_HELPER_MIN as minimum
    except ImportError:
        minimum, maximum = min(widths), max(widths)

    try:
        widths = map(float, widths)
    except ValueError:
        print 'dem aint numbers. fix em.'
        raise

    
    sizes = {str(int(round(i, 0))): i / maximum for i in widths}

    return sizes

def create_directories(sizes, media_root, upload_to):
    '''
    This accepts a dict of sizes and checks for a directory 'upload_to'
    located in media_root/size. If it doesn't already exist, is is created
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
    
    
    sizes = get_sizes()
    create_directories(sizes, media_root, instance.image.field.upload_to)
    
    # sets full path of image to be opened
    item_path = os.path.join(media_root, instance.image.name)
    image = Image.open(item_path)

    #width, height = image.size

    # iterates over sizes, scales, and saves accordingly.
    for key, val in sizes.iteritems():
        resize(media_root, key, val, image_path)



def resize_all(media_root, resolution):
    '''
    Resizes all images in upload directories for a new resolution

    :param root MEDIA_ROOT
    :param resolution a string representation of an integer
    '''
    new_size = generate_sizes([resolution,])
     
    upload_dirs = find_upload_dirs(find_models_with_field(models.ImageField))

    
    for x in upload_dirs:
        # Source dir of images to be resized
        source_dir = os.path.join(media_root, x)
        
        if os.path.isdir(source_dir):
            resize_dir = os.path.join(media_root, resolution, x)
            
            create_directories(new_size, media_root, x)
            
            for subdir, dirs, files in os.walk(source_dir):
                for file in files:
                    new_file = os.path.join(resize_dir, x, file)
                    
                    if not os.path.isfile(new_file):
                        image_path = os.path.join(subdir, file)
                        #image = Image.open(image_path)

                        # This is ugly because django prepends the upload_to dir to the filename when
                        # saving.  It works, but I need to clean it up.
                        resize(media_root, new_size.keys()[0], new_size.values()[0], image_path)

    
def delete_resized_images(sender, instance, *args, **kwargs):
    '''
    Iterates over the defined sizes, and deletes images in those directories
    '''
    for key in get_sizes().iterkeys():
        image = os.path.join(settings.MEDIA_ROOT, key, instance.image.name)
        if os.path.isfile(image):
            os.remove(image)

def resize_signals():
    for model in find_models_with_field(models.ImageField):
        post_save.connect(resize_multiple, sender = model)
        pre_delete.connect(delete_resized_images, sender = model)

