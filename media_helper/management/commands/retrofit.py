from django.core.management.base import NoArgsCommand, CommandError
from media_helper.tools.resizers import resize_all
from django.conf import settings

class Command(NoArgsCommand):
    def handle_noargs(self, **options):