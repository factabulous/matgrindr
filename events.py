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

        if entry['event'] in ['Touchdown'] and 'Latitude' in entry and 'Longitude' in entry:
            if 'StarSystem' in state and 'Body' in state:
                loc = { 
                    'system': state['StarSystem'],
                    'planet': state['Body'],
                    'lat': entry['Latitude'],
                    'lon': entry['Longitude'] }
                if not self.visited.is_visited(loc) and self.materials.matches(loc):
                    self.visited.visited(loc)
                    return ("Collect",)
                
        return None
