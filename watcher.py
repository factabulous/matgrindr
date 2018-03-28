# -*- coding: utf-8 -*-

import json
import threading
import os
import time
import mats
import sys
import requests
import traceback
import re
from util import debug

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
        self.integerRe = re.compile(r'^-?\d+$')
        self.floatRe = re.compile(r'^-?\d+(\.\d+)?$')
        self.arrayRe = re.compile(r'^\[.*\]$')

    def need_refresh(self):
        """
        Returns True if the local cache needs a refresh. 
        """
        if not os.path.exists(self.filename):
            return True

        mtime = os,path.getmtime(self.filename)
        now = time.time()
        return mtime < now - 24 * 3600 # Daily update

    def array_splitter(self, value):
        return [ x[1:-1] for x in value[1:-1].split(", ") ]

    def detect(self, value):
        """
        Looks at a data value and converts into an appropriate type
        (maybe should look at using ast instead)
        """
        if self.integerRe.match(value):
            return int(value)
        elif self.floatRe.match(value):
            return float(value)
        elif self.arrayRe.match(value):
            return self.array_splitter(value)
        else:
            return value

    def parse(self, text):
        """
        Parse a string field containing all the data ina TSV
        into an array of dicts. Mainly split out so we can test
        """

        lines = text.replace("\r", "").split("\n")
        fields = lines[0].split("\t")
        res = []
        for entry in lines[1:]:
            values = entry.split("\t")
            if len(values) < len(fields):
                continue
            v = {}
            for k in range(0, len(fields)):
                v[fields[k]] = self.detect(values[k])
            res.append(v)
        return res

    def run(self):
        try:
            if self.need_refresh():
                r = requests.get("https://docs.google.com/spreadsheets/u/0/d/1g0y7inyvQopJ93jP5YIu3n0veX0ng8DraJXAvZk6pS4/export?format=tsv&id=1g0y7inyvQopJ93jP5YIu3n0veX0ng8DraJXAvZk6pS4&gid=0")
               
                res = self.parse(r.text)

                if res:
                    with open(self.filename, "wt") as cache_file:
                        json.dump(res, cache_file)
                     
                    self.queue.put( { 'mats': res } )
                    debug("Async remote mats loader from tsv is completed {} entries".format(len(res)))
                else:
                    debug("Async remote mats loader failed - zero records")
        except:
            self.queue.put( { 'error': 'Failed to load tsv materials ' + str(sys.exc_info()[0]) + ' ' + traceback.format_exc() } )

