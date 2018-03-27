#!/usr/bin/env python3

import watcher
import unittest

class WatcherTest(unittest.TestCase):
    def test_watcher_parse(self):
        """
        Tests that we can use the watcher that downloads from 
        a CSV and can populate a hash
        """
        m = watcher.MatsLoaderRemote("file", None)
        res = m.parse("A\tB\nJim\tBob\nBill\tJames\n")
        self.assertEqual([ { "A": "Jim", "B": "Bob" }, { "A": "Bill", "B": "James" }], res)

    def test_detect(self):
        m = watcher.MatsLoaderRemote("file", None)
        self.assertEqual(12, m.detect("12"))
        self.assertEqual(-12, m.detect("-12"))
        self.assertEqual(12.89, m.detect("12.89"))
        self.assertEqual("12.A89", m.detect("12.A89"))

    def _test_watcher_parses_ints(self):
        """
        Tests that values that can be integers are parsed as such 
        """
        m = watcher.MatsLoaderRemote("file", None)
        res = m.parse("A\tB\n1\t2\n3\t4\n")
        self.assertEqual([ { "A": 1, "B": 2 }, { "A": 3, "B": 4 }], res)



if __name__ == "__main__":
    unittest.main()
        
