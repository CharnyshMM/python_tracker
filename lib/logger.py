import logging

DEFAULT_LOGFILE = '../root_logger.txt'

logger = None


def get_logger():
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
    return logger


def configure_logger(log_file=None, level=logging.DEBUG):
    global logger
    if log_file is None:
        log_file = DEFAULT_LOGFILE
    logging.basicConfig(filename=log_file, level=level)
    if logger is None:
        logger = get_logger()
        logger.setLevel(level)



def log_decorator(f):
    global logger
    def do_log(*args,**kwargs):
        try:
            logger.debug('Called:  ' + f.__name__)
            logger.debug('Args:  ' + str(args) + ' Kwargs: ' + str(kwargs))
            result = f(*args,**kwargs)
            logger.debug('Return:  ' + f.__name__ + ' => ' + str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e
    return do_log



