import os
import django
from django.utils import timezone
from datetime import datetime

# Initialize Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIDPROJECT.ciddApp.settings")
django.setup()

from cidApp.models import Hotline

def read_voicemail_info(file_paths):
    voicemail_data = []
    
    for file_path in file_paths:
        origdate = None
        duration = None
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('origdate='):
                    origdate = line.split('=')[1].strip()
                elif line.startswith('duration='):
                    duration = line.split('=')[1].strip()
        if origdate and duration:
            voicemail_data.append((file_path, origdate, duration))
    
    return voicemail_data

def read_directory_list(directory):
    path_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                path_files.append(os.path.join(root, file))
    return path_files

directory = '.'

path_files = read_directory_list(directory)

# Read voicemail information from the files
voicemail_info = read_voicemail_info(path_files)

# Insert records into the Hotline model
for info in voicemail_info:
    file_path, origdate, duration = info
    print(f"Inserting file: {file_path}")
    print(f"Original Date: {origdate}")
    print(f"Duration: {duration} seconds")

    # Convert origdate to datetime object
    try:
        created_at = datetime.strptime(origdate, "%a %b %d %H:%M:%S %Y")
    except ValueError:
        print(f"Error parsing date for file: {file_path}")
        continue

    # Create Hotline instance
    file_name = os.path.basename(file_path)
    hotline_instance = Hotline(
        type='voicemail',
        file_path=file_path,
        file=file_name,
        created_at=created_at,
        modify_at=timezone.now()
    )
    hotline_instance.save()

    print(f"Inserted: {hotline_instance}\n")
