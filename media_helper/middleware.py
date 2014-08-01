from django.http import HttpResponseRedirect
from django.conf import settings
from media_helper.settings import Settings
from media_helper.resizer import resize



class InterceptMediaRequest(object):
    '''
    Incercepts all requests made to the media server and inserts the appropriate 
    folder according to screen size and aspect ratio.
    '''
    def process_response(self, request, response):
        import re
        import os

        # Only intercepts media requests 
        if request.path.startswith(settings.MEDIA_URL):
            media_helper_settings = Settings()        
            file_name = request.path.split('/')[-1]
            
            try:
                folder = request.session['width']
            except:
                folder = str(media_helper_settings.default)
            
            # [1:] in case PROJECT_PATH isn't defined, it will not duplicate the 
            # MEDIA_URL in the path
            # [1:] is used because 
            root = set(settings.MEDIA_ROOT.strip('/').split('/'))
            url =  set(request.path.strip('/').split('/'))
            diff = list(root & url)

            new_request_path = request.path.strip('/').split('/')[1:]


            if folder in new_request_path:
                return response 
            
            new_request_path.insert(0, folder)  # This will be the redirect path 
            
            system_path = os.path.join(settings.MEDIA_ROOT, *new_request_path)
            
            if os.path.isfile(system_path):   
                return HttpResponseRedirect(os.path.join(settings.MEDIA_URL, *new_request_path))
            else:
                # Resizes image
                
                # extracts image name + upload folder from request path
                image_name = request.path.split(settings.MEDIA_URL)[-1].strip('/')
                image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                
                if os.path.isfile(image_path):
                    resize(settings.MEDIA_ROOT, folder, media_helper_settings.generate_scaling_factors()[folder], image_path)

            return response

        return response

    def append_to_session(self, request, file_name):
        if request.session.get('redirected_files') is not None and request.session.get('redirected_files') != []:
                request.session['redirected_files'].append(file_name)
        else:
            request.session['redirected_files'] = [file_name, ]

