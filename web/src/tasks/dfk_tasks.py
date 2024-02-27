
from web.src.celery import celery
from web.src.db.ORM.dfk_orm import LocalHero
from web.src.db.query.accounts import get_accounts
from web.src.db.query.heroes import get_account_full_stamina_status, get_account_hero_idle_status, \
    set_all_account_hero_data, get_account_heroes, is_quest_finished
from web.src.dfk_.gold.gold import start_gold_quest, complete_gold_quest
from web.src.dfk_.heroes.levels import level_up_hero, at_level_cap, get_required_runes, get_required_jewel
from web.src.static.loggers import logger


@celery.task(name='dfk.quest.level-up')
def level_up_heroes():

    for account in get_accounts():
        if not get_account_hero_idle_status(account):
            logger.info("Heroes not idle")
            continue

        logger.info('Checking hero level status for account : %s' % account.public_address)
        heroes_to_level = [h for h in get_account_heroes(account) if at_level_cap(h.level, h.current_xp)]
        total_runes_required = sum([get_required_runes(h.level) for h in heroes_to_level])
        logger.info("Required total runes : %d" % total_runes_required)

        total_jewel_required = sum([get_required_jewel(hero_level=h.level) for h in heroes_to_level])
        logger.info("Total Jewel required : %d" % total_jewel_required)

        for hero in get_account_heroes(account):
            if at_level_cap(hero.level, hero.current_xp):
                level_up_hero(account, hero_id=hero.dfk_hero_id)


@celery.task(name='dfk.quest.gold-start', autoretry_for=(ValueError,), retry_kwargs={'max_retries': 3})
def start_gold_mine():
    for account in get_accounts():

        if not get_account_full_stamina_status(account):
            logger.info("Heroes not full stamina")
            continue

        if not get_account_hero_idle_status(account):
            logger.info("Heroes not idle")
            continue

        start_gold_quest(account)
        update_local_hero_data.subtask().apply_async()


@celery.task(name='dfk.quest.gold-end')
def end_gold_mine():

    for account in get_accounts():
        heroes: [LocalHero] = get_account_heroes(account)
        if get_account_hero_idle_status(account):
            continue

        if is_quest_finished(heroes[0]):
            complete_gold_quest(account)


@celery.task(name='dfk.hero-data-update')
def update_local_hero_data():
    set_all_account_hero_data()


@celery.task(name='dfk.periodic-tick')
def periodic_state_check():
    update_local_hero_data.subtask().apply_async()



