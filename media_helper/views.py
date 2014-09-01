from django.shortcuts import get_object_or_404, get_list_or_404, render
#from django.template.defaultfilters import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.conf import settings as dj_settings
from media_helper.settings import Settings
from .resizer import resize_all, resize, construct_paths, check_encoding

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
        # These are paths that will be used often by this app.
        paths = construct_paths(image[0])
        old_request_path = paths['request_path']
        
        # Only certain types of encodings are allowed by the settings
        encoding = check_encoding(image[0])
        if not encoding:
            continue

        # New images will be named according to their size
        # image[1] is an integer
        tail = "%d.%s" % (image[1], encoding)            
        new_request_path = os.path.join(paths['response_path'], tail)
        new_image_path = os.path.join(paths['response_system_path'], tail)

        if os.path.isfile(new_image_path):
            new_images[old_request_path] = new_request_path
        else:
            if resize(image[0], image[1]) == True:
                new_images[old_request_path] = new_request_path
            else:
                # Fallback
                new_images[old_request_path] = old_request_path           

    return new_images

def resolution(request):
    ''' Finds or resizes images and returns them via ajax '''
    
    warnings.warn(
        "The name of this view/URL pair will be changed in future versions. Its name no longer"\
        "reflects its function.  Please take note.",
        DeprecationWarning
        )

    if request.is_ajax():
        import os
        from ast import literal_eval
        from json import dumps

        json = {}

        images = literal_eval(request.POST.get('images']))
        if images is not None:
            new_images = get_resized_images(images )
            json['images'] = new_images

        backgrounds = literal_eval(request.POST.get('backgrounds']))
        if backgrounds is not None:
            new_backgrounds = get_resized_images(backgrounds)
            json['backgrounds'] = new_backgrounds
        
        json = dumps(json)

        return HttpResponse(json, content_type = "application/json")

    else:
        return HttpResponseForbidden()

def insert_folder(width):
    '''Choses folder larger than width'''
    pass#return [key for key, val in get_sizes().iteritems() if float(key) > width]

