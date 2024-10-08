import os
import requests
from datetime import datetime
import shutil
import logging
import urllib3
import ssl
from requests.auth import HTTPDigestAuth
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# Disable SSL warnings from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SSLAdapter(HTTPAdapter):
    """
    A custom adapter for handling SSL contexts with lower security levels.
    """
    def __init__(self, ssl_context=None, *args, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        """
        Initialize the pool manager with the custom SSL context.
        """
        context = self.ssl_context if self.ssl_context else ssl.create_default_context()
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=context
        )

class HotlinePulling:
    def __init__(self):
        self.api_url = 'https://10.10.0.20:8443/recapi'  # Use HTTPS
        self.api_user = 'cdrapi'
        self.api_pwd = 'cdrapi123'
        self.storage_dir = '/var/www/ciddash/hotline_api_py'  # Adjust as necessary
        self.api_path = 'voicemail'  # API path for pulling files
        self.api_extension = '5000'  # API extension, example value
        self.log_file_path = '/var/www/ciddash/hotline_api_py/log.txt'  # Path to log file
        self.new_voicemail_dir = '/var/www/ciddash/hotline_api_py/new_voicemail'  # New directory for voicemail files

        # Configure logging
        logging.basicConfig(filename=self.log_file_path, level=logging.INFO)

        # Create an SSL context to allow weaker DH keys and disable hostname checking
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')  # Allow weaker ciphers
        self.ssl_context.check_hostname = False  # Disable hostname checking
        self.ssl_context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

        # Create an HTTP session with the custom SSL context
        self.session = requests.Session()
        self.session.mount('https://', SSLAdapter(ssl_context=self.ssl_context))

        self.start_pulling()

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

                        file_downloaded_path = self.download_files(file['directory'], file['filename'], filename_with_extension)

                        if file_downloaded_path:
                            self.move_file_to_new_voicemail(file_downloaded_path, filename_with_extension)
                except Exception as e:
                    self.create_log(f"Error processing hotline {hotline['filename']}: {str(e)}")
        except Exception as e:
            self.create_log(f"Error starting hotline pulling: {str(e)}")

    def create_log(self, message):
        log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        logging.info(log_message)

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

    def get_hotline_files(self, array_file):
        file_dir = f"{self.api_path}/default/{array_file['filename']}/INBOX"

        response = self.get({'filedir': file_dir})
        content = response.text
        self.create_log(f'Get Hotlines Files: {content}')
        return self.format_response_body_contents(content)

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

    def get_storage_dir(self):
        folder = self.storage_dir.rstrip('\\')
        if not os.path.exists(folder):
            try:
                os.makedirs(folder, mode=0o755, exist_ok=True)
            except OSError as e:
                self.create_log(f'Error creating directory "{folder}"')
                raise RuntimeError(f'Directory "{folder}" was not created') from e
        return folder

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

# Instantiate the class to start pulling process
if __name__ == "__main__":
    downloader = HotlinePulling()
