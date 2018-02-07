#!/usr/bin/env python3

import unittest
import events

class FakeMaterials():
    def __init__(self, system_name, body_name = None, lat = 0, lon = 0, mats = []):
        self.system_name = system_name
        self.body_name = body_name
        self.lat = lat
        self.lon = lon
        self.mats = mats

    def closest(self, pos1, pos2):
        if not self.system_name:
            return None
        return { 'system': self.system_name, 'body': self.body_name, 
                 'lat': self.lat, 'lon': self.lon, 'materials': self.mats }

    def matches(self, loc):
        return { 'system': self.system_name, 'body': self.body_name, 
                 'lat': self.lat, 'lon': self.lon, 'materials': self.mats }

    def local(self, system, planet):
        return [ {'system': self.system_name, 'body': self.body_name, 
                 'lat': self.lat, 'lon': self.lon, 'materials': self.mats }]
 

class NoneVisited():
    def is_visited(self, loc):
        return False

    def set_visited(self, loc):
        self._captured_visit = loc

    def captured_visit(self):
        return self._captured_visit


class EventsTest(unittest.TestCase):
    def test_fsd_event_empty(self):
        """
        Simple test we return nothing if we aren't given coords
        """
        ev = events.EventEngine(FakeMaterials(None), None, NoneVisited())
        self.assertIsNone(ev.process( { 'event': 'FSDJump' }, {} ))

    def test_fsd_event_wrong_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        ev = events.EventEngine(FakeMaterials('Sol'), None, NoneVisited())
        self.assertEqual(("Go to", "Sol"), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'}, {} ))

    def test_fsd_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Mercury'), None, NoneVisited())
        self.assertEqual(("Supercruise to", "Mercury"), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_location_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Venus'), None, NoneVisited())
        self.assertEqual(("Supercruise to", "Venus"), ev.process( { 'event': 'Location', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_startup_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Earth'), None, NoneVisited())
        self.assertEqual(("Supercruise to", "Earth"), ev.process( { 'event': 'StartUp', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_touchdown_at_target(self):
        """
        test that we note success when we hit a target
        """
        visited = NoneVisited()
        ev = events.EventEngine(FakeMaterials('Sol', 'Earth', 13, 67, ['Iron', 'Gold']), ['Gold'], visited)
        self.assertEqual(("Collect","Gold"), ev.process( { 'event': 'Touchdown', 'Latitude': 13, 'Longitude': 67}, {'StarSystem': 'Sol', "Body": 'Earth'} ))
        self.assertEqual( { 'system': 'Sol', 'body': 'Earth', 'lat': 13, 'lon': 67 }, visited.captured_visit())
        
    def test_takeoff_event_wrong_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        ev = events.EventEngine(FakeMaterials('Sol'), None, NoneVisited())
        self.assertEqual(("Go to", "Sol"), ev.process( { 'event': 'Takeoff'}, {  'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'} ))

    def test_takeoff_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Mercury'), None, NoneVisited())
        self.assertEqual(("Supercruise to", "Mercury"), ev.process( { 'event': 'Takeoff'}, { 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'} ))

    def test_supercruise_exit_event_correct_planet(self):
        """
        test when system and planet match we return a location to visit on 
        the planet, plus the lat / lon to go to
        """
        ev = events.EventEngine(FakeMaterials('Sol', 'Mercury', 12, 88), None, NoneVisited())
        self.assertEqual(("Fly to", "(12.00, 88.00)", 12, 88), ev.process( { 'event': 'SupercruiseExit', 'StarSystem': 'Sol', 'Body': 'Mercury', 'BodyType': 'Planet'}, {} ))

if __name__ == '__main__':
    unittest.main()
