import os
from datetime import datetime
from django.utils.dateparse import parse_datetime
from cidApp.models import Hotline

def process_and_insert_new_hotlines(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)

            # Generate .wav file path and file name
            wav_filepath = filepath.replace(".txt", ".wav")
            wav_filename = filename.replace(".txt", ".wav")
            
            # Check if the file_path already exists in the Hotline model
            if Hotline.objects.filter(file_path=wav_filepath).exists():
                print(f"File {wav_filename} already processed. Skipping.")
                continue  # Skip this file if it has already been processed
            
            # If not processed, proceed to extract origdate and insert new record
            origdate = None
            with open(filepath, 'r') as file:
                for line in file:
                    if line.startswith("origdate="):
                        origdate_str = line.split('=', 1)[1].strip()
                        # Parse the extracted date into a datetime object
                        origdate = parse_datetime(origdate_str)
                        if not origdate:
                            # Try parsing it as a regular datetime
                            origdate = datetime.strptime(origdate_str, "%a %b %d %I:%M:%S %p %Z %Y")
                        break
            
            # Insert the new record into the Hotline model
            hotline = Hotline(
                type="hotline",  # Update this with your desired type value
                file_path=wav_filepath,
                file=wav_filename,
                origin_date=origdate
            )
            hotline.save()
            print(f"Inserted new hotline for file {wav_filename} with origdate {origdate}")

# Example usage
directory = "/path/to/your/txt/files"  
process_and_insert_new_hotlines(directory)
