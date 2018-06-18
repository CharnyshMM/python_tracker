"""This module describes Parser class"""

import argparse
import sys


class Parser(argparse.ArgumentParser):
    """Just a wrapper for default ArgumentParser to add ability to print help in case of error arguments"""
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
