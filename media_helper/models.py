import django
from resizer import resize_signals
from cleanup import connect_signals

if django.VERSION < (1, 7):
    resize_signals()
    connect_signals()
