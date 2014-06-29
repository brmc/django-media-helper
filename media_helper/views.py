from django.shortcuts import get_object_or_404, get_list_or_404, render
#from django.template.defaultfilters import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from .resizer import get_sizes

def resolution(request):
    '''Sets new session variable based on resolution'''
    if request.is_ajax():
        resolution = int(request.POST['resolution'])
        folder = [key for key, val in get_sizes().iteritems() if float(key) > resolution]
        folder.sort()
        request.session['resolution'] = folder[0]
        return HttpResponse("ok")

    else:
        return HttpResponseForbidden()

    