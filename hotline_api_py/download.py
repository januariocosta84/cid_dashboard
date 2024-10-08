import paramiko
from scp import SCPClient
import os

# SSH and SCP connection details
hostname = "10.10.11.106"  # IP address of the remote server
username = "ifmisu"          # Username for the server
password = "P@ssw0rd"          # Password for the server (or use key authentication)
remote_path = "/var/www/ciddash/hotline_api_py/"
local_path = r"C:\\Users\\TGA\\OneDrive - IBI\\Desktop"  # Destination on Windows

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the remote server
    ssh.connect(hostname, username=username, password=password)
    
    # Use SCP to copy files
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(remote_path, local_path=local_path, recursive=True)  # Download directory recursively
    
    print(f"Files downloaded successfully to {local_path}")

except Exception as e:
    print(f"Error: {e}")

finally:
    ssh.close()
