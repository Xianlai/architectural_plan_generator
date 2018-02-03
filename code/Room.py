#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Room class for architectural_plan_generator.

Author: Xian Lai
Date: Dec.21, 2017
"""


from Wall import Wall
from shapely.geometry import Polygon, box
from shapely.ops import cascaded_union as union


flatten = lambda l: list(set([item for sublist in l for item in sublist]))


def calc_convex_aspect(bounds):
    """ Find the convex aspect ratio of a rectangle given the bounds of this
    rectangle.
    """
    minx, miny, maxx, maxy = bounds
    aspect = (maxx - minx) / (maxy - miny)
    
    return max(aspect, 1 / aspect)


class Room(Polygon):

    """
    The room class implements the real-world room objects. It has states 
    attributes include the rid, the enclosing walls, the room function etc. 
    And stats attribtues include room area, convex aspect ratio, etc.

    Inputs:
    -------
    - rid: room id which is its index in main walls list
    - xys: the indices of grids this room contains
    - function: function of room like hallway, service room, etc.
    
    Attributes:
    -----------
    - rid: room id
    - walls: the walls enclosing it.
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
    - parse: Parse the geometry and stats of this room given states.
    - find_adjacent_rids: Find the rids of rooms adjacent to this room.
    - find_boundary_xys: Find the xys on boundary(inward) and corresponding 
        outward xys in other rooms.

    """

    def __init__(self, rid, xys, function):
        """ 
        """
        self.rid       = rid
        self.xys       = xys
        self.function  = function
        self._parse()
        

    def _parse(self, ):
        """ Parse the geometry and stats of this room given states
        """
        # init each grid in this room as a box and union them as a polygon
        init_box = lambda xy: box(xy[0]-0.5, xy[1]-0.5, xy[0]+0.5, xy[1]+0.5)
        self.geom  = union([init_box(xy) for xy in self.xys])

        # parse the stats based on the polygon geometry of this room
        self.stats = {
            'area':self.geom.area,
            'center':self.geom.centroid,
            'convex_aspect':calc_convex_aspect(self.geom.bounds),
            'min_x':self.geom.bounds[0],
            'max_x':self.geom.bounds[2],
            'min_y':self.geom.bounds[1],
            'max_y':self.geom.bounds[3]
        }


    def find_adjacent_rids(self, grids):
        """ Find the rids of rooms adjacent to this room.

        Args:
            grids (dict): the grids of the whole plan

        Returns: 
            the rids of adjacent rooms as a list
        """
        # find all outward xys of this room
        _, outward_xys = self.find_boundary_xys(grids)

        # the adjacent rids are the list of rid for each outward xy
        adjacent_rids = []
        for xy in flatten(outward_xys):
            if grids[xy].rid not in adjacent_rids:
                adjacent_rids.append(grids[xy].rid)

        return adjacent_rids


    def find_boundary_xys(self, global_xys):
        """ Find the xys on boundary(inward) and corresponding outward xys in
        other rooms.

        Args: 
            global_xys (list): the xys of the whole plan

        Returns:
            boundary_xys (list): the xys on boundary(inward)
            outward_xys (list): corresponding outward xys in other rooms
        """
        boundary_xys = []
        outward_xys  = []
    
        # for each xy in this room
        for xy in self.xys:
            # find the neighbor xys of this xy
            ngbrs = [
                (xy[0] - 1, xy[1]), (xy[0] + 1, xy[1]),
                (xy[0], xy[1] + 1), (xy[0], xy[1] - 1)
            ]
            # the outward neighbor xys are the ones not in this room but not 
            # out of the boundary of plan
            outward_ngbrs = [ngbr for ngbr in ngbrs \
                if (ngbr not in self.xys) and (ngbr in global_xys)]
            
            # if there is outward neighbor xys for this xy, then this xy is on
            # boundary and we record the corresponding outward xys in a list
            if len(outward_ngbrs) > 0:
                boundary_xys.append(xy)
                outward_xys.append(outward_ngbrs)

        return boundary_xys, outward_xys



def main():
    pass


if __name__ == "__main__":
    main()