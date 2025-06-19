import requests
from app.utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


def download_file(url, cid, output_path="./", timeout=10):
    if not cid or not url:
        raise ValueError("Missing cid or url")
    try:
        url = f"{url.rstrip('/')}/ipfs/{cid}"
        logger.info(f"Downloading file from {url}")
        response = requests.get(url, timeout=int(timeout))
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"IPFS Error (download) : {e}")
