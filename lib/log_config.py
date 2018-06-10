import logging
import os

DEFAULT_DIR = os.path.join(os.environ['HOME'], 'py_tracker')
DEFAULT_LOGFILE = 'py_tracker_lib.log'
DEFAULT_LEVEL = logging.DEBUG
DEFAULT_FORMAT = '%(asctime)s - %(name)s : %(levelname)s : %(funcName)s : %(module)s : %(message)s'
LOGGING_ENABLED = True