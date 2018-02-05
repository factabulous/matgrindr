#!/usr/bin/env python3

import mats
import unittest

class MaterialsTest(unittest.TestCase):
    def test_names(self):
        m = mats.Materials("mats_test.json")
        self.assertEqual(set([ "Carbon", "Iron", "Nickel", "Phosphorus", "Sulphur",
    "Chromium", "Manganese", "Zirconium", "Mercury", "Tungsten",
    "Antimony", "Tin", "Germanium" ]), m.names())

    def test_closest(self):
        """
        Tests a system is chosen where the mat is present
        """
        m = mats.Materials("mats_test.json")
        self.assertEqual( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Tungsten'])['system'])
        self.assertEqual( '2MASS J10433563-5945136', m.closest([0, 0, 0], ['Germanium'])['system'])

    def test_closest_common_mats(self):
        """
        Test when a mat is present in both systems that the closest is 
        chosen
        """
        m = mats.Materials("mats_test.json")
        self.assertEqual( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Iron'])['system'])
        self.assertEqual( '2MASS J10433563-5945136', m.closest([8000, 0, 3000], ['Iron'])['system'])

    def test_closest_multiple_mats(self):
        """
        Check that the closest system with any of the required mats is 
        chosen
        """
        m = mats.Materials("mats_test.json")
        self.assertEqual( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Tungsten', 'Germanium'])['system'])
        self.assertEqual( '2MASS J10433563-5945136', m.closest([8000, 0, 3000], ['Tungsten', 'Germanium'])['system'])


if __name__ == "__main__":
    unittest.main()
        
