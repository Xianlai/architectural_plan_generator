#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Room class.

Author: Xian Lai
Date: Dec.21, 2017
"""


from Wall import Wall


class Room(object):

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
        self.rid      = rid
        self.function = function
        self.walls    = walls
        self.stats    = {
            'area':0.0, 'convexAspect':0.0, 'adjacency':([], []), 
            'center':(0, 0), 'escapeDist':0.0
        }


    def parse(self, ):
        """
        """
        pass


def main():

    pass

if __name__ == "__main__":
    main()