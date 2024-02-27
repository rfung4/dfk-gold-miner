import os

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

LOG_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'web/src/logs')
ERROR_LOG_PATH = os.path.join(LOG_DIRECTORY, 'error.log')
DEFAULT_LOG_PATH = os.path.join(LOG_DIRECTORY, 'default.log')
CRITICAL_LOG_PATH = os.path.join(LOG_DIRECTORY, 'critical.log')

PRIVATE_KEY_PATH = os.path.join(ROOT_DIRECTORY, 'private-key.pem')
PUBLIC_KEY_PATH = os.path.join(ROOT_DIRECTORY, 'public-key.pem')

DFK_CHAIN_RPC = 'https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
GOLD_MINING_ADDRESS = '0x75912145f5cFEfb980616FA47B2f103210FaAb94'

XP_INTERVALS = [2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]

TRANSACTION_TIMEOUT = 200
GAS_PRICE_GWEI = 20
MINUTE_PER_STAMINA = 20
