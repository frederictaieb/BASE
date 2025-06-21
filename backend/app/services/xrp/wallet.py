# app/services/xrp/wallet.py

from xrpl.asyncio.wallet import generate_faucet_wallet
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models.requests import AccountInfo
from xrpl.utils import drops_to_xrp 
from app.utils.logger import logger_init
import logging
import os

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__) 

JSON_RPC_URL = os.getenv("XRP_RPC_URL", "https://s.altnet.rippletest.net:51234/")

async def create_wallet():
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = await generate_faucet_wallet(client)
    logger.info(f"Wallet created: {wallet}")
    return wallet

async def get_xrp_balance(wallet_address):
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    req = AccountInfo(account=wallet_address, ledger_index="validated", strict=True)
    response = await client.request(req)
    balance_drops = response.result["account_data"]["Balance"]
    logger.info(f"Balance: {balance_drops} drops")
    return drops_to_xrp(balance_drops)
