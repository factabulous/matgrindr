# -*- coding: utf-8 -*-

import json
import math

class Materials():
    def __init__(self, filename, visited = None):
        self.visited = visited
        with open(filename, "rt") as mats_file:
            self.materials = json.load(mats_file)

    def names(self):
        """
        Return the set of all materials we can find
        """
        res = set()
        for loc in self.materials:
            res.update(loc['materials'])
        return res

    def distance(self, mat, loc):
        """
        Returns the distance between a mat (with coords in "x", "y", "z"
        fields) and a loc (tuple of x, y, z)
        """
        return math.sqrt( 
            math.pow( mat['x'] - loc[0], 2) + 
            math.pow( mat['y'] - loc[1], 2) + 
            math.pow( mat['z'] - loc[2], 2))

    def closest(self, loc, mats):
        """
        Returns the closest site that contains any of the materials in the mats
        list. loc is a tuple / array of x,y,z coords
        """
        mats = set(mats)
        res = sorted( ( self.distance(mat, loc), mat) for mat in self.materials if set(mat['materials']).intersection(mats) and (not self.visited or not self.visited.is_visited(loc)))
        if res:
            return res[0][1]
        return None

    def matches(self, loc):
        """
        Returns the material location for this location, or None if this is 
        not a known location. lat and lon are allowed to differ slightly
        """
        if self.visited.is_visited(loc):
            return None

        for m in self.materials:
            if m['system'] == loc['system'] and m['body'] == loc['body'] and math.fabs(m['lat'] - loc['lat']) < 3 and math.fabs(m['lon'] - loc['lon']) < 3:
                return m
        return None

    def local( self, system, body):
        """
        Returns all the locations on the given body that have not already
        been visited.

        Returns a list - can be empty, but not None
        """

        locs = []
        
        for m in self.materials:
            if m['system'] == system and m['body'] == body and not self.visited.is_visited(m):
                locs.append(m)
        return locs

