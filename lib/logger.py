import logging
from functools import wraps
from lib.log_config import DEFAULT_FORMAT,DEFAULT_LOGFILE,DEFAULT_DIR,DEFAULT_LEVEL, LOGGING_ENABLED
import os

_logger = None


def get_logger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger(__name__)
        if not os.path.isdir(DEFAULT_DIR):
            os.mkdir(DEFAULT_DIR)
        file_handler = logging.FileHandler(os.path.join(DEFAULT_DIR, DEFAULT_LOGFILE))
        file_handler.formatter = logging.Formatter(DEFAULT_FORMAT)
        _logger.setLevel(DEFAULT_LEVEL)
        _logger.addHandler(file_handler)
    return _logger


def log_decorator(f):
    global _logger
    if _logger is None:
        get_logger()

    @wraps(f)
    def do_log(*args,**kwargs):
        if not LOGGING_ENABLED:
            return f(*args, **kwargs)
        try:
            #_logger.debug('Called:  {}'.format(f.__name__))
            _logger.debug('Args:  {}'.format(str(args)))
            _logger.debug('Kwargs: {}'.format(str(kwargs)))
            result = f(*args, **kwargs)
            _logger.debug('Return:  {0} => {1}'.format(f.__name__ , str(result)))
            return result
        except Exception as e:
            _logger.error(e)
            raise e
    return do_log