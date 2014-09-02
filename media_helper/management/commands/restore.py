import os
import shutil
from django.core.management.base import NoArgsCommand
#from media_helper.tools.resizers import restore
from media_helper.tools.helpers import construct_paths, check_encoding
from django.conf import settings as django_settings
from media_helper.settings import Settings

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        media_root = django_settings.MEDIA_ROOT
        if os.path.isdir(media_root):
            # The directory for the newly scaled images
            
            for path, dirs, files in os.walk(media_root):
                
                for file in files:
                    
                    
                    upload = path.split(media_root)[-1]
                    #upload = os.path.join(upload, file)
                    image_path = os.path.join(path, file)
                    paths = construct_paths(image_path)

                    if os.path.isfile(paths['backup_path']):
                        shutil.copy(paths['backup_path'], os.path.join(path, file))
                        print "restoring %s" % os.path.join(path, file)
                    else:
                        print "Skipping image.  No backup found: %s " % os.path.join(path, file)


                '''for file in files:
                    new_file = os.path.join(resize_dir, upload_dir, file)
                    
                    if not os.path.isfile(new_file):
                        image_path = os.path.join(subdir, file)
                        
                        resize(media_root, new_size.keys()[0], new_size.values()[0], image_path)
                '''
        else:
            print "Oh, oh.  Something went terribly wrong.  It seems your media root directory"\
                  "doesn't exist: %s" % settings.MEDIA_ROOT
            raise
