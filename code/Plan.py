#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Plan class.

Author: Xian Lai
Date: Dec.21, 2017
"""

import numpy as np
from shapely.geometry import Point, LineString, Polygon
from Room import Room
from Wall import Wall
from Visual import SingleAxPlot


class Plan(object):

    """
    The plan class implements the real-world plan objects. It has states 
    attributes rooms. And stats attribtues include total area, space 
    efficiency etc.

    Inputs:
    -------
    - rm_functions: All the room functions exist in function model
    - rm_num: the initial numbers of rooms corresponding to each function. 
        (this number will change in search process)
    - silent: do not print out the searching process

    Attributes:
    -----------
    - walls: the walls in this plan
    - rooms: the rooms in this plan
    - silent: do not plot plans or print stats in the middle of searching
    - stats: a dictionary of properties of this plan:
        {
         'rm_functions': ['mr', 'wr', 'el', ...],
         'rm_nums': [0, 1, 2, ...],
         'walls': [],
         'total_area': 100.0,
         'n_rm_outOfBound': 0,
         'space_eff': 0.4, 
         'objective': 100.0
         ...
        }

    Methods:
    --------
    # actions:
    - initialize: initialize a floor with given room functions and numbers.
    - swap_rooms: swap the id and type of 2 rooms
    - split_room: add a wall somewhere in the middle of a room
    - remove_room: remove a wall between 2 rooms
    - move_wall: There are multiple situations in this action  
    - move_opening: move the location of opening on the wall. 
    - change_opening: change the opening type. Possible opening types: 
        {0:’close’, 1:’window’, 2:’door’}

    # supporting methods:
    - parse: parse stats from states
    - evaluate: Use the objective function to evaluate the stats and return 
        the objective value.
    - plot: extract walls and openings from rooms and plot the plan
    - print_stats: print the stats
    """

    def __init__(self, rm_functions, rm_nums, silent=False):
        """ 
        """
        self.silent   = silent 
        self.rm_func  = rm_functions
        self.rm_nums  = rm_nums
        self.walls    = []
        self.rooms    = []
        self.wall_cnt = 0
        self.room_cnt = 0
        self.initialize(rm_functions, rm_nums)
        
        

    def initialize(self, rm_functions, rm_nums):
        """ Initialize a plan with given room functions and room numbers.
        """
        # initialize all the rooms as 3.0*3.0 squares, each type in a row.
        for func, num, r in zip(rm_functions, rm_nums, range(len(rm_nums))):
            for q in range(num):
                rid = self.wall_cnt

                # initiate 4 walls for this room
                cnrs = [
                    (3.0*q, 3.0*r),         (3.0*q, 3.0*r + 3), 
                    (3.0*q + 3, 3.0*r + 3), (3.0*q + 3, 3.0*r)
                ]
                for i in range(-1, 3):
                    ends = (cnrs[i], cnrs[i+1])
                    wid  = self.wall_cnt
                    self.walls.append(Wall(ends=ends, wid=wid, rid=rid))
                    self.wall_cnt += 1

                # initiate a room
                room = Room(rid=rid, function=func, walls=self.walls[-4:])
                self.rooms.append(room)
                self.wall_cnt += 1
        
        self.check_sharing_walls()
        self.parse()
        self.evaluate()
        for room in self.rooms:
            print(room.exterior.coords)
        self.plot()


    def check_sharing_walls(self, ):
        """
        """
        for wall_0 in self.walls:
            for wall_1 in self.walls:
                if wall_0 is not wall_1:
                    if wall_0 == wall_1:
                        wall_0.stats['same'] = wall_1
                        wall_1.stats['same'] = wall_0



    def parse(self,):
        """ Parse the state and return the stats.
        """
        self.stats  = {
            'rm_areas':[],
            'fl_area': 100.0,
            'n_rm_outOfBound': 0,
            'space_eff': 0.4, 
            'objective': 100.0
        }


    def evaluate(self, ):
        """ Use the objective function to evaluate the stats and return the
        objective value.
        """
        
        pass
  

    def plot(self,):
        """ Plot the rooms' tags, walls and openings.
        """
        xy = [list(zip(wall.coords[0], wall.coords[1])) for wall in self.walls]
        X = [x[0] for x in xy]
        Y = [y[1] for y in xy]

        p = SingleAxPlot(figsize=(6,6))
        p.plot_lines(X, Y, title='Floor Plan', show=False)
        p.show()
        



    def print_stats(self,):
        """
        """
        pass

    # ---------------------------- actions -----------------------------------
    def swap_rooms(self,):
        """ Swap the id and type of 2 rooms
        """
        
        pass


    def split_room(self,):
        """ Add a wall somewhere in the middle of a room. 
        """
        
        pass


    def remove_room(self,):
        """ Remove a wall between 2 rooms.
        """
        
        pass


    def move_wall(self,):
        """ Move a selected wall.
        There are multiple situations in this action 
        """
        
        pass


    def move_opening(self,):
        """ Move the location of opening on the wall. 
        """
        
        pass


    def change_opening(self,):
        """ Change the opening type
        """
        
        pass


def main():
    rm_functions = ['men\'s_room', 'women\'s_room', 'service_room']
    rm_nums = [2, 3, 4]
    p = Plan(rm_functions=rm_functions, rm_nums=rm_nums)



if __name__ == "__main__":
    main()