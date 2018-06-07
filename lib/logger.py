import logging
from functools import wraps
import lib.log_config as log_config


logger = None


def get_logger():
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
    return logger


def configure_logger(log_file=None, level=None):
    global logger
    if log_file is None:
        log_file = log_config.DEFAULT_LOGFILE
    if level is None:
        level = log_config.DEFAULT_LEVEL
    logging.basicConfig(filename=log_file, level=level)
    if logger is None:
        logger = get_logger()
        logger.setLevel(level)



def log_decorator(f):
    global logger
    if logger is None:
        get_logger()
    @wraps(f)
    def do_log(*args,**kwargs):
        try:
            logger.debug('Called:  ' + f.__name__)
            logger.debug('Args:  ' + str(args) + '\nKwargs: ' + str(kwargs))
            result = f(*args,**kwargs)
            logger.debug('Return:  ' + f.__name__ + ' => ' + str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e
    return do_log



