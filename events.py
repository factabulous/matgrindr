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

    def report_keys(self, event, state, keys):
        """
        Reports on presence of names keys (in list) in the event/state stores. 
        reporting them using the given name, e.g.:
            <key> [Yes|No] [Yes|No}
        """

        def rep_key(store, key):
            return "Yes" if key in store else "No"
        
        fmt = "{:10s} {:>10s} {:>10s}"
        print(fmt.format("key", "event", "state"))
        for k in keys:
            print(fmt.format(k, rep_key(event, k), rep_key(state, k)))
               
        
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
    def remove_latlon(self):
        self._location['lat'] = None
        self._location['lon'] = None

    def location(self): 
        """
        Returns the current location we have built up from messages
        """
        return self._location

    def is_on_planet(self):
        return 'lat' in self._location and self._location['lat'] != None

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

    def on_correct_body(self, params, closest):
        return 'ShortBody' in params and same(closest['body'], params['ShortBody'])

    def process(self, entry, state):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with fields indicating what has updated. Contains
            action - describes what to do
            location - one of the mats hashes with system, planet, lat, lon, mats
        """

        print("[matgrindr] Event {}".format(entry['event']))

        params = self.make_params(entry, state)
        location_changed = False
        if self.event_in(params, ['Touchdown', 'StartUp', 'Liftoff', 'FSDJump', 'Location', 'SupercruiseExit', 'SupercruiseEntry']):
            # These events can change our location
            self.update_location( params )
            location_changed = True

        if self.event_in(params, ['Liftoff', 'FSDJump', 'SupercruiseEntry']):
            # These events make us want to ignore latlon if we have one
            self.remove_latlon()
            location_changed = True

        if location_changed:
            keys = ['StarPos', 'StarSystem', 'Body', 'Latitude', 'Longitude']
            self.report_keys(entry, state, keys)

        if location_changed and self.is_on_planet():
            print("On a planet")
            target = self._materials.matches(self.location())
            if target:
                print("Found a resource on planet")
                mats = set(target['materials']).intersection(self._requirements)
                self._visited.set_visited(target)
                return ("Collect "+",".join(mats),)

        if location_changed and self.keys_in(params, ['StarPos']):
            distance, closest = self._materials.closest(params['StarPos'], self._requirements)
            if closest and same(closest['system'], self._location['system']):
                print("Are in correct system")
                return ("Supercruise to {} {}".format(closest['system'], closest['body']), closest)
            return ("Go to {} {} ({:1.0f} Ly)".format(closest['system'], closest['body'], distance), closest)


