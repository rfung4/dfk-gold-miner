
from web.src.celery import celery
from web.src.db.ORM.dfk_orm import LocalHero
from web.src.db.query.accounts import get_accounts
from web.src.db.query.heroes import get_account_full_stamina_status, get_account_hero_idle_status, \
    set_all_account_hero_data, get_account_heroes, is_quest_finished
from web.src.dfk_.gold.gold import start_gold_quest, complete_gold_quest
from web.src.dfk_.heroes.levels import level_up_hero, at_level_cap, get_required_runes, get_required_jewel
from web.src.disc.webhook import send_discord_message
from web.src.static.loggers import logger


# @celery.task(name='dfk.perioidic_miner_check')
# def miner_check():
#     resolve_gold_quests(cancel_quests=False)


@celery.task(name='dfk.quest.level-up')
def level_up_heroes():

    for account in get_accounts():
        if not get_account_hero_idle_status(account):
            logger.info("Heroes not idle")
            continue

        #if get_account_full_stamina_status(account):
            # Only level up heroes when NOT full stamina
        #    continue

        logger.info('Checking hero level status for account : %s' % account.public_address)

        heroes_to_level = [h for h in get_account_heroes(account) if at_level_cap(h.level, h.current_xp)]
        total_runes_required = sum([get_required_runes(h.level) for h in heroes_to_level])
        logger.info("Required total runes : %d" % total_runes_required)

        total_jewel_required = sum([get_required_jewel(hero_level=h.level) for h in heroes_to_level])
        logger.info("Total Jewel required : %d" % total_jewel_required)

        # total_runes = get_rune_count(account.public_address)
        # if total_runes < total_runes_required:
        #     runes_to_buy = total_runes_required - total_runes
        #     logger.info('Buying %d runes' % runes_to_buy)

        #total_jewel = get_jewel_count(account.public_address)
        # if total_jewel < total_jewel_required:
        #     jewel_to_buy = total_jewel_required - total_jewel
        #     logger.info('Buying %f jewel' % jewel_to_buy)

        for hero in get_account_heroes(account):
            if at_level_cap(hero.level, hero.current_xp):
                send_discord_message("Leveled up hero with ID %d from %d to %d"
                                     % (hero.hero_id, hero.level, hero.level + 1))
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

        send_discord_message("Started gold mine for account: %s" % account.public_address)
        start_gold_quest(account)
        update_local_hero_data.subtask().apply_async()


@celery.task(name='dfk.quest.gold-end')
def end_gold_mine():

    for account in get_accounts():
        heroes: [LocalHero] = get_account_heroes(account)
        hids = [h.dfk_hero_id for h in heroes]

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



