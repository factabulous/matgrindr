# -*- coding: utf-8 -*-

from config import config
import time
import os
import sys

class Version():
    """
    Class to encapsulate version checking against github. 

    No tests, as it relies on EDMC methods :(
    """
    def __init__(self, config_prefix):
        self._config_prefix = config_prefix
        self._last_check_key = config_prefix + ".last_vcheck"

    def local_file(name):
        # TODO: This is a duplicate from load.py
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    def is_new_version(self):
        last_check = float(config.get(self._last_check_key) or "0")
        now = time.time()
        # Only check every 24 hours
        if now < last_check + 24 * 3600:
            return False
        try:
            on_github = requests.get("https://raw.githubusercontent.com/factabulous/matgrindr/master/VERSION.md").text.strip()
            config.set(self._last_check_key, str(now))

            with open(local_file("VERSION.md"), "rt") as current_version_file:
                current_version = current_version_file.read().strip()

                return current_version != on_github
        except:
            print("[matgrindr] Exception reading version files" + sys.exc_info()[0])
        return False
