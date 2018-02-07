# -*- coding: utf-8 -*-

import json
import math
import time

class Visited():
    def __init__(self, state = '[]', interval_days = 7):
       """
       state is a json string to take the initial state from - 
       see also the save() method. Can optionally set how long you want to 
       leave between visits

       Visits are dict entries containing:
           system / body / latitude / longitude / visit_time
       """
       self._visited = json.loads(state)
       self._interval_secs = interval_days * 24 * 3600

    def expired(self, t, now):
        """
        Helper to say of time 't' is expired with respect to the 
        now time using the interval specified in the constructor
        """

        how_long = now - t
        return how_long >= self._interval_secs

    def save(self, when=time.time()):
        """
        Returns a string representation of the visited status such that it
        can be stored in a string

        when allows you to specify the time now - mainly for testing
        """
        return json.dumps([ x for x in self._visited if not self.expired(x['at'], when)])

    def find(self, location):
        """
        Finds a location in the store, or return None if not present
        """
        for v in self._visited:
            if v['system'] == location['system'] and v['body'] == location['body'] and v['lat'] == location['lat'] and v['lon'] == location['lon']:
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
        else:
            location['at'] = when
            self._visited.append(location)

    def is_visited(self, location, when=time.time()):
        """
        Asks if a location is visited. Location is expected to be a dict 
        containing system / body / lat / lon
        when allows you to specify the time now - mainly for testing
        Returns True or False
        """
        v = self.find(location)
        if v and not self.expired(v['at'], when):
            return True
        return False
        



