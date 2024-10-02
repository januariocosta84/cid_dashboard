from django.core.management.base import BaseCommand
from cidApp.models import WebForm, CallAndWebForm, Status
from cidApp.api_consuming import insert_subject  # Import your insert_subject function

class Command(BaseCommand):
    help = 'Fetch and insert subjects from API every 3 hours'

    def handle(self, *args, **kwargs):
        insert_subject()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and inserted subjects'))
