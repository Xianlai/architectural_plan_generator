#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Wall class.
Author: Xian Lai
Date: Oct.29, 2017
"""

from shapely.geometry import Point, LineString, Polygon

class Wall(LineString):

    """
    The wall class implements the real-world wall objects. It has states 
    attributes including the id, 2 end points, the opening, 2 rooms it belongs  
    to, thickness, material etc. In the searching process, we will abstract it 
    into a line with 1 id, 2 end points, 1 opening and 2 owning rooms. The  
    other attributes will be implemented later when needed in other problems.

    Inputs:
    -------
    - wid  : the id of this wall
    - ends : 2 end points, (left, right) or (upper, lower).
    - rids : the list of ids of 2 rooms this wall belongs to
    
    Attributes:
    -----------
    - wid    : wall id
    - ends   : 2 end points
    - rid    : the room it belongs to
    - opening: the stats of opening it has: location, type
    - stats  : The stats of this wall is encoded as a dictionary: 
        {
        normalDir: The normal direction of wall,
        same     : The same wall that belong to another room
        thickness: (Not in use for now.) 
        material: (Not in use for now.)
        }

    Methods:
    --------
    - parse: parse the states attributes to get stats attributes.
    """

    def __init__(self, ends, wid, rid):
        """ Init a wall object with the wall id, 2 end points and 2 owning 
        rooms. When initialize, the opening type and location is always 0.
        """
        LineString.__init__(self, ends)
        self.wid     = wid
        self.rid     = rid
        self.opening = [0, 0]
        self.parse()


    def parse(self,):
        """ parse the states attributes to get stats attributes.
        """
        # parse normal direction: x-axis:0, y-axis:1
        if self.coords[0][0] == self.coords[1][0]: normal = 0
        else: normal = 1

        self.stats = {
            'normalDir':normal, 
            'same':None
        }

    

def main():
    wall_0 = Wall(wid=0, rid=1, ends=((0, 0), (0, 1)))
    wall_1 = Wall(wid=0, rid=1, ends=((0, 0), (0, 1)))
    print(wall_0.stats)
    print(wall_0 == wall_1)
    print(wall_0.length)

if __name__ == "__main__":
    main()