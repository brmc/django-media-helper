import os
import shutil
from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings as django_settings
from media_helper.tools.resizers import resize, resize_original
from media_helper.tools.helpers import construct_paths
from media_helper import settings


class Command(NoArgsCommand):
    help = 'This command is used to retrofit the media_helper app into a ' \
    'project that \nalready exists. With it you can resize all images found ' \
    'in the MEDIA_ROOT \ndirectory, resize/adjust the quality of the ' \
    'placeholder image, delete all \nresized images, and/or restore images ' \
    'to their original size, quality and \nlo' \
    'cation.  If all command options '\
    'are used simultaneously, they will be \nprocessed in the following ' \
    'order:\n   --restore\n   --delete\n   --resize-originals\n' \
    '   --resize-all\n\nAnd note that whenever --delete is pass, ' \
    "--restore will be forced so you don't risk losing your original " \
    'images.' \

    option_list = NoArgsCommand.option_list + (
        (make_option(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Restores the original images and deletes the media-helper '
                'directory tree.'),) +
        (make_option(
            '--resize',
            dest='resize',
            default=False,
            metavar="FILE",
            help='Resizes a specific image. Include the upload_to directory '
                'where applicable.  (e.g., --resize=images/donkey.jpg)'),) +
        (make_option(
            '--resize-all',
            action='store_true',
            dest='resize-all',
            default=False,
            help='Resizes all allowed images in MEDIA_ROOT.'),) +
        (make_option(
            '--resize-originals',
            action='store_true',
            dest='resize-originals',
            default=False,
            help='Use this when you want to change the quality and/or size of '
                'the place holder images'),) +
        (make_option(
            '--restore',
            action='store_true',
            dest='restore',
            default=False,
            help='Restores the original images found in the media-helper '
                'sub directory to their native path and then deletes the '
                'backup.  All other images remain intact.  This means that '
                'the full-sized image will be delivered when the page is '
                'loaded.'),)
    )





    def handle_noargs(self, **options):
        # counters
        if options['delete']:
            resize_all = options['resize-all']
            resize_originals = options['resize-originals']

            options['resize-all'] = options['resize-originals'] = False

            # Force restoring backups while temporarily disabling resizing
            options['restore'] = True
            self.traverse_media_root(**options)

            # Returning original state...
            options['resize-all'] = resize_all
            options['resize-originals'] = resize_originals
            # ...except for restore which doesn't need to be called again
            options['restore'] = False
            try:
                shutil.rmtree(
                    os.path.join(django_settings.MEDIA_ROOT, 'media-helper'))
                if options['verbosity'] > '0':
                    self.stdout.write('All resized images deleted.')
            except OSError:
                self.stdout.write("Media-helper directory doesn't exist.")

        if (options['restore'] or
            options['resize-originals'] or
            options['resize-all']):
                self.traverse_media_root(**options)
        if (options['resize']):
            self.auto_resize(options['resize'], **options)

    def restore(self, original_path, backup_path, **options):
        ''' Copies original.jpg from media-helper to its original location '''
        if os.path.isfile(backup_path):
            shutil.copy(backup_path, original_path)
            # paths['image_name'] is used instead of `file` because it includes
            # the upload_to directory
            if options['verbosity'] > '1':
                self.stdout.write("restoring %s" % original_path)
            return True
        else:
            if options['verbosity'] > '1':
                self.stdout.write(
                    "Skipping %s:  No backup found. " % original_path)
            return False

    def traverse_media_root(self, **options):
        # counters for stats
        skipped = restored = resized = 0
        media_root = django_settings.MEDIA_ROOT

        if os.path.isdir(media_root):
            for path, dirs, files in os.walk(media_root, topdown=True):
                # Exclude media-helper directory
                if 'media-helper' in dirs:
                    dirs.remove('media-helper')

                dirs[:] = [d for d in dirs if d is not 'media-helper']
                for file in files:
                    image_path = os.path.join(
                        path.decode('utf-8'), file.decode('utf-8'))
                    paths = construct_paths(image_path)

                    if options['restore']:
                        if self.restore(
                            image_path, paths['backup_path'], **options):
                            restored += 1
                        else:
                            skipped += 1
                    if options['resize-originals']:
                        if resize_original(image_path, paths['backup_path']):
                            resized += 1
                            if options['verbosity'] > '0':
                                self.stdout.write('Resizing %s' % image_path)
                        else:
                            skipped += 1

                    if options['resize-all']:
                        if self.auto_resize(image_path, **options):
                            resized += 1
                        else:
                            skipped += 1
        else:
            raise CommandError("Oh, oh.  Something went terribly wrong.  It "
                               "seems your media root directory doesn't exist:"
                               "%s" % django_settings.MEDIA_ROOT)

        if options['verbosity'] > '0':
            self.stdout.write(
                "%d file(s) restored.\n%d file(s) resized.\n%d file(s) skipped"
                % (restored, resized, skipped))

    def auto_resize(self, image_path, **options):
        ''' Resizes all images found in the media directory '''
        from PIL import Image

        paths = construct_paths(image_path)

        # Check for backup before resizing
        if os.path.isfile(paths['backup_path']):
            open_path = paths['backup_path']
        elif os.path.isfile(image_path):
            open_path = image_path
        else:
            return False

        try:
            image = Image.open(open_path)
            width, height = image.size
            del image
        except IOError:
            return False

        try:
            if options['verbosity'] > '0':
                self.stdout.write("Resizing %s " % image_path)

            for scaling_factor in settings.SIZES:
                new_size = int(scaling_factor * width)

                if options['verbosity'] > '1':
                    self.stdout.write(
                        "Resizing %s to %dpx wide" % (image_path, new_size))

                resize(image_path, new_size)
            return True

        except:
            raise
