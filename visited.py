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
       self.visited = json.loads(state)
       self.interval_days = 7

    def save(self, when=time.time()):
        """
        Returns a string representation of the visited status such that it
        can be stored in a string
        """
        return json.dumps(self.visited)

    def set_visited(self, location, when=time.time()):
        """
        Sets a location as visited. Location is expected to be a dict 
        containing system / body / latitude / longitude
        """
        pass # For now - needs implementing

    def is_visited(self, location, when=time.time()):
        """
        Asks if a location is visited. Location is expected to be a dict 
        containing system / body / latitude / longitude
        Returns True or False
        """
        return False # For now - needs implementing



