#!/usr/bin/env python3

import unittest
import events

class FakeMaterials():
    def __init__(self, system_name):
        self.system_name = system_name

    def closest(self, pos1, pos2):
        if not self.system_name:
            return None
        return { 'system': self.system_name }


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
        self.assertTrue(ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'}, {} ).show_system())

    def test_fsd_event_correct_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        ev = events.EventEngine(FakeMaterials('Sol'), None)
        self.assertTrue(ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ).show_planet())

    def test_location_event_correct_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        ev = events.EventEngine(FakeMaterials('Sol'), None)
        self.assertTrue(ev.process( { 'event': 'Location', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ).show_planet())

    def test_startup_event_correct_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        ev = events.EventEngine(FakeMaterials('Sol'), None)
        self.assertTrue(ev.process( { 'event': 'StartUp', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ).show_planet())

if __name__ == '__main__':
    unittest.main()
