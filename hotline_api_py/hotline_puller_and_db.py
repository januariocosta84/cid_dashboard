import os
import time
import requests
import shutil
import logging
import ssl
import mysql.connector
from datetime import datetime
from requests.auth import HTTPDigestAuth
from requests.adapters import HTTPAdapter
#from apscheduler.schedulers.blocking import BlockingScheduler

# Disable SSL warnings to avoid warnings about unverified HTTPS requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Custom HTTPAdapter to use a specific SSL context
class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

# Main class for pulling voicemails
class HotlinePulling:
    def __init__(self):
        # Configuration for API and directories
        self.api_url = 'https://10.10.0.20:8443/recapi'  # Use HTTPS
        self.api_user = 'cdrapi'
        self.api_pwd = 'cdrapi123'
        self.storage_dir = 'C:\\Users\\TGA\\OneDrive - IBI\\Desktop\\hotline_api_py'  # Directory to save downloaded files
        self.api_path = 'voicemail'  # API path for pulling files
        self.api_extension = '5000'  # API extension, example value
        self.log_file_path = 'C:\\Users\\TGA\\OneDrive - IBI\\Desktop\\hotline_api_py\\log.txt'  # Path to log file
        self.new_voicemail_dir = 'C:\\Users\\TGA\\OneDrive - IBI\\Desktop\hotline_api_py\\new_voicemai'  # Directory for new voicemails

        # Configure logging to write to the specified log file
        logging.basicConfig(filename=self.log_file_path, level=logging.INFO)

        # Create an SSL context to allow weaker DH keys and disable hostname checking
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        # Create an HTTP session with the custom SSL context
        self.session = requests.Session()
        self.session.mount('https://', SSLAdapter(ssl_context=self.ssl_context))

        # Initialize a set to track existing voicemails
        self.existing_voicemails = set()

        # Start the periodic execution
        #self.run_periodically()

    # Function to set up a scheduler to run the script every hour
    # def run_periodically(self):
    #     scheduler = BlockingScheduler()
    #     scheduler.add_job(self.start_pulling, 'interval', hours=1)
    #     scheduler.start()

    # Main function to pull data from the voicemail machine
    def start_pulling(self):
        try:
            self.create_log('Starting to pull data.')
            hotlines = self.get_hotlines()

            for hotline in hotlines:
                try:
                    files = self.get_hotline_files(hotline)

                    for file in files:
                        if not file['filename'] or not file['directory']:
                            self.create_log(f"Invalid file or directory for hotline {hotline['filename']}")
                            continue

                        filename_with_extension = f"{datetime.now().strftime('%y')}_{file['filename']}"
                        filename = f"{datetime.now().strftime('%y')}_{os.path.splitext(file['filename'])[0]}"

                        # Check if the voicemail has already been processed
                        if filename in self.existing_voicemails:
                            continue

                        file_downloaded_path = self.download_files(file['directory'], file['filename'], filename_with_extension)

                        if file_downloaded_path:
                            self.move_file_to_new_voicemail(file_downloaded_path, filename_with_extension)
                            self.existing_voicemails.add(filename)
                            self.insert_into_database(file_downloaded_path, filename_with_extension)
                except Exception as e:
                    self.create_log(f"Error processing hotline {hotline['filename']}: {str(e)}")
        except Exception as e:
            self.create_log(f"Error starting hotline pulling: {str(e)}")

    # Function to log messages to the specified log file
    def create_log(self, message):
        log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        logging.info(log_message)

    # Function to make GET requests to the API
    def get(self, query=None):
        try:
            if query is None:
                query = {}
            response = self.session.get(self.api_url, params=query, auth=HTTPDigestAuth(self.api_user, self.api_pwd), verify=False)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.create_log(f"GET request failed: {str(e)}")
            raise e

    # Function to get the list of hotlines/extensions
    def get_hotlines(self):
        self.create_log('Get Hotlines Extensions')

        response = self.get({'filedir': self.api_path})
        content = response.text
        all_extensions = self.format_response_body_contents(content)

        self.create_log(f'Found Extensions: {all_extensions}')

        extensions = []
        if self.api_extension:
            filter_extensions = [ext.strip() for ext in self.api_extension.split(',')]

            self.create_log(f'Filtering extensions by: {filter_extensions}')
            
            for extension in all_extensions:
                filename = extension['filename'].strip().lower()
                if filename in filter_extensions:
                    extensions.append(extension)
        else:
            extensions = all_extensions

        self.create_log(f'Extensions to be processed: {extensions}')

        return extensions

    # Function to get the list of files for a specific hotline/extension
    def get_hotline_files(self, array_file):
        file_dir = f"{self.api_path}/default/{array_file['filename']}/INBOX"
        
        response = self.get({'filedir': file_dir})
        content = response.text
        
        self.create_log(f'Get Hotlines Files: {content}')
        return self.format_response_body_contents(content)
    # Function to parse the response body and format it into a list of dictionaries
    def format_response_body_contents(self, content):
        csv = content.strip().split('\n')
        if csv:
            csv.pop(0)  # Assuming first line is headers, remove if not needed

        formatted_array = []
        for item in csv:
            parts = item.split(',')
            formatted_array.append({
                'filename': parts[1] if len(parts) > 1 else 'default_filename',
                'directory': parts[0]
            })

        return formatted_array

    # Function to download files from the voicemail machine
    def download_files(self, directory, filename, disk_name):
        query = {
            'filedir': directory,
            'filename': filename,
        }

        storage_dir = self.get_storage_dir()
        dir_path = os.path.join(storage_dir, directory)

        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, mode=0o755, exist_ok=True)
            except OSError as e:
                self.create_log(f"Error creating folder: {dir_path}")
                return None

        file_path = os.path.join(dir_path, disk_name)
        try:
            with self.session.get(self.api_url, params=query, auth=HTTPDigestAuth(self.api_user, self.api_pwd), verify=False, stream=True) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        except requests.RequestException as e:
            self.create_log(f"Failed to download file: {file_path}. Error: {str(e)}")
            return None

        self.create_log(f"Downloaded file: {file_path}")
        return file_path

    # Function to get the storage directory, creating it if necessary
    def get_storage_dir(self):
        folder = self.storage_dir.rstrip('\\')
        if not os.path.exists(folder):
            try:
                os.makedirs(folder, mode=0o755, exist_ok=True)
            except OSError as e:
                self.create_log(f'Error creating directory "{folder}"')
                raise RuntimeError(f'Directory "{folder}" was not created') from e
        return folder

    # Function to move the downloaded file to the new voicemail directory
    def move_file_to_new_voicemail(self, file_path, filename):
        if not os.path.exists(self.new_voicemail_dir):
            try:
                os.makedirs(self.new_voicemail_dir, mode=0o755, exist_ok=True)
            except OSError as e:
                self.create_log(f"Error creating folder: {self.new_voicemail_dir}")
                return

        new_file_path = os.path.join(self.new_voicemail_dir, filename)
        try:
            shutil.move(file_path, new_file_path)
            self.create_log(f"Moved file to: {new_file_path}")
        except OSError as e:
            self.create_log(f"Failed to move file to: {new_file_path}")

    # Function to insert the voicemail metadata into the database
    def insert_into_database(self, file_path, filename):
        # Parse the metadata from the associated txt file
        metadata_file = file_path.replace('.wav', '.txt')
        created_at = None
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                for line in f:
                    if line.startswith('origdate='):
                        created_at = line.split('=')[1].strip()
                        break

        if created_at is None:
            self.create_log(f"Metadata file {metadata_file} does not contain creation date.")
            return
        print("File path", file_path)
        try:
            # Connect to the MySQL database
            db_connection = mysql.connector.connect(
                host="localhost",
                user="cid_user",
                password="CID_2024!",
                database="cid"
            )
            cursor = db_connection.cursor()
            
            # SQL query to insert the voicemail metadata into the database
            insert_query = """
                INSERT INTO cidapp_hotline (type, file_path, file, created_at, modify_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            current_time = datetime.now().strftime('%H:%M:%S.%f')
            cursor.execute(insert_query, ("Hotline", file_path, filename, created_at, current_time))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            self.create_log(f"Inserted {filename} into database.")
        except mysql.connector.Error as err:
            self.create_log(f"Error inserting into database: {err}")

# Instantiate the class to start the pulling process
downloader = HotlinePulling()
