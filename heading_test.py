#!/usr/bin/env python3

import heading
import unittest

class HeadingTest(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(90, heading.heading((0, 0), (0, 45)))
        self.assertEqual(264, heading.heading((10, 20), (-10, -170)))
        self.assertEqual(185, heading.heading((90, 179), (0, 0)))

    def test_great_circle(self):
        self.assertAlmostEqual(87.266, heading.great_circle((0, 0), (0, 10), 500), places=3)
        self.assertAlmostEqual(87.266, heading.great_circle((0, 0), (0, -10), 500), places=3)
        self.assertAlmostEqual(87.266, heading.great_circle((0, 0), (-10, 0), 500), places=3)
        self.assertAlmostEqual(87.266, heading.great_circle((0, 0), (10, 0), 500), places=3)
        self.assertAlmostEqual(174.533, heading.great_circle((0, 0), (0, 20), 500), places=3)

    def test_angle_of_descent(self):
        """
        Works out the rate of descent needed to hit zero height at the 
        given end point
        """
        self.assertEqual(45, heading.angle_of_descent((0,0), (0,10), radius=500, height=87000))
        self.assertEqual(63, heading.angle_of_descent((0,0), (0,10), radius=500, height=174000))
        self.assertEqual(30, heading.angle_of_descent((0,0), (0,10), radius=500, height=50000))
        self.assertEqual(29, heading.angle_of_descent((0,0), (0,10), radius=500, height=49000))
        # What happens when we are a long way off
        self.assertEqual(12, heading.angle_of_descent((0,0), (0,160), radius=500, height=300000))
        

        

if __name__ == "__main__":
    unittest.main()
   
