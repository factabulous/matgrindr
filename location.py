# -*- coding: utf-8 -*-

class Location():
    """
    Class to store the location for a CMDR. This is the star 
    position (x,y,z), system, body, lat and lon. Not all are 
    always present.
    """

    def __init__(self):
        self._loc = {}
        self._is_dirty = False

    def change_system(self, system, pos):
        """
        Location switches systems(s). The body and latlon are invalidated.
        """
        if 'system' not in self._loc or self._loc['system'] != system:
            self._loc['system'] = system
            self._loc['x'] = pos[0]
            self._loc['y'] = pos[1]
            self._loc['z'] = pos[2]
            if 'body' in self._loc:
                del self._loc['body']
            if 'lat' in self._loc:
                del self._loc['lat']
                del self._loc['lon']
            self._is_dirty = True
        return self

    def landed(self, is_landed = True):
        """
        Set whether we are landed somewhere
        """
        if self.is_landed() != is_landed:
            self._loc['landed'] = is_landed
            self._is_dirty = True

    def is_landed(self):
        """
        Indicates whether we think we are landed
        """
        if 'landed' in self._loc:
            return self._loc['landed']
        return False

    def change_body(self, body):
        """
        Change the body within the sytem - latlon would be invalid, system
        is retained
        """
        if 'body' not in self._loc or self._loc['body'] != body:
            self._loc['body'] = body
            if 'lat' in self._loc:
                del self._loc['lat']
                del self._loc['lon']
            self._is_dirty = True
        return self

    def change_latlon(self, lat, lon):
        self._loc['lat'] = lat
        self._loc['lon'] = lon
        self._is_dirty = True
        return self

    def has_latlon(self):
        """
        Checks we have latitude and longitude (in lat and lon). Actually
        only checks one as they are always set in a pair
        """
        return 'lat' in self._loc

    def has_system(self):
        """
        Checks we know which system we are in (name and position)
        """
        return 'system' in self._loc and 'x' in self._loc

    def has_body(self):
        """
        Checks we have a body available
        """
        return 'body' in self._loc

    def get(self):
        """
        Returns a copy of the location info - resets the dirty flag 
        as it is assumed you now know the new state
        """
        self._is_dirty = False
        return self._loc.copy()

    def is_changed(self):
        """
        Indicates if the location has changed since last read via get()
        and also resets the 'changed' flag so a subsequent read will 
        indicate no changes
        """
        changed = self._is_dirty
        self._is_dirty = False
        return changed

    def pos(self):
        """
        Returns the star position as a tuple with x, y, z values
        """
        if 'x' in self._loc:
            return ( self._loc['x'], self._loc['y'], self._loc['z'] )
        return None

    def latlon(self):
        if 'lat' in self._loc:
            return ( self._loc['lat'], self._loc['lon'] )
        return None

    def system(self):
        return self._loc['system'] if 'system' in self._loc else None

    def body(self):
        return self._loc['body'] if 'body' in self._loc else None

