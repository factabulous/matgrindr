# -*- coding: utf-8 -*-

class EventEngine():
    def __init__(self, materials, requirements, visited):
        self._materials = materials
        self._requirements = requirements
        self._visited = visited

    def process(self, entry, state):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with (Action, Location)
        """
        if entry['event'] in ['FSDJump', 'StartUp', 'Location'] and 'StarPos' in entry and 'StarSystem' in entry:
            closest = self._materials.closest(entry['StarPos'], self._requirements)
            if closest and closest['system'].upper() == entry['StarSystem'].upper():
                target = self._materials.local(entry['StarSystem'], closest['body'])
		if target:
                    return ("Supercruise to", closest['body'], target[0]['lat'], target[0]['lon'])
                return ("Supercruise to", closest['body'])
            return ("Go to", closest['system'])

        if entry['event'] in ['Takeoff'] and 'StarPos' in state and 'StarSystem' in state:
            closest = self._materials.closest(state['StarPos'], self._requirements)
            if closest and closest['system'] == state['StarSystem']:
                return ("Supercruise to", closest['body'])
            return ("Go to", closest['system'])
        if entry['event'] in ['Touchdown'] and 'Latitude' in entry and 'Longitude' in entry:
            if 'StarSystem' in state and 'Body' in state:
                loc = { 
                    'system': state['StarSystem'],
                    'body': state['Body'],
                    'lat': entry['Latitude'],
                    'lon': entry['Longitude'] }
                target = self._materials.matches(loc)
                if target:
                    mats = set(target['materials']).intersection(self._requirements)
                    self._visited.set_visited(loc)
                    return ("Collect",",".join(mats))
        if entry['event'] in ['SupercruiseExit'] and 'StarSystem' in entry and 'Body' in entry and 'BodyType' in entry:
            if entry['BodyType'] == 'Planet':
                locs = self._materials.local(entry['StarSystem'], entry['Body'])
                if locs:
                    loc = locs[0]
                    return ( 'Fly to', "({:4.2f}, {:4.2f})".format(loc['lat'], loc['lon']), loc['lat'], loc['lon'])
                
        return None
