#!/usr/bin/env python3

import heading
import unittest

class HeadingTest(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(90, heading.heading((0, 0), (0, 45)))
        self.assertEqual(264, heading.heading((10, 20), (-10, -170)))
        self.assertEqual(185, heading.heading((90, 179), (0, 0)))

    def test_great_circle(self):
        self.assertEqual(87, heading.great_circle((0, 0), (0, 10), 500))
        self.assertEqual(87, heading.great_circle((0, 0), (0, -10), 500))
        self.assertEqual(87, heading.great_circle((0, 0), (-10, 0), 500))
        self.assertEqual(87, heading.great_circle((0, 0), (10, 0), 500))
        self.assertEqual(174, heading.great_circle((0, 0), (0, 20), 500))

    def test_angle_of_descent(self):
        """
        Works out the rate of descent needed to hit zero height at the 
        given end point
        """
        self.assertEqual(45, heading.angle_of_descent((0,0), (0,10), radius=500, height=87))
        self.assertEqual(63, heading.angle_of_descent((0,0), (0,10), radius=500, height=174))
        # Make sure we have a cut-off at 30 degrees
        self.assertEqual(30, heading.angle_of_descent((0,0), (0,10), radius=500, height=50))
        self.assertEqual(0, heading.angle_of_descent((0,0), (0,10), radius=500, height=49))
        # What happens when we are a long way off
        self.assertEqual(0, heading.angle_of_descent((0,0), (0,160), radius=500, height=300))
        


if __name__ == "__main__":
    unittest.main()
   
