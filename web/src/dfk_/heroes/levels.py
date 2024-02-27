import time

from definitions import XP_INTERVALS, GAS_PRICE_GWEI, DFK_CHAIN_RPC
from web.src.db.ORM.dfk_orm import Account
import dfktools.meditation.meditation as meditation

from web.src.disc.webhook import send_discord_message
from web.src.encrypt.encrypt import decrypt_bytes
from web.src.static.loggers import logger
from web.src.w3_ import w3


def xp_to_level(xp: int) -> int:
    if xp < XP_INTERVALS[0]:
        return 1

    for i, interval in enumerate(XP_INTERVALS):
        if xp <= interval:
            return i + 2


def at_level_cap(level: int, xp: int) -> bool:
    return xp in XP_INTERVALS and level == XP_INTERVALS.index(xp) + 1


def get_required_runes(hero_level: int) -> int:
    return sum(meditation.get_required_runes(contract_address=meditation.CRYSTALVALE_CONTRACT_ADDRESS,
                                             level=hero_level, rpc_address=DFK_CHAIN_RPC))


def get_required_jewel(hero_level: int) -> float:
    return hero_level*0.1


def level_up_hero(account: Account, hero_id: int):

    logger.info('Leveling up hero with ID %d for account %s' % (hero_id, account.public_address))
    account_private_key = decrypt_bytes(account.private_key)

    try:
        meditation.start_meditation(meditation.CRYSTALVALE_CONTRACT_ADDRESS, hero_id, 'strength', 'endurance', 'luck',
                                    meditation.ZERO_ADDRESS, account_private_key,
                                    w3.eth.get_transaction_count(account.public_address),
                                    GAS_PRICE_GWEI, 30, DFK_CHAIN_RPC, logger)
    except Exception as e:
        logger.critical('Exception on starting meditation : %s' % str(e))
        send_discord_message("Failed to start level up for hero : %s" % str(e))
        return

    time.sleep(20)

    try:
        meditation.complete_meditation(meditation.CRYSTALVALE_CONTRACT_ADDRESS,
                                       hero_id, account_private_key, w3.eth.get_transaction_count(account.public_address),
                                       GAS_PRICE_GWEI, 30, DFK_CHAIN_RPC, logger)
    except Exception as e:
        logger.critical('Exception on ending meditation : %s' % str(e))
        send_discord_message("Failed to finish level up for hero : %s" % str(e))

