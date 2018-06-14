import logging
import os

DEFAULT_DIR = os.path.join(os.environ['HOME'], 'py_tracker')
DEFAULT_LOGFILE = 'py_tracker_cli.log'
DEFAULT_LEVEL = logging.DEBUG
DEFAULT_FORMAT = '%(asctime)s - %(name)s : %(levelname)s : %(funcName)s : %(module)s : %(message)s'
LOGGING_ENABLED = True


def configure_logger(logger):
    if not os.path.isdir(DEFAULT_DIR):
        os.mkdir(DEFAULT_DIR)
    file_handler = logging.FileHandler(os.path.join(DEFAULT_DIR, DEFAULT_LOGFILE))
    file_handler.formatter = logging.Formatter(DEFAULT_FORMAT)
    logger.setLevel(DEFAULT_LEVEL)
    logger.addHandler(file_handler)
    return logger
