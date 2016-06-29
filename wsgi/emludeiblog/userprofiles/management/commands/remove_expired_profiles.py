from django.core.management.base import BaseCommand

from userprofiles.models import User


class Command(BaseCommand):
    help = 'Remove expired profiles from database'

    def handle(self, *args, **options):
        User.delete_expired_profiles()
