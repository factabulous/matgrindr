#!/usr/bin/env python3

import unittest
import location

class LocationTest(unittest.TestCase):

    def test_set(self):
        loc = location.Location()

        loc.set( system = "Sol", pos = ( 1, 2, 3), body = 'Earth', latlon = ( 4, 5))

        self.assertTrue(loc.valid())
        self.assertTrue(loc.has_body())
        self.assertTrue(loc.has_latlon())

        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth', 'lat': 4, 'lon': 5 }, loc.get())

if __name__ == "__main__":
     unittest.main()
