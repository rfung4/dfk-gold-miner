from dfktools.quests import quest_v3, quest_core_v3
from web.src.static.loggers import logger

crystalvale_rpc_server = 'https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'
CRYSTALVALE_CONTRACT_ADDRESS = '0xE9AbfBC143d7cef74b5b793ec5907fa62ca53154'
questV3 = quest_v3.Quest(quest_core_v3.CRYSTALVALE_CONTRACT_ADDRESS, crystalvale_rpc_server, logger)
