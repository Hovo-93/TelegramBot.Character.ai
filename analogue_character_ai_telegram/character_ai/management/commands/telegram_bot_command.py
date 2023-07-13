from django.core.management.base import BaseCommand
from character_ai.telegram_api import send_welcome


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_welcome()
        print('Completed')