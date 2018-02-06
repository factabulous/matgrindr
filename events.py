# -*- coding: utf-8 -*-

class EventEngine():
    def __init__(self, materials, requirements, visited):
        self.materials = materials
        self.requirements = requirements
        self.visited = visited

    def process(self, entry, state):
        """
        Decides what we should do given a new journal event. Returns either
        None or a tuple with (Action, Location)
        """
        if entry['event'] in ['FSDJump', 'StartUp', 'Location'] and 'StarPos' in entry and 'StarSystem' in entry:
            closest = self.materials.closest(entry['StarPos'], self.requirements)
            if closest and closest['system'] == entry['StarSystem']:
                return ("Supercruise to", closest['planet'])
            return ("Go to", closest['system'])

        if entry['event'] in ['Takeoff'] and 'StarPos' in state and 'StarSystem' in state:
            closest = self.materials.closest(state['StarPos'], self.requirements)
            if closest and closest['system'] == state['StarSystem']:
                return ("Supercruise to", closest['planet'])
            return ("Go to", closest['system'])
        if entry['event'] in ['Touchdown'] and 'Latitude' in entry and 'Longitude' in entry:
            if 'StarSystem' in state and 'Body' in state:
                loc = { 
                    'system': state['StarSystem'],
                    'planet': state['Body'],
                    'lat': entry['Latitude'],
                    'lon': entry['Longitude'] }
                target = self.materials.matches(loc)
                if not self.visited.is_visited(loc) and target:
                    mats = set(target['materials']).intersection(self.requirements)
                    self.visited.visited(loc)
                    return ("Collect",",".join(mats))
        if entry['event'] in ['SupercruiseExit'] and 'StarSystem' in entry and 'Body' in entry and 'BodyType' in entry:
            if entry['BodyType'] == 'Planet':
                locs = self.materials.local(entry['StarSystem'], entry['Body'])
                if locs:
                    loc = locs[0]
                    return ( 'Fly to', "({:4.2f}, {:4.2f})".format(loc['lat'], loc['lon']), loc['lat'], loc['lon'])
                
        return None
