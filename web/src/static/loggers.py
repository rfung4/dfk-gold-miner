import logging
import os
from logging.handlers import RotatingFileHandler
from definitions import ERROR_LOG_PATH, DEFAULT_LOG_PATH, CRITICAL_LOG_PATH

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

format_type = logging.Formatter('[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()))


error_log_handler = logging.FileHandler(filename=ERROR_LOG_PATH, mode='a')
error_log_handler.setLevel(logging.ERROR)
error_log_handler.setFormatter(format_type)
logger.addHandler(error_log_handler)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

critical_log_handler = logging.FileHandler(filename=CRITICAL_LOG_PATH, mode='a')
critical_log_handler.setLevel(logging.CRITICAL)
critical_log_handler.setFormatter(format_type)
logger.addHandler(critical_log_handler)

default_log_handler = RotatingFileHandler(filename=DEFAULT_LOG_PATH, mode='a',
                                          maxBytes=1024 * 1000 * 50, backupCount=1)
default_log_handler.setLevel(logging.INFO)
logger.addHandler(default_log_handler)
default_log_handler.setFormatter(format_type)





