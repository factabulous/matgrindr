# -*- coding: utf-8 -*-

class Action():
    def __init__(self, show_bearing = False, show_system = False, show_planet = False, show_action = False):
        self._show_bearing = show_bearing
        self._show_system = show_system
        self._show_planet = show_planet
        self._show_action = show_action

    def show_bearing(self):
        """
        Should be be showing (and updating) the bearing info?
        """
        return self._show_bearing

    def show_system(self):
        """
        Should be be showing the system to navigate to?
        """
        return self._show_system

    def show_planet(self):
        """
        Should we be showing the planet to navigate to?
        """
        return self._show_planet

    def show_action(self):
        """
        Should we be showing the action to take at the location?
        """
        return self._show_action

class EventEngine():
    def __init__(self, materials, requirements):
        self.materials = materials
        self.requirements = requirements

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
        return None
