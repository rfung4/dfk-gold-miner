CELERY_WORKER_CONCURRENCY = 8
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

imports = ("web.src.tasks.dfk_tasks", )
