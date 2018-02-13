#!/usr/bin/env python3

import unittest
import location

class LocationTest(unittest.TestCase):

    def test_set(self):
        """
        Simple test - all parts of the location are set and then tested
        """
        loc = location.Location()

        loc.set( system = "Sol", pos = ( 1, 2, 3), body = 'Earth', latlon = ( 4, 5))

        self.assertTrue(loc.valid())
        self.assertTrue(loc.has_body())
        self.assertTrue(loc.has_latlon())

        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth', 'lat': 4, 'lon': 5 }, loc.get())

    def test_set_no_body(self):
        """
        Set with no body specified - which is Ok. More specific info 
        like the latlon should not be stored
        """
        loc = location.Location()

        loc.set( system = "Sol", pos = ( 1, 2, 3), latlon = ( 4, 5))

        self.assertTrue(loc.valid())
        self.assertFalse(loc.has_body())
        self.assertFalse(loc.has_latlon())

        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3 }, loc.get())

    def test_remove_latlon(self):
        loc = location.Location()

        loc.set( system = "Sol", pos = ( 1, 2, 3), body = 'Earth', latlon = ( 4, 5))
        self.assertTrue(loc.has_latlon())
        loc.remove_latlon()

        self.assertFalse(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth' }, loc.get())

if __name__ == "__main__":
     unittest.main()
