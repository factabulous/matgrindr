# -*- coding: utf-8 -*-

import json
import threading
import os
import time
import mats
import sys

class MatsLoader(threading.Thread):
    """
    Fire and forget loader for materials - will queue a 'mats' event or 
    an 'error' event if the load fails. Automatically runs as a daemon
    """
    def __init__(self, filename, queue):
        """
        filename is the file to async load
        queue is the queue to report the results into
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.filename = filename
        self.daemon = True

    def run(self):
        try:
            m = mats.Materials(self.filename)
            self.queue.put( { 'mats': m._materials } )
            print("Async mats loader is completed")
        except:
            self.queue.put( { 'error': 'Failed to load materials ' + str(sys.exc_info()[0]) } )

