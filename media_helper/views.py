from django.shortcuts import get_object_or_404, get_list_or_404, render
#from django.template.defaultfilters import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.conf import settings as dj_settings
from media_helper.settings import Settings
from .resizer import resize_all, resize, resize_exact

def create_image_path(images):
    import os
    new_images = {}
    for image in images:
            old_request_path = os.path.join(dj_settings.MEDIA_URL, image[0])
            new_image_path = os.path.join(dj_settings.MEDIA_ROOT, str(image[1]), image[0])
            new_request_path = os.path.join(dj_settings.MEDIA_URL, str(image[1]), image[0])
            print new_image_path == new_request_path    
            if os.path.isfile(new_image_path):
                new_images[old_request_path] = new_request_path
            else:
                print "resizing"
                if resize_exact(image[0], image[1]) == True:
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
        print images

        #new_image_path = os.path.join(dj_settings.MEDIA_ROOT, width)
        #size = Settings().generate_scaling_factors([width,])
        
        '''if os.path.exists(new_image_path):
           pass
        else:
            #resize_all(dj_settings.MEDIA_ROOT, width )
            resize_exact()

            new_images = []
'''

        new_images = create_image_path(images)
        new_backgrounds = create_image_path(backgrounds)
        

        json = { 'images' : new_images, }

        json['backgrounds'] = new_backgrounds
        json = dumps(json)
                
        print json
            
        request.session['width'] = width
        return HttpResponse(json, content_type = "application/json")

    else:
        return HttpResponseForbidden()

def insert_folder(width):
    '''Choses folder larger than width'''
    pass#return [key for key, val in get_sizes().iteritems() if float(key) > width]

