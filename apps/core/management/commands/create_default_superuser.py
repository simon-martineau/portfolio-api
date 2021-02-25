import os

from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    """Django command to add a default superuser"""

    def handle(self, *args, **options):

        try:
            email = os.environ['DJANGO_SUPERUSER_EMAIL']
            password = os.environ['DJANGO_SUPERUSER_PASSWORD']
        except KeyError:
            self.stderr.write("DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD environment variables are absent")
            return

        self.stdout.write("Testing if superuser exists")
        exists = User.objects.filter(email=email).exists()

        if exists:
            self.stdout.write("User already exists, exiting")
        else:
            self.stdout.write(f"Creating user with email <{email}>")
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS('User created successfully'))
