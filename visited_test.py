#!/usr/bin/env python3

import unittest
import visited

class VisitedTest(unittest.TestCase):
    def test_visited_recently(self):
        v = visited.Visited()
        v.visit( { 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, 
                 when = 1000 )
        self.assertTrue(v.is_visited({ 'system': 'Sol', 'body': 'Earth', 'lat': 0, 'lon': 0 }, when=1000))


if __name__ == '__main__':
    unittest.main()
