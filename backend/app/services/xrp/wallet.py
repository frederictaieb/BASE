from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
from xrpl.utils import drops_to_xrp 
from app.utils.logger import logger_init
import logging


logger_init()
logger = logging.getLogger(__name__) 



def create_wallet():
    from xrpl.wallet import generate_faucet_wallet
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)
    wallet = generate_faucet_wallet(client)
    logger.info(f"Wallet created: {wallet}")
    return wallet

def get_xrp_balance(wallet_address):
    from xrpl.clients import JsonRpcClient
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
    client = JsonRpcClient(JSON_RPC_URL)
    req = AccountInfo(account=wallet_address, ledger_index="validated", strict=True)
    response = client.request(req)
    logger.info(f"Balance: {response.result['account_data']['Balance']}")
    return drops_to_xrp(response.result['account_data']['Balance'])
