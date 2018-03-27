# -*- coding: utf-8 -*-

import json
import math
import time
from util import debug
from util import same

class Visited():
    def __init__(self, state = '[]', interval_days = 7):
       """
       state is a json string to take the initial state from - 
       see also the save() method. Can optionally set how long you want to 
       leave between visits

       Visits are dict entries containing:
           system / body / latitude / longitude / visit_time
       """
       if not state:
           state = '[]'
       self._visited = json.loads(state)
       self._interval_secs = interval_days * 24 * 3600
       self._is_dirty = False

    def expired(self, t, now, period_secs = 24 * 7 * 3600 ):
        """
        Helper to say of time 't' is expired with respect to the 
        now time using the interval specified in the constructor
        """

        how_long = now - t
        return how_long >= period_secs

    def unexpired(self, when=time.time()):
        """
        Returns all the unexpired sites we know of 
        """
        return [ x for x in self._visited if not self.expired(x['at'], when, period_secs = self.expiry_secs(x))]

    def expiry_secs(self, entry):
        """
        Returns how many seconds before an entry expires
        """
        if 'respawn_days' in entry:
            return 24 * 3600 * entry['respawn_days']
        return self._interval_secs


    def save(self, when=time.time()):
        """
        Returns a string representation of the visited status such that it
        can be stored in a string

        when allows you to specify the time now - mainly for testing

        assumes that the save is successful, and the store is no longer dirty
        """
        self._is_dirty = False
        debug("Saving the visited() list - entries" + str(len(self.unexpired(when))))
        return json.dumps(self.unexpired(when))

    def find(self, location):
        """
        Finds a location in the store, or return None if not present
        """
        for v in self._visited:
            if same(v['system'], location['system']) and same(v['body'], location['body']) and v['lat'] == location['lat'] and v['lon'] == location['lon']:
                return v
        return None

    def set_visited(self, location, when=time.time()):
        """
        Sets a location as visited. Location is expected to be a dict 
        containing system / body / lat / lon
        when allows you to specify the time now - mainly for testing
        """
        v = self.find(location)
        if v:
            v['at'] = when
            debug("Setting previously site to 'visited' again")
        else:
            location = location.copy()
            location['at'] = when
            self._visited.append(location)
            debug("Adding site to 'visited' list")
        self._is_dirty = True

    def is_visited(self, location, when=time.time()):
        """
        Asks if a location is visited. Location is expected to be a dict 
        containing system / body / lat / lon
        when allows you to specify the time now - mainly for testing
        Returns True or False
        """
        v = self.find(location)
        if v:
            return False if self.expired(v['at'], when, period_secs = self.expiry_secs(v)) else True
        return False

    def is_dirty(self):
        """
        Returns True if the data should be written to storage. Note that
        expired entries do not count towards dirty state - they are left xu
        until a new entry is written, and will be removed then
        """
        debug("Asked if the visited() set is dirty: " + str(self._is_dirty))
        return self._is_dirty

