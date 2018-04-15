#!/usr/bin/env python
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

def create_superuser():
    from django.contrib.auth.models import User

    username = "admin"
    password = "admin123"
    email = "controle.mapa@agricultura.gov.br"
    print("[SUPERUSER] Creating superuser...")

    u = User.objects.create_superuser(
        username=username, password=password, email=email)
    u.save()

    print("[SUPERUSER] Done.")

    sys.exit(0)


if __name__ == '__main__':
    django.setup()
    create_superuser()
