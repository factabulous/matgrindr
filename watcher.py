# -*- coding: utf-8 -*-

import json
import threading
import os
import time
import mats
import sys
import requests

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

class MatsLoaderRemote(threading.Thread):
    """
    Fire and forget loader for materials - will queue a 'mats' event or 
    an 'error' event if the load fails. Automatically runs as a daemon
    """
    def __init__(self, filename, queue):
        """
        filename is the cache file - we only read the remote file 
        if the cache is old (or missing)
        queue is the queue to report the results into
    
        """
        threading.Thread.__init__(self)
        self.filename = filename
        self.queue = queue
        self.daemon = True

    def run(self):
        try:
            if not os.path.exists(self.filename):
                r = requests.get("https://docs.google.com/spreadsheets/u/0/d/1g0y7inyvQopJ93jP5YIu3n0veX0ng8DraJXAvZk6pS4/export?format=tsv&id=1g0y7inyvQopJ93jP5YIu3n0veX0ng8DraJXAvZk6pS4&gid=0")
               
                lines = t.text.split("\n")
                fields = line[0].split("\t")
                res = []
                with open(self.filename, "wt") as cache_file:
                    for entry in lines[1:]:
                        values = entry.split("\t")
                        v = {}
                        for k in range(0, len(fields)):
                            v[fields[k]] = entry[k]
                        res.append(v)
                    json.dump(cache_file, res)
                 
                self.queue.put( { 'mats': res } )
                print("Async mats loader is completed")
        except:
            self.queue.put( { 'error': 'Failed to load materials ' + str(sys.exc_info()[0]) } )

