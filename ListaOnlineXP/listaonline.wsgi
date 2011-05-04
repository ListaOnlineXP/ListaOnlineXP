#!/usr/bin/python
import os
import sys
path = '/www/ListaOnlineXP'
sys.path.append('/www')
sys.path.append('/www/ListaOnlineXP')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ListaOnlineXP.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
