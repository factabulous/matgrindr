# -*- coding: utf-8 -*-

from config import config
import time
import os
import sys
import requests
import util

class Version():
    """
    Class to encapsulate version checking against github. 
    The config_prefix is used for accessing local keys, and
    version_url is the url of the VERSION.md file on github

    No tests, as it relies on EDMC methods :(
    """
    def __init__(self, config_prefix, version_url):
        self._config_prefix = config_prefix
        self._last_check_key = config_prefix + ".last_vcheck"
        self._version_url = version_url

    def is_new_version(self):
        last_check = float(config.get(self._last_check_key) or "0")
        now = time.time()
        # Only check every 24 hours
        if now < last_check + 24 * 3600:
            return False
        try:
            on_github = requests.get(self._version_url).text.strip()
            util.debug("Github version {}".format(on_github))
            config.set(self._last_check_key, str(now))

            with open(util.local_file("VERSION.md"), "rt") as current_version_file:
                installed_version = current_version_file.read().strip()
                util.debug("Local version {}".format(installed_version))

                different =  installed_version != on_github
                util.debug("Versions different?: {}".format( different ))
                return different
        except:
            util.error("[kumay3305] Exception reading version files" + str(sys.exc_info()[0]))
        return False
