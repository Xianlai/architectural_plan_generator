#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Wall class.
Author: Xian Lai
Date: Oct.29, 2017
"""

from math import factorial as f
from collections import Counter
import random
from LocalSearch import LocalSearch


class Wall():

    """
    This class implements the wall objects. A wall object is identified by 2 
    end points, its opening and the 2 rooms it belongs to. 

    Inputs:
    -------
    - ends: 2 end points
    - rooms: the list of 2 rooms it belongs to
    
    Attributes:
    -----------
    - ends: 2 end points
    - rooms: the list of 2 rooms it belongs to
    - opening: the stats of opening it has: location, type
    - type: the type of wall like glazing, concrete etc.
    - ...

    Methods:
    --------
    - add_thickness: add thickness based on wall type.
    
    """
    def __init__(self, ends, normal, rooms):
        """ 
        """
        self.ends = tuple((0,0,0), (0,0,0))
        self.rooms = []
        self.normal = (0,0,0)
        self.opening = 0
        self.openingLoc = 0

    def updateRoom(self,):
        """ update all the attributes of associated rooms include
        Room.walls, Room.area, Room.car, Room.adjRms, Room.adjTypes
        """
        pass

    def move(self,):
        """ move the wall along self.normal or opposite direction
        by 0.1m 
        """
        pass

    def split(self,):
        """ split the wall into 2 walls
        """
        pass

    def merge(self,):
        """ merge 2 walls into 1 wall
        """
        pass

    def change_opening(self,):
        """ change the type or location of opening 
        """
        pass



def main():

    pass

if __name__ == "__main__":
    main()