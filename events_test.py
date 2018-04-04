#!/usr/bin/env python3

import unittest
import events

class FakeMaterials():
    def __init__(self, system_name, body_name = None, lat = None, lon = None, mats = []):
        self.system_name = system_name
        self.body_name = body_name
        self.lat = lat
        self.lon = lon
        self.mats = mats
        self.res = { 'system': self.system_name, 'body': self.body_name, 
                 'lat': self.lat, 'lon': self.lon, 'materials': self.mats,
                 'x': 0, 'y': 0, 'z': 0 }

    def closest(self, pos1, pos2):
        if not self.system_name:
            return None
        return (12, self.res)

    def matches(self, loc):
        # We only check lat for a match
        return self.res if self.res['lat'] and self.res['lat'] == loc['lat'] else None

    def local(self, system, planet):
        return [ self.res ] if self.res['lat'] else []

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
        self.assertEqual(("Go to Sol (12 Ly)", mats.res, False), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'}, {} ))

    def test_fsd_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        mats = FakeMaterials('Sol', 'Mercury')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Mercury", mats.res, True), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_fsd_event_correct_system_case_wrong(self):
        """
        test when systems do match we ask for the planet(s) to show and
        the data has case differences from the events
        """
        mats = FakeMaterials('SOL', 'MERCURY')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to SOL MERCURY", mats.res, True), ev.process( { 'event': 'FSDJump', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_location_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        (Location even no longer causes nav events)
        """
        mats = FakeMaterials('Sol', 'Venus')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Venus", mats.res, True), ev.process( { 'event': 'Location', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_approach_body_event_correct_system(self):
        """
        test when system and body do match we ask for the coordinates
        to go to
        """
        mats = FakeMaterials('Sol', 'Venus', 12, 15, [ 'Iron' ] )
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Land at target", mats.res, True), ev.process( { 'event': 'ApproachBody', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol','Body': 'Venus'}, {} ))

    def test_approach_body_event_correct_system_already_targeted(self):
        """
        test when system and body match but we're already targeting a location
        then we just keep targeting that, so we don't jump around.
        """
        current_target = { 'target': 'fake' }
        mats = FakeMaterials('Sol', 'Venus', 12, 15, [ 'Iron' ] )
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Land at target", current_target, True), ev.process( { 'event': 'ApproachBody', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol','Body': 'Venus'}, {}, current_target ))

    def test_startup_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        mats = FakeMaterials('Sol', 'Earth')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Earth", mats.res, True), ev.process( { 'event': 'StartUp', 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'}, {} ))

    def test_touchdown_at_target(self):
        """
        test that we note success when we hit a target
        """
        visited = NoneVisited()
        mats = FakeMaterials('Sol', 'Earth', 13, 67, ['Iron', 'Gold'])
        ev = events.EventEngine(mats, ['Gold'], visited)
        res = ev.process( { 'event': 'Touchdown', 'Latitude': 13, 'Longitude': 67}, {'StarSystem': 'Sol', "Body": 'Earth', 'StarPos': [ 0, 0, 0]} )
        self.assertEqual("Collect Gold", res[0])
        self.assertFalse(res[2])
        self.assertEqual( mats.res, visited.captured_visit())

    def test_touchdown_at_target_wrong_case(self):
        """
        test that we note success when we hit a target but the dataset
        case doesn't match the ones from the events
        """
        visited = NoneVisited()
        mats = FakeMaterials('SOL', 'EARTH', 13, 67, ['Iron', 'Gold'])
        ev = events.EventEngine(mats, ['Gold'], visited)
        res = ev.process( { 'event': 'Touchdown', 'Latitude': 13, 'Longitude': 67}, {'StarSystem': 'Sol', 'Body': 'Earth', 'StarPos': [ 0, 0, 0]} )
        self.assertEqual("Collect Gold",res[0])
        self.assertFalse(res[2])
        self.assertEqual( mats.res, visited.captured_visit())
        
    def test_liftoff_event_wrong_system(self):
        """
        test when systems do not match we ask for the system to show
        """
        mats = FakeMaterials('Sol', 'Earth')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Go to Sol (12 Ly)", mats.res, False), ev.process( { 'event': 'Liftoff'}, {  'StarPos': [ 0, 0, 0] , 'StarSystem': 'Arcturus'} ))

    def test_liftoff_event_correct_system(self):
        """
        test when systems do match we ask for the planet(s) to show
        """
        mats = FakeMaterials('Sol', 'Mercury')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Supercruise to Sol Mercury", mats.res, True), ev.process( { 'event': 'Liftoff'}, { 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol'} ))

    def test_liftoff_event_correct_body(self):
        """
        test when we are lifting off from a body that has a site we have not
        yet visited - probably means multiple sites on a body
        """
        mats = FakeMaterials('Sol', 'Mercury', lat=1, lon=2)
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual(("Land at target", mats.res, True), ev.process( { 'event': 'Liftoff'}, { 'StarPos': [ 0, 0, 0] , 'StarSystem': 'Sol', 'Body': 'Mercury'} ))

    def test_short_body(self):
        mats = FakeMaterials('Sol', 'Mercury')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual("Earth", ev.short_body("Sol", "Earth"))
        self.assertEqual("1 a", ev.short_body("Achenar", "Achenar 1 a"))

    def test_make_params(self):
        mats = FakeMaterials('Sol', 'Mercury')
        ev = events.EventEngine(mats, None, NoneVisited())
        self.assertEqual( { 'a': 1} , ev.make_params({ 'a': 1 }, { 'a': 2 }))
        self.assertEqual( { 'a': 2, 'b': 2} , ev.make_params({ 'b': 2 }, { 'a': 2 }))
        self.assertEqual( { 'ShortBody': 'Mars', 'Body': 'Mars', 'StarSystem': 'Sol'} , ev.make_params({ 'StarSystem': 'Sol' }, { 'Body': 'Mars' }))
        self.assertEqual( { 'ShortBody': '1', 'Body': 'Achenar 1', 'StarSystem': 'Achenar'} , ev.make_params({ 'StarSystem': 'Achenar' }, { 'Body': 'Achenar 1' }))
        

if __name__ == '__main__':
    unittest.main()
