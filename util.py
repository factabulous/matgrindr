# -*- coding: utf-8 -*-

import os

def error(str):
    """
    Output error information to the EDMC logfile - prepends the 
    plugin name
    """
    print('[matgrindr] ' + str)

def debug(str):
    """
    Output debug information to the EDMC logfile - prepends the 
    plugin name
    """
    if os.path.exists(local_file("debug.txt")):
        print('[matgrindr] ' + str)

def local_file(name):
    """
    Returns the full path to a filenam inside the plugin area
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def same(left, right):
    """
    Used for testing that thing link system names are the same (they 
    can be supplied in different cases - upper or lower). 
    returns True if they should be treated as the same
    """
    return left.upper() == right.upper()

class GridHelper():
    """
    Helper for Tk grid formatting - vends row and col numbers
    so that I don't have to keep altering them ;)
    """

    def __init__(self):
        self._row = 0
        self._col = 0

    def col(self, columnspan = 1):
        """
        Returns the next column
        """
        v = self._col
        self._col = self._col + columnspan
        return v

    def row(self):
        """
        Returns the current row (does not increment - use newrow() for that)
        """
        return self._row

    def newrow(self):
        self._row = self._row + 1
        self._col = 0
        return self._row


