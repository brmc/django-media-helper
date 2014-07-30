from django.http import HttpResponseRedirect
from django.conf import settings
from media_helper.settings import MEDIA_HELPER_DEFAULT

class InterceptMediaRequest(object):
    '''
    Incercepts all requests made to the media server and inserts the appropriate 
    folder according to screen size and aspect ratio.
    '''
    def process_response(self, request, response):
        import re
        import os

        #pattern = r'<img.*src\s?=\s?"(\w*.(?:jpg|png|jpeg))"'
        print request.path
        #print response
        if request.path.startswith(settings.MEDIA_URL):

            if request.session.get('last_redirect') == None:
                print "poop"
                folder = str(MEDIA_HELPER_DEFAULT)
                path = request.path.split('/')
                path.insert(2, folder)
                path = "/".join(path[2:])
                b= os.path.join(settings.MEDIA_ROOT, path)
                print "pathasdf", path
                print os.path.isfile(b)
               
                if os.path.isfile(b):
                    print "yay@!"
                    request.session['last_redirect'] = True
                    return HttpResponseRedirect('/media/' +  path)

            else:
                request.session['last_redirect'] = None

        return response


"""from django.http import HttpResponseRedirect
from django.conf import settings

class InterceptMediaRequest(object):
    '''
    Incercepts all requests made to the media server and inserts the appropriate 
    folder according to screen size and aspect ratio.
    '''
    def process_response(self, request, response):
        import re
        pattern = r'<img.*src\s?=\s?"(\w*.(?:jpg|png|jpeg))"'

        #print response.content
        #c = re.findall(str(pattern), response.content, re.I)
        print "redirect:", request.session['last_redirect']
        if request.path.startswith(settings.MEDIA_URL):
            if request.session.get('last_redirect') == None:
                dir = '/1280/'
                b = request.path.split('/')
                print "aaaaa"
                c = "/" + b[1] + dir + "/".join(b[2:])
                request.session['last_redirect'] = b[-1]
                return HttpResponseRedirect(c)
            else:
                request.session['last_redirect'] = None

        return response


"""