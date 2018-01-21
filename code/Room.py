#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Room class.

Author: Xian Lai
Date: Dec.21, 2017
"""

from math import factorial as f
from collections import Counter
import random


class Room(object):

    """
    This class defines the room objects. A room is identified by a collection
    of walls. Wall is implemented in Wall class. When initializing, a room 
    always starts from a 3 by 3 square consisted of 4 walls.

    Inputs:
    -------
    - type: room type like hallway, service room, etc.
    - id: room id which should be the same as its index in walls list
    - walls: the walls enclose this room
    
    Attributes:
    -----------
    - walls: the walls it has.
    - type: room type
    - id: room id
    - stats: a dictionary of its properties like area, type, convexAspect, etc.
    - adjacency: adjacent rooms and corresponding types
    - center: the center point of room. Center point is calculated by taking
        the average of xs and ys of walls' end points. It's possible that this
        center point will fall outside the boundary of room. 

    Methods:
    --------
    - update_stats: update the stats of this room given walls
    """

    def __init__(self, rm_type, rm_id, walls, openings=None, timer=9999, silent=False):
        """ self.n is the number of variables in a state defined in this problem.
        self.domains is a nested list of the possible values for every variable.
        """
        self.walls = self.init_walls()
        self.type = rm_type
        self.id = rm_id
        self.openings = openings
        self.area = 1.0
        self.car = 1.0
        self.center = (1,1,1)
        self.adjRms = 1
        self.adjTypes = 1
        self.escapeDist = 1

    def initialize(self, ):
        """
        """
        pass


    def init_walls(self):
        """
        """
        pass

    def switch_id(self,):
        """
        """
        pass





def main():

    pass

if __name__ == "__main__":
    main()