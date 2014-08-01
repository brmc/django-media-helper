from django.shortcuts import get_object_or_404, get_list_or_404, render
#from django.template.defaultfilters import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.conf import settings as dj_settings
from media_helper.settings import Settings
from .resizer import resize_all, resize

def resolution(request):
    '''Sets new session variable based on screen width'''
    if request.is_ajax():
        import os

        width = request.POST['width']
        new_path = os.path.join(dj_settings.MEDIA_ROOT, width)
        size = Settings().generate_scaling_factors([width,])
        
        if os.path.exists(new_path):
           pass
        else:
            resize_all(dj_settings.MEDIA_ROOT, width )
            
        request.session['width'] = width
        return HttpResponse("ok")

    else:
        return HttpResponseForbidden()

def insert_folder(width):
    '''Choses folder larger than width'''
    pass#return [key for key, val in get_sizes().iteritems() if float(key) > width]

