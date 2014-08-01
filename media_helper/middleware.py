from django.http import HttpResponseRedirect
from django.conf import settings
from media_helper.settings import Settings
from media_helper.resizer import resize

# TODO:  Make redirect prevention more robust to avoid naming conflicts with other apps

class InterceptMediaRequest(object):
    ''' Incercepts and potentially redirects all requests made to the media server.   

    '''
    def process_response(self, request, response):
        import re
        import os

        # Only intercepts media requests 
        if request.path.startswith(settings.MEDIA_URL):
            media_helper_settings = Settings()
            
            try:
                folder = request.session['width']
            except:
                folder = str(media_helper_settings.default)
            
            # The MEDIA_URL needs to be removed from the request so both a new request
            # and file path can be created.
            redirect_path = request.path[len(settings.MEDIA_URL):].strip('/').split('/')
            
            # This prevents redirect loops. But it also assumes no upload folders or any other
            # folder created by an app use the same naming convention.  This makes it 
            # incompatible with the resize template tag.
            if folder == redirect_path[0]:
                return response 
            
            redirect_path.insert(0, folder)
            system_path = os.path.join(settings.MEDIA_ROOT, *redirect_path)
            
            if os.path.isfile(system_path):   
                return HttpResponseRedirect(os.path.join(settings.MEDIA_URL, *redirect_path))
            else:                
                # extracts image name + upload folder from request path
                image_name = request.path.split(settings.MEDIA_URL)[-1].strip('/')
                image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                
                if os.path.isfile(image_path):
                    resize(settings.MEDIA_ROOT, folder, media_helper_settings.generate_scaling_factors()[folder], image_path)

        return response

