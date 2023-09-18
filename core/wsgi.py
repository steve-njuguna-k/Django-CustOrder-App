"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.contrib.auth.models import User
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

users = User.objects.all()
if not users:
    User.objects.create_superuser(username=os.environ.get("DJANGO_SUPERUSER_USERNAME"), email=os.environ.get("DJANGO_SUPERUSER_EMAIL"), password=os.environ.get("DJANGO_SUPERUSER_PASSWORD"), is_active=True, is_staff=True)