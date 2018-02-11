# -*- coding: utf-8 -*-

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


