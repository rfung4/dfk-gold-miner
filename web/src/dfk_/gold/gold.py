import time
from typing import Union

import dfktools.quests.utils.utils as quest_utils
from dfktools.quests import quest_core_v3
from web3.exceptions import ContractLogicError

from definitions import TRANSACTION_TIMEOUT, GAS_PRICE_GWEI
from web.src.db.ORM.dfk_orm import Account, LocalHero
from web.src.db.query.heroes import get_account_heroes
from web.src.dfk_.quest import questV3
from web.src.disc.webhook import send_discord_message
from web.src.encrypt.encrypt import decrypt_bytes
from web.src.static.loggers import logger
from web.src.w3_ import w3


def start_gold_quest(account: Account) -> Union[float, None]:

    public_address = account.public_address
    private_key = decrypt_bytes(account.private_key)

    heroes:  [LocalHero]= get_account_heroes(account)
    hero_ids = [h.dfk_hero_id for h in heroes]
    logger.info('Starting gold mining quest for heroes with ID : %s' % str(hero_ids))
    min_stam = min([20 + (h.level-1) for h in heroes])

    try:
        questV3.start_quest(quest_type=quest_core_v3.QUEST_TYPE_GOLD_MINING, hero_ids=hero_ids,
                            attempts=min_stam, level=0, quest_param=0,
                            private_key=private_key,
                            nonce=w3.eth.get_transaction_count(public_address), gas_price_gwei=GAS_PRICE_GWEI,
                            tx_timeout_seconds=TRANSACTION_TIMEOUT)

    except ContractLogicError as e:
        logger.error('Contract logic error on starting gold quest: %s' % str(e))
        logger.error(e)
        return None

    quest_info = quest_utils.human_readable_quest(questV3.get_hero_quest(hero_ids[0]))
    logger.info(quest_info)
    quest_completion_seconds = quest_info['completeAtTime'] - time.time()
    logger.info('%s seconds for mining quest to complete\n%s' % (str(quest_completion_seconds), str(quest_info)))

    return quest_completion_seconds


def complete_gold_quest(account: Account) -> bool:

    public_address = account.public_address
    private_key = decrypt_bytes(account.private_key)

    heroes = get_account_heroes(account)
    hero_ids = [h.dfk_hero_id for h in heroes]

    logger.info('Completing gold quest for account with address : %s' % public_address)

    try:
        tx = questV3.complete_quest(hero_ids[0], private_key,
                                    w3.eth.get_transaction_count(public_address), GAS_PRICE_GWEI, TRANSACTION_TIMEOUT)
        send_discord_message("Completed gold mine for account: %s" % account.public_address)

    except ContractLogicError as e:
        logger.error('Contract logic error on completing mining quest : %s' % str(e))
        return False

    return True


def cancel_gold_mine_quest(hero_ids: [int], public_address: str, private_key: str):
    try:
        tx = questV3.cancel_quest(hero_ids[0], private_key, w3.eth.get_transaction_count(public_address), GAS_PRICE_GWEI, TRANSACTION_TIMEOUT)
        logger.info('Cancelling gold quest for address : %s' % public_address)
    except ContractLogicError as e:
        logger.error('Contract logic error on cancelling mining quest : %s' % str(e))
        return False


# def resolve_gold_quests(cancel_quests: bool = True) -> None:
#     for account in get_accounts():
#         mining_hero_ids = get_mining_hero_ids(account)
#         logger.info("Got hero mining IDs : %s" % mining_hero_ids)
#
#         if len(mining_hero_ids):
#             logger.info('Got heroes mining : %s (%s) ' % (str(mining_hero_ids), account.public_address))
#
#             try:
#                 complete_gold_quest(mining_hero_ids, account.public_address, decrypt_bytes(account.private_key))
#                 logger.info('Completed gold quest for account : %s' % account.public_address)
#             except ContractLogicError:
#                 logger.info("Failed to complete gold quest")
#
#                 if cancel_quests:
#                     logger.info('Cancelling gold quest for account : %s' % account.public_address)
#                     result = cancel_gold_mine_quest(mining_hero_ids, account.public_address,
#                                                     decrypt_bytes(account.private_key))
#                     logger.info('Gold quest cancelled')