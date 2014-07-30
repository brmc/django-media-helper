from django.shortcuts import get_object_or_404, get_list_or_404, render
#from django.template.defaultfilters import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.conf import settings
from .resizer import get_sizes, generate_sizes, resize_all

def resolution(request):
    '''Sets new session variable based on resolution'''
    if request.is_ajax():

        import os
        resolution = request.POST['resolution']
        #print "resolution", resolution
        #folder = insert_folder(resolution)
        new_path = os.path.join(settings.MEDIA_ROOT, resolution)
        #print resolution
        
        if os.path.exists(new_path):
            pass
        else:
            resize_all(settings.MEDIA_ROOT, resolution)
            
        request.session['resolution'] = resolution
        return HttpResponse("ok")

    else:
        return HttpResponseForbidden()

def insert_folder(resolution):
    '''Choses folder larger than resolution'''
    return [key for key, val in get_sizes().iteritems() if float(key) > resolution]

