import os
import sys

path = '/home/efylan/projects/ccreservas/ccreservas'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ccreservas.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
