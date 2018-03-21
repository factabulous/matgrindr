#!/usr/bin/env python3

import unittest
import visited

class VisitedTest(unittest.TestCase):

    def test_visited_recently(self):
        """
        Checks that the visited state is remembered and expires after time
        """
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000 + 7 * 24 * 3600))

    def test_visited_recently_with_respawn(self):
        """
        Checks that the visited state is remembered and expires after time
        """
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0, 'respawn_days': 5 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000 + 5 * 24 * 3600))

    def test_visited_recently_with_no_respawn(self):
        """
        Checks that the visited state is remembered and we understand zero
        periods
        """
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0, 'respawn_days': 0 }, 
                 when = 1000 )
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))

    def test_visited_case_sensitivity(self):
        """
        Checks that the store is not case sensitve
        """
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'SOL', 'body': 'EARTH', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertFalse(v.is_visited({ 'system': 'SOL', 'body': 'EARTH', 'lat': 0, 'lon': 0 }, when=1000 + 7 * 24 * 3600))

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

    def test_never_visited(self):
        v = visited.Visited()
        self.assertFalse(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))

    def test_save(self):
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertNotEqual('[]', v.save(when=1000))
        self.assertEqual('[]', v.save(when=1000 + 7 * 24 * 3600))

    def test_is_dirty(self):
        v = visited.Visited()
        self.assertFalse(v.is_dirty())
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_dirty())
        v.save()

        self.assertFalse(v.is_dirty())
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1001 )
        self.assertTrue(v.is_dirty())

if __name__ == '__main__':
    unittest.main()
