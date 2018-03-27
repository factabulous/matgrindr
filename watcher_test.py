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

if __name__ == "__main__":
    unittest.main()
        
