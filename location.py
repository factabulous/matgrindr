# -*- coding: utf-8 -*-

class Location():
    """
    Class to store the location for a CMDR. This is the star 
    position (x,y,z), system, body, lat and lon. Not all are 
    always present.
    """

    def __init__(self):
        self._loc = {}

    def set( self, system = None, body = None, pos = None, latlon = None):
        if system:
            self._loc['system'] = system
        if body:
            self._loc['body'] = body
        if latlon:
            if len(latlon) ==2:
                self._loc['lat'] = latlon[0]
                self._loc['lon'] = latlon[1]
            else:
                raise ValueError("Expected latlon to be length 2")
        if pos:
            if len(pos) ==3:
                self._loc['x'] = pos[0]
                self._loc['y'] = pos[1]
                self._loc['z'] = pos[2]
            else:
                raise ValueError("Expected pos to be length 3")

    def valid(self):
        """
        Indicates we have at least some location information - at least a
        star position and a system name
        Note that we just check for 'x' as we only (at the moment) have ways
        to set all 3 of x, y, and z at the same time.
        """

        return 'x' in self._loc and 'system' in self._loc and self._loc['system']

    def has_latlon(self):
        """
        Checks we have latitude and longitude (in lat and lon). Actually
        only checks one as they are always set in a pair
        """
        return 'lat' in self._loc

    def has_body(self):
        """
        Checks we have a body available
        """
        return 'body' in self._loc

    def get(self):
        """
        Returns a copy of the location info
        """
        return self._loc.copy()
