#!/usr/bin/env python3

import heading
import unittest

class HeadingTest(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(90, heading.heading((0, 0), (0, 45)))
        self.assertEqual(264, heading.heading((10, 20), (-10, -170)))
        self.assertEqual(185, heading.heading((90, 179), (0, 0)))

if __name__ == "__main__":
    unittest.main()
   
