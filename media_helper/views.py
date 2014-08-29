from django.shortcuts import get_object_or_404, get_list_or_404, render
#from django.template.defaultfilters import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.conf import settings as dj_settings
from media_helper.settings import Settings
from .resizer import resize_all, resize, resize_exact

def create_image_path(images):
    ''' Constructs a new image path for the appropriately sized image

    Currently:
        prepends MEDIA_URL to the path
        prepends <image size in px> to the path

        current form:
        MEDIA_URL/<upload_to>/<size>/filename.ext
    Should:
        prepend MEDIA_URL
        prepend 'media_helper/'
        append 'filename.ext/' as directory
        append '<image size>.ext' as file

        final form:
        media_helper/<upload_to>/filename.ext/<size>.jpg

    Arguments:
    :param images: images paired with their new sizes
    :type images: list of tuples of strings
    :returns: dict 
    '''

    import os
    new_images = {}
    for image in images:
        old_request_path = os.path.join(dj_settings.MEDIA_URL, image[0])
        encoding = image[0].split(".")[-1]

        if encoding.lower() == "jpg":
            encoding = "jpeg"

        if encoding not in Settings().allowed_encodings:
            new_images[old_request_path] = old_request_path
            break
        
        tail = "/".join([
            'media-helper',
            image[0], 
            "%d.%s" % (image[1], encoding)
            ])

        new_request_path = os.path.join(dj_settings.MEDIA_URL, tail)
        
        new_image_path = os.path.join(dj_settings.MEDIA_ROOT, tail)
         
        if os.path.isfile(new_image_path):
            new_images[old_request_path] = new_request_path
        else:
            print "resizing"
            # This is where the round problem starts
            if resize_exact(image[0], image[1]) == True:
                print "no path"
                new_images[old_request_path] = new_request_path
            else:
                new_images[old_request_path] = old_request_path            

    return new_images

def resolution(request):
    '''Sets new session variable based on screen width'''
    if request.is_ajax():
        import os
        from ast import literal_eval
        from json import dumps

        width = request.POST['width']
        images = literal_eval(request.POST['images'])
        backgrounds = literal_eval(request.POST['backgrounds'])
        
        new_images = create_image_path(images)
        new_backgrounds = create_image_path(backgrounds)
        
        json = { 'images' : new_images, }

        json['backgrounds'] = new_backgrounds
        json = dumps(json)

        request.session['width'] = width
        return HttpResponse(json, content_type = "application/json")

    else:
        return HttpResponseForbidden()

def insert_folder(width):
    '''Choses folder larger than width'''
    pass#return [key for key, val in get_sizes().iteritems() if float(key) > width]

