import datetime
import time
import dfktools.quests.utils.utils as quest_utils
from math import floor

from definitions import ZERO_ADDRESS
from web.src.db.ORM.dfk_orm import Account, LocalHero
from web.src.db.db import dfk_session_creator
from web.src.db.query.accounts import get_accounts
from web.src.dfk_.heroes.hero import crystalvale_heroes
from web.src.static.loggers import logger
from dfktools.quests.professions.mining import CRYSTALVALE_GOLD_QUEST_CONTRACT_ADDRESS
from web.src.dfk_.quest import questV3


def get_current_timestamp() -> int:
    return int(datetime.datetime.now().timestamp())


def is_hero_questing(hero: LocalHero) -> bool:
    return hero.current_quest != ZERO_ADDRESS


def is_quest_finished(hero: LocalHero) -> bool:
    return get_current_timestamp() > hero.quest_end_time


def get_hero_from_id(hero_id: int) -> LocalHero:
    with dfk_session_creator() as session:
        return session.query(LocalHero).filter(LocalHero.hero_id == hero_id).first()


def get_account_hero_ids(account: Account) -> [int]:
    return [h.dfk_hero_id for h in _get_account_heroes(account)]


def get_account_heroes(account: Account) -> [LocalHero]:
    return [h for h in _get_account_heroes(account)]


def get_account_hero_idle_status(account: Account) -> bool:
    return all([h.current_quest == ZERO_ADDRESS for h in _get_account_heroes(account)])


def get_account_full_stamina_status(account: Account) -> bool:
    return all([h.is_full_stamina for h in _get_account_heroes(account)])


def get_lowest_hero_stamina(account: Account) -> int:
    return min([h.maximum_stamina for h in _get_account_heroes(account)])


def _get_account_heroes(account: Account) -> [LocalHero]:
    with dfk_session_creator() as session:
        heroes = session.query(Account, LocalHero).filter(Account.account_id == LocalHero.account_id).filter(Account.account_id == account.account_id).\
            filter(LocalHero.account_id == account.account_id).all()
        return [h for a, h in heroes]


def _is_full_stamina(h: {}):
    return floor(time.time()) >= h['state']['staminaFullAt']


def _hero_dict_to_hero(h: {}, account_id: int) -> LocalHero:
    return LocalHero(dfk_hero_id=h['id'], account_id=account_id,
                     maximum_stamina=h['stats']['stamina'], is_full_stamina=_is_full_stamina(h),
                     current_xp=h['state']['xp'], level=h['state']['level'],
                     current_quest=h['state']['currentQuest'])


def set_hero_data(hero_dict: {}, account_id: int) -> None:
    with dfk_session_creator() as session:

        hero_id = hero_dict['id']
        new_hero = _hero_dict_to_hero(hero_dict, account_id)
        existing_hero = session.query(LocalHero).filter(LocalHero.dfk_hero_id == hero_id).first()
        hero = existing_hero if existing_hero else new_hero

        hero.maximum_stamina = new_hero.maximum_stamina
        hero.level = new_hero.level
        hero.current_xp = new_hero.current_xp
        hero.is_full_stamina = new_hero.is_full_stamina

        quest_info = quest_utils.human_readable_quest(questV3.get_hero_quest(hero_id))

        if quest_info:
            hero.current_quest = quest_info['type']
            hero.quest_start_time = quest_info['startTime']
            hero.quest_end_time = quest_info['completeAtTime']
        else:
            hero.current_quest = ZERO_ADDRESS
            hero.quest_start_time = 0
            hero.quest_end_time = 0

        session.add(hero)
        session.commit()

        return hero


def clear_hero_data() -> None:
    logger.info('Clearing hero data')
    with dfk_session_creator() as session:
        session.query(LocalHero).delete()
        session.commit()


def set_account_hero_data(account: Account) -> [int]:
    public_address = account.public_address
    for hid in crystalvale_heroes.get_users_heroes(public_address):
        logger.debug('Setting hero data for ID : %d' % hid)
        hero = crystalvale_heroes.get_hero(hid)
        set_hero_data(hero, account.account_id)


def set_all_account_hero_data() -> None:
    for account in get_accounts():
        logger.debug("Setting account hero data")
        set_account_hero_data(account)


def get_mining_hero_ids(account: Account):
    return [h.dfk_hero_id for h in _get_account_heroes(account) if h.current_quest == 'Gold Mining']


