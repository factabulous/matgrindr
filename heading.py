# -*- coding: utf-8 -*-

from math import log, radians, degrees, sin, pi, tan, cos, asin, atan2, fabs, sqrt

def heading(start, end):
    """
    Find how to get from the point on a planet specified as a tuple start
    to a point specified in the tuple end
    """
    start = ( radians(start[0]), radians(start[1]))
    end = ( radians(end[0]), radians(end[1]))

    delta_lon = end[1] - start[1]
    delta_lat = log(tan(pi/4 + end[0]/2)/tan(pi/4 + start[0]/2))
    return int(round((360 + degrees(atan2(delta_lon, delta_lat))) % 360))

def great_circle(start, end, radius):
    start = ( radians(start[0]), radians(start[1]))
    end = ( radians(end[0]), radians(end[1]))
    delta_lat = fabs(start[0] - end[0])
    delta_lon = fabs(start[1] - end[1])

    delta = 2 * asin( sqrt( 
        pow(sin(delta_lat / 2), 2) + cos(start[0]) * cos(end[0]) * pow(sin(delta_lon/2), 2)))
    return radius * delta

def angle_of_descent(start, end, height, radius):
    """
    Works out the angle of descent needed to hit zero height at the 
    given end point
    """
    horz_distance = great_circle(start, end, radius)
    angle = atan2(-height, horz_distance)
    return int(round(degrees(angle)))

def target_info(now, goal, height, radius):
    """
    Returns a dict with (heading, distance, descent_angle) to make
    it easier to gather this information
    """
    return { 
        "heading": heading(now, goal),
        "distance": great_circle(now, goal, radius),
        "descent_angle": angle_of_descent(now, goal, height, radius)
    }
