#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Grid class for architectural_plan_generator.
Author: Xian Lai
Date: Jan.30, 2017
"""


class Grid():

    """
    The grid class implements the abstract grid objects which are the unit 
    areas inside rooms. We use it to manipulate the geometry of rooms.

    Inputs:
    -------
    - xy (tuple): the coordinates of this grid. Also used as the key for 
        retrieval from main grids list.
    - rid (int): the id of the room this grid belongs to.
    
    Attributes:
    -----------
    - xy (tuple): the coordinates of this grid
    - x (int): the x of this grid
    - y (int): the y of this grid
    - rid (int): the id of the room it belongs to

    Methods:
    --------
    - parse: parse the states attributes to get stats attributes.
    """

    def __init__(self, xy, rid):
        """ 
        """
        self.xy = xy
        self.x, self.y = xy
        self.rid = rid


    def parse(self,):
        """ parse the states attributes to get stats attributes.
        """
        pass

    

def main():
    pass

if __name__ == "__main__":
    main()