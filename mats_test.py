#!/usr/bin/env python3

import mats
import unittest

class NoneVisited():
    def is_visited(self, loc):
        if 'system' not in loc: 
            raise ValueError("Should be passed a location with a system")
        return False

class AllVisited():
    def is_visited(self, loc):
        if 'system' not in loc: 
            raise ValueError("Should be passed a location with a system")
        return True

class MaterialsTest(unittest.TestCase):
    def test_names(self):
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertEqual(set([ "Carbon", "Iron", "Nickel", "Phosphorus", "Sulphur",
    "Chromium", "Manganese", "Zirconium", "Mercury", "Tungsten",
    "Antimony", "Tin", "Germanium" ]), m.names())

    def test_closest(self):
        """
        Tests a system is chosen where the mat is present
        """
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertEqual( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Tungsten'])[1]['system'])
        self.assertEqual( '2MASS J10433563-5945136', m.closest([0, 0, 0], ['Germanium'])[1]['system'])

    def test_closest_common_mats(self):
        """
        Test when a mat is present in both systems that the closest is 
        chosen
        """
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertEqual( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Iron'])[1]['system'])
        self.assertEqual( '2MASS J10433563-5945136', m.closest([8000, 0, 3000], ['Iron'])[1]['system'])

    def test_closest_multiple_mats(self):
        """
        Check that the closest system with any of the required mats is 
        chosen
        """
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertEqual( '164 G. Canis Majoris', m.closest([0, 0, 0], ['Tungsten', 'Germanium'])[1]['system'])
        self.assertEqual( '2MASS J10433563-5945136', m.closest([8000, 0, 3000], ['Tungsten', 'Germanium'])[1]['system'])

    def test_closest_all_visited(self):
        """
        Check that when all the systems are visited recently we don't 
        return any
        """
        m = mats.Materials("mats_test.json", AllVisited())
        self.assertEqual( (None, None), m.closest([0, 0, 0], ['Tungsten', 'Germanium']))
        self.assertEqual( (None, None), m.closest([8000, 0, 3000], ['Tungsten', 'Germanium']))

    def test_matches(self):
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertTrue( m.matches( { 'system': '164 G. Canis Majoris', 'body': '5 c a', "lat": -4.8631, "lon": 3.0394 }))
        self.assertFalse( m.matches( { 'system': '165 G. Canis Majoris', 'body': '5 c a', "lat": -4.8631, "lon": 3.0394 }))
        self.assertFalse( m.matches( { 'system': '164 G. Canis Majoris', 'body': '5 c b', "lat": -4.8631, "lon": 3.0394 }))
        self.assertFalse( m.matches( { 'system': '164 G. Canis Majoris', 'body': '5 c a', "lat": 4.8631, "lon": 3.0394 }))
        self.assertFalse( m.matches( { 'system': '164 G. Canis Majoris', 'body': '5 c a', "lat": -4.8631, "lon": 7.0394 }))
        
    def test_matches_case_insensitive(self):
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertTrue( m.matches( { 'system': '164 G. canis majoris', 'body': '5 C A', "lat": -4.8631, "lon": 3.0394 }))

    def test_matches_all_visited(self):
        m = mats.Materials("mats_test.json", AllVisited())
        self.assertFalse( m.matches( { 'system': '164 G. Canis Majoris', 'body': '5 c a', "lat": -4.8631, "lon": 3.0394 }))

    def test_local(self):
        """
        Check we can get all the local sites (on the same body) 
        """
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertTrue( m.local( '164 G. Canis Majoris', '5 c a'))
        self.assertFalse( m.local( '164 G. Canis Majoris', '5 c b'))

    def test_local_visited(self):
        """
        Check we can get all the local sites (on the same body) 
        """
        m = mats.Materials("mats_test.json", AllVisited())
        self.assertFalse( m.local( '164 G. Canis Majoris', '5 c a'))

    def test_local_case_insensitive(self):
        """
        Check we can get all the local sites (on the same body) 
        """
        m = mats.Materials("mats_test.json", NoneVisited())
        self.assertTrue( m.local( '164 G. canis majoris', '5 C A'))

if __name__ == "__main__":
    unittest.main()
        
