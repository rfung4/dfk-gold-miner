from web.src.celery import celery
from web.src.tasks.dfk_tasks import periodic_state_check, start_gold_mine, end_gold_mine, level_up_heroes


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30, periodic_state_check.s(), name='Hero state update & CHECK')
    sender.add_periodic_task(60, start_gold_mine.s(), name='Starts idle miners')
    sender.add_periodic_task(60, end_gold_mine.s(), name='Ends completed gold quests')
    sender.add_periodic_task(24*60*60, level_up_heroes.s(), name='Daily level up hero task')