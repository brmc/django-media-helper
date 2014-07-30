from django.http import HttpResponseRedirect
from django.conf import settings
from media_helper.settings import MEDIA_HELPER_DEFAULT
from media_helper.resizer import get_sizes, resize

class InterceptMediaRequest(object):
    '''
    Incercepts all requests made to the media server and inserts the appropriate 
    folder according to screen size and aspect ratio.
    '''
    def process_response(self, request, response):
        import re
        import os
        # Only intercepts media requests 
        file_name = request.path.split('/')[-1]
        request.session['a'] = [1,2,3,]
        if request.path.startswith(settings.MEDIA_URL) and request.session.get('last_file_name') != file_name:
            request.session['last_file_name'] = file_name
            if request.session.get('requested') is not None:
                request.session['requested'].append(file_name)
            else:
                request.session['requested'] = [file_name, ]
            # Session variable to avoid redirect loops
        
            
            try:
                folder = request.session['width']
            except:
                folder = str(MEDIA_HELPER_DEFAULT)
            
            # [1:] in case PROJECT_PATH isn't defined, it will not duplicate the 
            # MEDIA_URL in the path
            new_request_path = request.path.strip("/").split('/')[1:]
            # This will be the redirect path 
            new_request_path.insert(0, folder)
            
            system_path = os.path.join(settings.MEDIA_ROOT, *new_request_path)
            print "system path", system_path
            print "is file", os.path.isfile(system_path) 
            if os.path.isfile(system_path):   
                print "last file name, ", request.session.get('last_file_name')
                return HttpResponseRedirect(os.path.join(settings.MEDIA_URL, *new_request_path))
            else:
                # Resizes image
                
                # extracts image name + upload folder from request path
                image_name = request.path.split(folder)[-1].strip('/')
                image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                
                if os.path.isfile(image_path):
                    print "resizing", image_path
                    resize(settings.MEDIA_ROOT, folder, get_sizes()[folder], image_path)
                    request.session['resized'] = True
                else:
                    request.session['resized'] = True

            return response
            
        return response

