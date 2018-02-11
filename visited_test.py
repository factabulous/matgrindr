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

    def test_visited_case_sensitivity(self):
        """
        Checks that the store is not case sensitve
        """
        v = visited.Visited()
        v.set_visited( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'SOL', 'body': 'EARTH', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertFalse(v.is_visited({ 'system': 'SOL', 'body': 'EARTH', 'lat': 0, 'lon': 0 }, when=1000 + 7 * 24 * 3600))

    def test_visited_planet_body_name_long(self):
        """
        Checks that the store handles bodies that are prefixed by their
        system name
        """
        v = visited.Visited()
        v.set_visited( { 'system': 'Synuefe Sector AA-A c2-12', 'body': '5', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Synuefe Sector AA-A c2-12', 'body': '5', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertTrue(v.is_visited({ 'system': 'Synuefe Sector AA-A c2-12', 'body': 'Synuefe Sector AA-A c2-12 5', 'lat': 0, 'lon': 0 }, when=1000))

        # In these cases we stored the longform so we can't test the shortform
        # I think that is ok for now
        v.set_visited( { 'system': 'Synuefe Sector BB-B c2-12', 'body': 'Synuefe Sector BB-B c2-12 5', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertFalse(v.is_visited({ 'system': 'Synuefe Sector BB-B c2-12', 'body': '5', 'lat': 0, 'lon': 0 }, when=1000))
        self.assertTrue(v.is_visited({ 'system': 'Synuefe Sector BB-B c2-12', 'body': 'Synuefe Sector BB-B c2-12 5', 'lat': 0, 'lon': 0 }, when=1000))

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
