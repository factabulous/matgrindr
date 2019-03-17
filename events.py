# -*- coding: utf-8 -*-

import sys
from util import same
import location
from util import debug

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
        self._location = location.Location()
        self._types = None

    def change_requirements(self, requirements, types):
        """
        When the user changes what they want, use this to update the event
        engine
        requirements - the materials we are interested in
        types - the types of location to search for the requirements - None is all
        """
        self._requirements = requirements
        self._types = types

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
        debug(fmt.format("key", "event", "state"))
        for k in keys:
            debug(fmt.format(k, rep_key(event, k), rep_key(state, k)))
               
        
    def event_in(self, d, keys):
        """
        Returns True if the 'event' key contains one of the keys values
        """
        if 'event' in d:
            return d['event'] in keys
        return False

    def location(self): 
        """
        Returns the current location we have built up from messages
        """
        return self._location.get()

    def is_on_planet(self):
        """
        Indicates if we know lat log - so not really 'on planet' as 
        takeoff knows latlon
        """
        return self._location.has_latlon()

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

    def is_event_with_params(self, event, event_names, params):
        """
        Checks if the event contains an 'event' key containing on
        of 'event_names' and also has keys from all the values in 'params'
        """
        if 'event' in event and event['event'] in event_names:
            for k in params:
                if k not in event:
                    return False
            return True
        return False

    def process(self, entry, state, current_target = None):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with fields indicating what has updated. Contains
            action - describes what to do
            location - one of the mats hashes with 
                       system, planet, lat, lon, mats
            display_target - True or False to determine whether to show the 
                              target fields or blank them

        Body is reported by:
            Location
            ApproachBody
        Latitude is reported by:
            Location
            Liftoff
            Touchdown
        StarPos is reported by:
            Location
            FSDJump
        StarSystem is reported by: 
            Docked
            FSDJump
            Location
            StartJump
            SupercruiseEntry
            ApproachBody
        """

        debug("[matgrindr] Event {}".format(entry['event']))

        params = self.make_params(entry, state)
        system_ev = ['FSDJump', 'Location', 'StartUp', 'LoadGame']
        body_ev = ['ApproachBody', 'Location', 'StartUp', 'LoadGame']
        latlon_ev = ['Touchdown', 'Location', 'Liftoff', 'StartUp', 'LoadGame']

        if self.is_event_with_params(params, system_ev + body_ev + latlon_ev, ['StarSystem', 'StarPos']):
            self._location.change_system(params['StarSystem'], params['StarPos'])
        if self.is_event_with_params(params, body_ev + latlon_ev, ['ShortBody']):
            self._location.change_body(params['ShortBody'])
        if self.is_event_with_params(params, latlon_ev, ['Latitude', 'Longitude']):
            self._location.change_latlon(params['Latitude'], params['Longitude'])
        if params['event'] == 'Touchdown':
            self._location.landed(True)
        if params['event'] == 'Liftoff':
            self._location.landed(False)

        location_changed = self._location.is_changed()
        if location_changed:
            keys = ['StarPos', 'StarSystem', 'Body', 'Latitude', 'Longitude']
            self.report_keys(entry, state, keys)

            return self.find_location(current_target)

    def find_location(self, current_target = None):
        """
        Finds where we should be heading based the current location state
        current_target is where we are currently headed, can be None
        """

        debug("find_location - location is {}".format(self._location._loc))

        if self._location.is_landed():
            debug("Landed")
            target = self._materials.matches(self.location())
            if target:
                debug("Found a resource on planet")
                mats = set(target['materials']).intersection(self._requirements)
                self._visited.set_visited(target)
                return ("Collect "+", ".join(mats),target, False)

        if self._location.has_system():
            distance, closest = self._materials.closest(self._location.pos(), self._requirements, types = self._types)
            if self._location.has_body():
                # If we are already heading to a location then stick with it, 
                # don't flip between targets on a body as they get close
                if current_target and not self._visited.is_visited(current_target):
                    return ("Land at target", current_target, True)
                # See if there is another location on this body
                local = self._materials.local(self._location.system(), self._location.body())
                if local:
                    debug("More mats on same body")
                    return ("Land at target", local[0], True)
                else:
                    print("No more mats local to this body {}".format(self._location.body()))
            if closest and same(closest['system'], self._location.system()):
                debug("in correct system")
                return ("Supercruise to {} {}".format(closest['system'], closest['body']), closest, True)
            if closest:
                return ("Go to {} ({:1.0f} Ly)".format(closest['system'], distance), closest, False)


