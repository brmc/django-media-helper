import os
import shutil
from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings as django_settings
from media_helper.tools.resizers import resize, move_original, resize_original
from media_helper.tools.helpers import construct_paths, check_encoding

from media_helper.settings import Settings


class Command(NoArgsCommand):
    help = 'This command restores the original images found in the media-helper' \
        'sub directory to their native path and then deletes the backup.  All '\
        'other images remain intact.  This means that the full-sized image will'\
        'be delivered when the page is loaded.'

    option_list = NoArgsCommand.option_list + (
        make_option('--restore',
            action='store_true',
            dest='restore',
            default=False,
            help='This command restores the original images found in the media-helper' \
                'sub directory to their native path and then deletes the backup.  All '\
                'other images remain intact.  This means that the full-sized image will'\
                'be delivered when the page is loaded.'),
        ) + (
        make_option('--resize-all',
            action='store_true',
            dest='resize-all',
            default=False,
            help='Resizes all allowed images in MEDIA_ROOT.'),
        ) + (make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Restores the original images then deletes the media-helper dir.'),
        ) + (make_option('--resize-originals',
            action='store_true',
            dest='resize-originals',
            default=False,
            help='Use this when you want to change the quality and/or size of the place holder images'),
        ) 

    def handle_noargs(self, **options):
        # counters
        if options['delete']:
            resize_all = options['resize-all']
            resize_originals = options['resize-originals']
            restore = options['restore']

            options['resize-all'] = options['resize-originals'] = False

            # Force restoring backups while temporarily disabling resizing
            options['restore'] = True
            self.traverse_media_root(**options)
           
            # Returning original state
            options['resize-all'] = resize_all
            options['resize-originals'] = resize_originals
            # except for restore which doesn't need to be called again
            options['restore'] = False
            try:
                shutil.rmtree(os.path.join(django_settings.MEDIA_ROOT, 'media-helper'))
                if options['verbosity'] > '0':
                    self.stdout.write('All resized images deleted.')
            except OSError:
                self.stdout.write("Media-helper directory doesn't exist.")
            

        if options['restore'] or options['resize-originals'] or options['resize-all']:
            self.traverse_media_root(**options)
            
        '''
        if options['delete']:
            resize = options['resize-all']
            # Force restoring backups while temporarily disabling resizing
            options['resize-all'], options['restore'] = False, True
            self.traverse_media_root(**options)
            # Returning 
            options['resize-all'] = resize

            shutil.rmtree(os.path.join(django_settings.MEDIA_ROOT, 'media-helper'))

        if options['resize-all']:    
            self.traverse_media_root(**options)
        '''
        

    def restore(self, original_path, backup_path, **options):
        if os.path.isfile(backup_path):
            shutil.copy(backup_path, original_path)
            # os.remove(backup_path)
            # paths['image_name'] is used instead of `file` because it includes
            # the upload_to directory
            if options['verbosity'] > '1':
                self.stdout.write("restoring %s" % original_path)
            return True
        else:
            if options['verbosity'] > '1':
                self.stdout.write("Skipping %s:  No backup found. " % original_path)
            return False

    def traverse_media_root(self, **options):
        # counters
        skipped = restored = resized = 0
        media_root = django_settings.MEDIA_ROOT
        media_helper_root = construct_paths("")['media_helper_root']

        if os.path.isdir(media_root):
            for path, dirs, files in os.walk(media_root, topdown = True):
                if 'media-helper' in dirs:
                    dirs.remove('media-helper')
                dirs[:] = [d for d in dirs if d is not 'media-helper']
                
                for file in files:
                    image_path = os.path.join(path, file)
                    paths = construct_paths(image_path)
                    
                    if options['restore']:
                        if self.restore(image_path, paths['backup_path'], **options):
                            restored += 1
                        else:
                            skipped += 1
                    if options['resize-originals']:
                        if resize_original(image_path, paths['backup_path']):
                            if options['verbosity'] > '0':
                                self.stdout.write('Resizing %s' % image_path)

                    if options['resize-all']:
                        if self.resize_all(image_path, **options):
                            resized += 1
                        else:
                            skipped += 1
        else:
            raise CommandError("Oh, oh.  Something went terribly wrong.  It seems your media root directory"\
                  "doesn't exist: %s" % settings.MEDIA_ROOT)

        if options['verbosity'] > '0':
                if options['restore']:
                    self.stdout.write("%d file(s) restored.\n%d file(s) resized.\n%d file(s) skipped" % (restored, resized, skipped))
        
    def resize_all(self, image_path, **options): 
        from PIL import Image
        
        if os.path.isfile(image_path):
            try:
                image = Image.open(image_path)
                width, height = image.size
                del image
            except IOError:
                return False
        else:
            return False

        try:
            if options['verbosity'] > '0':
                self.stdout.write("Backing up and creating placeholder for %s " % image_path)
            
            backup_path = move_original(image_path)

            for size in Settings().sizes:
                # scale width
                new_size = int(size * width)
                
                if options['verbosity'] > '1':
                    self.stdout.write("Resizing %s to %dpx wide" % (image_path, new_size))
                resize(image_path, new_size)

            if backup_path:
                resize_original(image_path, backup_path)
       
        except:
            raise
        return True

