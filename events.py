# -*- coding: utf-8 -*-

class EventEngine():
    def __init__(self, materials, requirements, visited):
        self._materials = materials
        self._requirements = requirements
        self._visited = visited

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

    def process(self, entry, state):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with (Action, Location)
        """

        params = state.copy()
        params.update(entry)
        if self.event_in(params, ['Takeoff', 'FSDJump', 'StartUp', 'Location']) and self.keys_in(params, ['StarPos', 'StarSystem']):
            closest = self._materials.closest(params['StarPos'], self._requirements)
            if closest and closest[1]['system'].upper() == params['StarSystem'].upper():
                target = self._materials.local(params['StarSystem'], closest[1]['body'])
                if target:
                    return ("Supercruise to", closest[1]['body'], target[0]['lat'], target[0]['lon'])
                return ("Supercruise to", closest[1]['body'])
            return ("Go to", "{} ({:3.1f} Ly)".format(closest[1]['system'], closest[0]), None, None)

        if self.event_in(params, ['Touchdown']) and self.keys_in(params, ['Latitude', 'Longitude', 'StarSystem', 'Body']):
                loc = { 
                    'system': params['StarSystem'],
                    'body': params['Body'],
                    'lat': params['Latitude'],
                    'lon': params['Longitude'] }
                target = self._materials.matches(loc)
                if target:
                    mats = set(target['materials']).intersection(self._requirements)
                    self._visited.set_visited(loc)
                    return ("Collect",",".join(mats))
                else:
                    print("Failed to find touchdown target")
        if self.event_in(params, ['SupercruiseExit']) and self.keys_in(params, ['StarSystem' , 'Body', 'BodyType']):
            if params['BodyType'] == 'Planet':
                locs = self._materials.local(params['StarSystem'], params['Body'])
                if locs:
                    loc = locs[0]
                    return ( 'Fly to', "({:4.2f}, {:4.2f})".format(loc['lat'], loc['lon']), loc['lat'], loc['lon'])
                
        return None
