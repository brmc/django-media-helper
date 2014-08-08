import django
from django.db import models
from resizer import resize_signals
from cleanup import connect_signals

if django.VERSION < (1, 7):
    resize_signals()
    connect_signals()


class TestModel(models.Model):
    '''
    Only to be used for tests
    '''

    image = models.ImageField(upload_to="images")

class FakeModel(models.Model):
    '''
    Only to be used for tests
    '''

    image = models.FileField(upload_to="images")