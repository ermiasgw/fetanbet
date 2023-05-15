"""
WSGI config for fetanbet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path
import sys
from django.core.wsgi import get_wsgi_application


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
