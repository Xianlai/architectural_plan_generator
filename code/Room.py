#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Room class.

Author: Xian Lai
Date: Dec.21, 2017
"""


from Wall import Wall
from shapely.geometry import Point, LineString, Polygon

class Room(Polygon):

    """
    The room class implements the real-world room objects. It has states 
    attributes include the rid, the enclosing walls, the room function etc. 
    And stats attribtues include room area, convex aspect ratio, etc. When 
    initializing, a room always starts from a 3 by 3 square consisted of 4 
    walls without openings.

    Inputs:
    -------
    - rid: room id which should be the same as its index in walls list
    - function: room function like hallway, service room, etc.
    - walls: the walls enclose this room
    
    Attributes:
    -----------
    - rid: room id
    - walls: the walls it has.
    - function: room function
    - stats: a dictionary of its properties:
        {
        'area':0,
        'convexAspect':0.0,
        'adjacency':[rooms, functions],
        'escapeDist':0,
        'center': the center point of room for adding room tags,
        }

    Methods:
    --------
    - parse: parse the stats of this room given states
    """

    def __init__(self, rid, function, walls):
        """ 
        """
        Polygon.__init__(self, [wall.coords[0] for wall in walls])
        self.rid   = rid
        self.func  = function
        self.walls = walls
        self.parse()
        

    def parse(self, ):
        """
        """
        self.stats = {
            'area':self.area,
            'center':self.centroid,
            'convexAspect':calc_convex_aspect(self.bounds),
            'adjacency':[wall.stats['same'].rid for wall in self.walls \
                if wall.stats['same'] != None],
            'escapeDist':0.0
        }
        print(self.stats)






def calc_convex_aspect(bounds):
    """
    """
    minx, miny, maxx, maxy = bounds
    aspect = (maxx-minx)/(maxy-miny)
    return max(aspect, 1/aspect)



def main():
    wall_0 = Wall(wid=0, rid=0, ends=((0, 0), (0, 1)))
    wall_1 = Wall(wid=1, rid=0, ends=((0, 1), (1, 1)))
    wall_2 = Wall(wid=1, rid=0, ends=((1, 1), (1, 0)))
    wall_3 = Wall(wid=1, rid=0, ends=((1, 0), (0, 0)))

    walls = [wall_0, wall_1, wall_2, wall_3]
    room = Room(rid=0, function='test', walls=walls)
    print(room.area)
    print(room.length)
    print(list(room.exterior.coords))


if __name__ == "__main__":
    main()