# -*- coding: utf-8 -*-

import sys
from util import same

class EventEngine():
    """
    This class takes in the events from the journal and uses them
    to maintain internal state and decide what should be displayed. 
    Note that it (and related classes) expect body names to be the 
    'short' form - so Achenar 1 would just have a body name '1'. 

    This is enforced by adding a field 'ShortBody' into events as the
    journals use longform body names.
    """

    def __init__(self, materials, requirements, visited):
        self._materials = materials
        self._requirements = requirements
        self._visited = visited
        self._location = {}

    def keys_in(self, d, keys):
        """
        Returns True if all keys are in d
        """
        for k in keys:
            if k not in d:
                return False
        return True
        
    def event_in(self, d, keys):
        """
        Returns True if the 'event' key contains one of the keys values
        """
        if 'event' in d:
            return d['event'] in keys
        return False

    def update_location(self, params = {}): 
        """
        Extracts as much location information as possible from data
        in the format of the journal messages
        """
        if 'StarSystem' in params:
            self._location = { 'system': params['StarSystem'] }

            if 'ShortBody' in params:
                self._location['body'] = params['ShortBody']

        if self.keys_in( params, ['Latitude', 'Longitude' ]):
            self._location['lat'] = params['Latitude']
            self._location['lon'] = params['Longitude']

        return self._location

    def location(self): 
        """
        Returns the current location we have built up from messages
        """
        return self._location

    def short_body(self, system, body):
        """
        Returns a field that contains
        the normalised body name
        """
        if body.startswith(system + ' '):
            return body[len(system)+1:]
        else:
            return body

    def make_params(self, entry, state):
        """
        Returns a combined set of parameters made from the 
        entry and state parameters, plus any internal state we 
        already have. Also adds a 'ShortBody' field that contains
        the normalised body name
        """
        p = {}
        p.update(state)
        p.update(entry)
        if self.keys_in(p, ['StarSystem', 'Body']):
            p['ShortBody'] = self.short_body(p['StarSystem'], p['Body'])
        return p

    def process(self, entry, state):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with fields indicating what has updated. Contains
            action - describes what to do
            location - one of the mats hashes with system, planet, lat, lon, mats
        """

        print("[matgrindr] Event {}".format(entry['event']))

        params = self.make_params(entry, state)
        if self.event_in(params, ['Takeoff', 'FSDJump', 'StartUp']) and self.keys_in(params, ['StarPos', 'StarSystem']):
            self.update_location( params )
            distance, closest = self._materials.closest(params['StarPos'], self._requirements)
            if closest and same(closest['system'], params['StarSystem']):
                target = self._materials.local(params['StarSystem'], closest['body'])
                if target:
                    return ("Supercruise to {} {}".format(target[0]['system'], target[0]['body']), target[0])
                return ("Unexpected supercruise to {} {}".format(closest['system'], closest['body']), closest)
            return ("Go to {} {} ({:1.0f} Ly)".format(closest['system'], closest['body'], distance), closest)

        if self.event_in(params, ['SupercruiseExit', 'Location']):
            # Useful for finding the body we are at
            self.update_location( params )
            
        if self.event_in(params, ['Touchdown']) and self.keys_in(params, ['Latitude', 'Longitude' ]):
            self.update_location( params )
            target = self._materials.matches(self.location())
            if target:
                mats = set(target['materials']).intersection(self._requirements)
                self._visited.set_visited(self.location())
                return ("Collect "+",".join(mats),)
            else:
                print("Failed to find touchdown target")
        return None
