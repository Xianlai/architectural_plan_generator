#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Wall class.
Author: Xian Lai
Date: Oct.29, 2017
"""


from math import factorial as f


class Wall():

    """
    The wall class implements the real-world wall objects. It has states 
    attributes including the id, 2 end points, the opening, 2 rooms it belongs  
    to, thickness, material etc. In the searching process, we will abstract it 
    into a line with 1 id, 2 end points, 1 opening and 2 owning rooms. The  
    other attributes will be implemented later when needed in other problems.

    Inputs:
    -------
    - id   : the id of this wall
    - ends : 2 end points, (left, right) or (upper, lower).
    - rooms: the list of 2 rooms it belongs to
    
    Attributes:
    -----------
    - id     : id
    - ends   : 2 end points
    - rooms  : the list of 2 rooms it belongs to
    - opening: the stats of opening it has: location, type
    - stats  : The stats of this wall is encoded as a dictionary: 
        {
        normalDir: The normal direction of wall,
        thickness: (Not in use for now.) 
        material: (Not in use for now.)
        }

    Methods:
    --------
    - parse: parse the states attributes to get stats attributes.
    """

    def __init__(self, id, ends, rooms):
        """ Init a wall object with the wall id, 2 end points and 2 owning 
        rooms. When initialize, the opening type and location is always 0.
        """
        self.id      = 0
        self.ends    = tuple((0,0,0), (0,0,0))
        self.rooms   = []
        self.opening = [0, 0]
        self.stats   = {'normalDir':0}


    def parse(self,):
        """ parse the states attributes to get stats attributes.
        """
        pass

    

def main():

    pass

if __name__ == "__main__":
    main()