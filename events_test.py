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
        self.res = { 'system': self.system_name, 'body': self.body_name, 
                 'lat': self.lat, 'lon': self.lon, 'materials': self.mats }

    def closest(self, pos1, pos2):
        if not self.system_name:
            return None
        return (12, self.res)

    def matches(self, loc):
        return self.res

    def local(self, system, planet):
        return [ self.res ]

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
        mats = FakeMaterials('Sol', 'Luna')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Go to Sol Luna (12 Ly)", mats.res), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'}, {} ))

    def test_fsd_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        mats = FakeMaterials('Sol', 'Mercury')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Mercury", mats.res), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_fsd_event_correct_system_case_wrong(self):
        """
        test when systems do match we ask for the planet(s) to show and
        the data has case differences from the events
        """
        mats = FakeMaterials('SOL', 'MERCURY')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to SOL MERCURY", mats.res), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def _test_location_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        (Location even no longer causes nav events)
        """
        mats = FakeMaterials('Sol', 'Venus')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Venus", mats.res), ev.process( { 'event': 'Location', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_startup_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        mats = FakeMaterials('Sol', 'Earth')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Earth", mats.res), ev.process( { 'event': 'StartUp', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_touchdown_at_target(self):
        """
        test that we note success when we hit a target
        """
        visited = NoneVisited()
        mats = FakeMaterials('Sol', 'Earth', 13, 67, ['Iron', 'Gold'])
        ev = events.EventEngine(mats, ['Gold'], visited)
        ev.process( {'event': 'Location', 'StarSystem': 'Sol', "Body": 'Earth'}, {} )
        self.assertEqual(("Collect Gold",), ev.process( { 'event': 'Touchdown', 'Latitude': 13, 'Longitude': 67}, {'StarSystem': 'Sol', "Body": 'Earth'} ))
        self.assertEqual( { 'system': 'Sol', 'body': 'Earth', 'lat': 13, 'lon': 67 }, visited.captured_visit())

    def test_touchdown_at_target_wrong_case(self):
        """
        test that we note success when we hit a target but the dataset
        case doesn't match the ones from the events
        """
        visited = NoneVisited()
        mats = FakeMaterials('SOL', 'EARTH', 13, 67, ['Iron', 'Gold'])
        ev = events.EventEngine(mats, ['Gold'], visited)
        ev.process( { 'event': 'SupercruiseExit', 'StarSystem': 'Sol', 'Body': 'Earth' }, {} )
        self.assertEqual(("Collect Gold",), ev.process( { 'event': 'Touchdown', 'Latitude': 13, 'Longitude': 67}, {} ))
        self.assertEqual( { 'system': 'Sol', 'body': 'Earth', 'lat': 13, 'lon': 67 }, visited.captured_visit())
        
    def test_takeoff_event_wrong_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        mats = FakeMaterials('Sol', 'Earth')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Go to Sol Earth (12 Ly)", mats.res), ev.process( { 'event': 'Takeoff'}, {  'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'} ))

    def test_takeoff_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        mats = FakeMaterials('Sol', 'Mercury')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Mercury", mats.res), ev.process( { 'event': 'Takeoff'}, { 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'} ))


if __name__ == '__main__':
    unittest.main()
