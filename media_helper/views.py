from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings as dj_settings

from .settings import Settings
from .tools.resizers import resize # resize_all, 
from .tools.helpers import construct_paths, check_encoding


def get_resized_images(images):
    ''' Constructs a new image path for the appropriately sized image
    
    If an image can't be resized, it falls back to the default image.

    Changes have been made.
    Previously it:
        prepended MEDIA_URL to the path
        prepended <image size in px> to the path

        previous form:
        MEDIA_URL/<upload_to>/<size>/filename.ext

    Now it:
        prepends MEDIA_URL
        prepends 'media_helper/'
        appends 'filename.ext/' as directory
        appends '<image size>.ext' as file

        current form:
        media_helper/<upload_to>/filename.ext/<size>.jpg

    Arguments:
    :param images: images paired with their new sizes
        image[0]: 'upload_to/image.ext'
        image[1]: integer
    :type images: list of tuples of strings
    :returns: dict 
    '''

    import os

    new_images = {}

    for image in images:
        # Common paths used often by this app.
        paths = construct_paths(image[0])
        old_request_path = paths['request_path']
        
        # Only certain types of encodings are allowed by the settings
        encoding = check_encoding(image[0])
        if not encoding:
            new_images[old_request_path] = old_request_path
            continue

        # image sizes will be rounded
        new_size = image[1]
        round_to = Settings().round_to

        if new_size % round_to != 0:
            new_size += round_to - new_size % round_to

        # named according to size
        resized_image_name = "%d.%s" % (new_size, encoding)            
        new_request_path = os.path.join(paths['response_path'], resized_image_name)
        new_image_path = os.path.join(paths['response_system_path'], resized_image_name)
        
        if os.path.isfile(new_image_path):
            new_images[old_request_path] = new_request_path

        elif not image[0].startswith(dj_settings.STATIC_URL):
            result = resize(image[0], image[1]) 
            
            if result == True: # successful resizing
                new_images[old_request_path] = new_request_path
            elif result == False: # failed.  Low-res used
                new_images[old_request_path] = old_request_path
            else:  # requested size was larger than original.  Original returned
                new_images[old_request_path] = result
        
        else:
            new_images[old_request_path] = old_request_path         
    return new_images

def check_images(images):
    from ast import literal_eval
    
    try:  # convert to python object
        images = literal_eval(images)
    except:
        return None

    # Check if images is a list of (str, int) tuples
    if (isinstance(images, list) and 
            len(images) > 0 and
            isinstance(images[0], tuple) and
            len(images[0]) == 2 and
            isinstance(images[0][0], str) and 
            isinstance(images[0][1], int)):
        return images
    return None


def resolution(request):
    ''' Finds or resizes images and returns them via ajax '''
    import warnings
    warnings.warn(
        "The name of this view/URL pair will be changed in future versions. Its name no longer"\
        "reflects its function.  Please take note.",
        DeprecationWarning
        )
    
    if request.is_ajax():
        import os
        from json import dumps

        json = {}
        # Get, convert, and check data from client
        images = check_images(request.POST.get('images'))
        if images is not None:
            new_images = get_resized_images(images )
            json['images'] = new_images

        # same as above...i don't remember why i have these separate, but i 
        # know I had a reason at some point.
        backgrounds = check_images(request.POST.get('backgrounds'))
        if backgrounds is not None:
            new_backgrounds = get_resized_images(backgrounds)
            json['backgrounds'] = new_backgrounds
        
        json = dumps(json)

        return HttpResponse(json, content_type = "application/json")

    else:
        return HttpResponseForbidden()
