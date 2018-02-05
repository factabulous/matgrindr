#!/usr/bin/env python3

import mats
import unittest

class MaterialsTest(unittest.TestCase):
    def test_names(self):
        m = mats.Materials("mats_test.json")
        self.assertEqual(set([ "Carbon", "Iron", "Nickel", "Phosphorus", "Sulphur",
    "Chromium", "Manganese", "Zirconium", "Mercury", "Tungsten",
    "Antimony" ]), m.names())

    def test_closest(self):
        m = mats.Materials("mats_test.json")
        self.assertEquals( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Tungsten'])['system'])

if __name__ == "__main__":
    unittest.main()
        
