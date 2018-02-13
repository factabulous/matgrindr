#!/usr/bin/env python3

import unittest
import location

class LocationTest(unittest.TestCase):

    def test_change_system(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3))
        self.assertTrue(loc.has_system())
        self.assertFalse(loc.has_body())
        self.assertFalse(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3 }, loc.get())

    def test_change_body(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3))
        loc.change_body("Earth")
        self.assertTrue(loc.has_system())
        self.assertTrue(loc.has_body())
        self.assertFalse(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth' }, loc.get())

    def test_change_latlon(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3)).change_body("Earth").change_latlon(4, 5)
        self.assertTrue(loc.has_system())
        self.assertTrue(loc.has_body())
        self.assertTrue(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth', 'lat': 4, 'lon': 5 }, loc.get())

    def test_reset_body(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3)).change_body("Earth").change_latlon(4, 5).change_body('Mercury')
        self.assertTrue(loc.has_system())
        self.assertTrue(loc.has_body())
        self.assertFalse(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Mercury' }, loc.get())

    def test_reset_system(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3)).change_body("Earth").change_latlon(4, 5).change_system('Sirius', ( 6, 7, 8))
        self.assertTrue(loc.has_system())
        self.assertFalse(loc.has_body())
        self.assertFalse(loc.has_latlon())
        self.assertEqual( { 'system': 'Sirius', 'x': 6, 'y': 7, 'z': 8 }, loc.get())
if __name__ == "__main__":
     unittest.main()
