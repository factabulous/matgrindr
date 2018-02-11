#!/usr/bin/env python3

import unittest
import util

class UtilTestCase(unittest.TestCase):
    def test_same(self):
        self.assertTrue(util.same("This", "This"))
        self.assertTrue(util.same("This", "THIS"))
        self.assertFalse(util.same("THIS", "THAT"))

    def test_grid_helper(self):
        h = util.GridHelper()
        self.assertEqual(0, h.col())
        self.assertEqual(1, h.col())
        self.assertEqual(2, h.col())
        self.assertEqual(3, h.col())
        self.assertEqual(0, h.row())
        self.assertEqual(1, h.newrow())
        self.assertEqual(0, h.col())
        self.assertEqual(1, h.row())
    
    def test_grid_helper_columnspan(self):
        """
        Shows that specifying how many columns to span causes col to 
        skip the spanned columns
        """
        h = util.GridHelper()
        self.assertEqual(0, h.col(3))
        self.assertEqual(3, h.col())

if __name__ == "__main__":
    unittest.main()
