from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from core.models import Admin


class Command(BaseCommand):

    help = "Create the Sujatha admin account"

    def handle(self, *args, **kwargs):

        username = "Sujatha"
        password = "admin123"

        admin, created = Admin.objects.get_or_create(
            username=username,
            defaults={
                "password": make_password(password)
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Sujatha admin created successfully!"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Sujatha admin already exists."
                )
            )