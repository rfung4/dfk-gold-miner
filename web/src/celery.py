import os

from celery import Celery
from celery.signals import worker_ready

from web.src.db.query.heroes import clear_hero_data, set_all_account_hero_data
from web.src.static.loggers import logger

celery = Celery(broker=os.getenv('CELERY_BROKER_URL'))
celery.config_from_object('web.src.settings')
celery.autodiscover_tasks(packages=['web.src.tasks'])

task_base = celery.Task


@worker_ready.connect
def on_worker_ready(**_):
    logger.info('Worker starting up')
    clear_hero_data()
    set_all_account_hero_data()

    # resolve_gold_quests(cancel_quests=True)




