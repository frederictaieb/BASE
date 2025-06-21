from app.models.client import Client
from app.services.xrp.wallet import create_wallet
from app.services.ipfs.upload import upload_file
from xrpl.wallet import Wallet
import dotenv
import os
import logging
from app.utils.logger import logger_init

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)
dotenv.load_dotenv()

class Player(Client):
    def __init__(self, username: str, wallet: Wallet, ipfs_images: list[str] = None):
        super().__init__(username)
        self.wallet = wallet
        self.ipfs_images = ipfs_images or []
        logger.info(f"Player {self.username} created with wallet {self.wallet.address}")

    @classmethod
    async def create(cls, username: str):
        wallet = await create_wallet()
        return cls(username, wallet)

    def get_wallet_address(self):
        return self.wallet.address

    def add_ipfs_image(self, image_path: str):
        ipfs_url = os.getenv("IPFS_URL")
        img_ipfs_url = upload_file(ipfs_url, image_path)
        self.ipfs_images.append(img_ipfs_url)
        logger.info(f"Image {image_path} uploaded to IPFS {img_ipfs_url}")

    def get_last_image(self) -> str | None:
        if self.ipfs_images:
            return self.ipfs_images[-1]
        return None

    def get_all_images(self) -> list[str]:
        return self.ipfs_images.copy()

    def clear_images(self):
        self.ipfs_images.clear()

    def __repr__(self):
        return f"<Player(username={self.username}, wallet={self.wallet.address}, images={len(self.ipfs_images)})>"