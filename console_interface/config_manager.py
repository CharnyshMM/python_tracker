"""This module describes a ConfigManager class"""

import configparser
import os

DEFAULT_DIR = os.path.join(os.environ['HOME'], 'py_tracker')
CONFIG_PATH = os.path.join(DEFAULT_DIR, 'py_tracker_cli.config')

class ConfigManager:
    """Tiny config manager for Console interface. Config stores default user."""
    def __init__(self):
        self.config = configparser.ConfigParser()
        try:
            if not os.path.isdir(DEFAULT_DIR):
                os.mkdir(DEFAULT_DIR)
            self.config.read(CONFIG_PATH)
        except FileNotFoundError:
            self.config['USER'] = ''
            self.write_config()

    def read_config(self):
        self.config.read(CONFIG_PATH)

    def get_default_user(self):
        self.read_config()
        if (not self.config.has_option('DEFAULT', 'USER')) or self.config['DEFAULT']['USER'] == '':
            return None
        return self.config['DEFAULT']['USER']

    def set_default_user(self, user):
        if self.config is None:
            self.config = configparser.ConfigParser()
        self.config.set('DEFAULT','USER',user)
        self.write_config()

    def write_config(self):
        with open(CONFIG_PATH, 'w') as configfile:
            self.config.write(configfile)

