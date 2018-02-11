# -*- coding: utf-8 -*-

import sys
from util import same

class EventEngine():
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

            if 'Body' in params:
                self._location['body'] = params['Body']

        if self.keys_in( params, ['Latitude', 'Longitude' ]):
            self._location['lat'] = params['Latitude']
            self._location['lon'] = params['Longitude']

        return self._location

    def location(self): 
        """
        Returns the current location we have built up from messages
        """
        return self._location

    def process(self, entry, state):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with fields indicating what has updated. Contains
            action - describes what to do
            location - one of the mats hashes with system, planet, lat, lon, mats
        """

        print("[matgrindr] Event {}".format(entry['event']))

        params = state.copy()
        params.update(entry)
        if self.event_in(params, ['Takeoff', 'FSDJump', 'StartUp']) and self.keys_in(params, ['StarPos', 'StarSystem']):
            self.update_location( params )
            closest = self._materials.closest(params['StarPos'], self._requirements)
            if closest and same(closest[1]['system'], params['StarSystem']):
                target = self._materials.local(params['StarSystem'], closest[1]['body'])
                if target:
                    return ("Supercruise to {} {}".format(target[0]['system'], target[0]['body']), target[0])
                return ("Unexpected supercruise to {} {}".format(closest[1]['system'], closest[1]['body']), closest[1])
            return ("Go to {} {} ({:1.0f} Ly)".format(closest[1]['system'], closest[1]['body'], closest[0]), closest[1])

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
