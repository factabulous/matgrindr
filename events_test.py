#!/usr/bin/env python3

import unittest
import events

class FakeMaterials():
    def __init__(self, system_name, planet_name = None, lat = 0, lon = 0):
        self.system_name = system_name
        self.planet_name = planet_name
        self.lat = lat
        self.lon = lon

    def closest(self, pos1, pos2):
        if not self.system_name:
            return None
        return { 'system': self.system_name, 'planet': self.planet_name, 
                 'latitude': self.lat, 'longitude': self.lon }


class EventsTest(unittest.TestCase):
    def test_fsd_event_empty(self):
        """
        Simple test we return nothing if we aren't given coords
        """
        ev = events.EventEngine(FakeMaterials(None), None)
        self.assertIsNone(ev.process( { 'event': 'FSDJump' }, {} ))

    def test_fsd_event_wrong_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        ev = events.EventEngine(FakeMaterials('Sol'), None)
        self.assertEqual(("Go to", "Sol"), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'}, {} ))

    def test_fsd_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Mercury'), None)
        self.assertEqual(("Supercruise to", "Mercury"), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_location_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Venus'), None)
        self.assertEqual(("Supercruise to", "Venus"), ev.process( { 'event': 'Location', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_startup_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Earth'), None)
        self.assertEqual(("Supercruise to", "Earth"), ev.process( { 'event': 'StartUp', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

if __name__ == '__main__':
    unittest.main()
