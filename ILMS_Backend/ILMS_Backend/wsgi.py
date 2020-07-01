"""
WSGI config for ILMS_Backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/app/ILMS_Backend')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ILMS_Backend.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ILMS_Backend.settings'

application = get_wsgi_application()
