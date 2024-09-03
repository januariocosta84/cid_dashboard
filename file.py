import django
from django.utils.timezone import make_aware
import datetime
import os

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CidProject.settings')

# Initialize Django
django.setup()

from cidApp.models import Audits

# Data integrity check
for audit in Audits.objects.all():
    if isinstance(audit.created_at, str):
        print(f"Audit ID {audit.id} has a string created_at")
    if isinstance(audit.updated_at, str):
        print(f"Audit ID {audit.id} has a string updated_at")

# Optionally, fix the issues
for audit in Audits.objects.all():
    if isinstance(audit.created_at, str):
        audit.created_at = make_aware(datetime.datetime.fromisoformat(audit.created_at))
    if isinstance(audit.updated_at, str):
        audit.updated_at = make_aware(datetime.datetime.fromisoformat(audit.updated_at))
    audit.save()