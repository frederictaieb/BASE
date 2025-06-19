import os
import requests
from app.utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

def upload_file(url, file_path, timeout=10):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found : {file_path}")
    try:
        with open(file_path, 'rb') as file:
            logger.info(f"Uploading file to {url}")
            response = requests.post(
                f"{url.rstrip('/')}/api/v0/add",
                files={'file': file},
                timeout=int(timeout)
            )
        response.raise_for_status()
        data = response.json()
        return data['Hash']
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"IPFS Error (upload) : {e}")