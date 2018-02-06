# -*- coding: utf-8 -*-

import math

def heading(start, end):
    """
    Find how to get from the point on a planet specified as a tuple start
    to a point specified in the tuple end
    """
    start = ( math.radians(start[0]), math.radians(start[1]))
    end = ( math.radians(end[0]), math.radians(end[1]))

    delta_lon = end[1] - start[1]
    delta_lat = math.log(math.tan(math.pi/4 + end[0]/2)/math.tan(math.pi/4 + start[0]/2))
    return int(round((360 + math.degrees(math.atan2(delta_lon, delta_lat))) % 360))
