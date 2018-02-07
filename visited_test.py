#!/usr/bin/env python3

import unittest
import visited

class VisitedTest(unittest.TestCase):

    def test_visited_recently(self):
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000 + 7 * 24 * 3600))

    def test_visited_multiple_times(self):
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000 + 7 * 24 * 3600))
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 3000 )
        # Now should be using the new recorded visit at 3000 secs
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000 + 7 * 24 * 3600))
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=3000 + 7 * 24 * 3600))

    def test_save(self):
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertNotEqual('[]', v.save(when=1000))
        self.assertEqual('[]', v.save(when=1000 + 7 * 24 * 3600))


if __name__ == '__main__':
    unittest.main()
