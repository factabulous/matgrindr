#!/usr/bin/env python3

import unittest
import location

class LocationTest(unittest.TestCase):

    def test_change_system(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3))
        self.assertTrue(loc.is_changed())
        self.assertTrue(loc.has_system())
        self.assertFalse(loc.has_body())
        self.assertFalse(loc.has_latlon())
        self.assertEqual('Sol', loc.system())
        self.assertIsNone(loc.body())
        self.assertIsNone(loc.latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3 }, loc.get())
        self.assertEqual( (1, 2, 3), loc.pos())

    def test_change_body(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3))
        loc.change_body("Earth")
        self.assertTrue(loc.is_changed())
        self.assertTrue(loc.has_system())
        self.assertTrue(loc.has_body())
        self.assertFalse(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth' }, loc.get())
        self.assertEqual('Earth', loc.body())
        self.assertIsNone(loc.latlon())

    def test_change_latlon(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3)).change_body("Earth").change_latlon(4, 5)
        self.assertTrue(loc.has_system())
        self.assertTrue(loc.has_body())
        self.assertTrue(loc.has_latlon())
        self.assertEqual( { 'system': 'Sol', 'x': 1, 'y': 2, 'z': 3, 'body': 'Earth', 'lat': 4, 'lon': 5 }, loc.get())
        self.assertEqual( (4,5), loc.latlon())

    def test_reset_body(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3)).change_body("Earth").change_latlon(4, 5).change_body('Mercury')
        self.assertTrue(loc.has_system())
        self.assertTrue(loc.has_body())
        self.assertFalse(loc.has_latlon())

    def test_landing(self):
        loc = location.Location()
        self.assertFalse(loc.is_landed())
        loc.landed()
        self.assertTrue(loc.is_landed())
        loc.landed(False)
        self.assertFalse(loc.is_landed())

    def test_reset_system(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3)).change_body("Earth").change_latlon(4, 5).change_system('Sirius', ( 6, 7, 8))
        self.assertTrue(loc.has_system())
        self.assertFalse(loc.has_body())
        self.assertFalse(loc.has_latlon())

    def test_dirty_flag(self):
        loc = location.Location()
        loc.change_system("Sol", (1, 2, 3))
        self.assertTrue(loc.is_changed())
        self.assertFalse(loc.is_changed()) # Reading the flag should reset it
        loc.change_system("Sol", (1, 2, 3))
        # Still not dirty - is same system
        self.assertFalse(loc.is_changed())
        loc.change_system("Arcturus", (1, 2, 5))
        self.assertTrue(loc.is_changed())

if __name__ == "__main__":
     unittest.main()
