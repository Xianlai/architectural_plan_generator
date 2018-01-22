#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Plan class.

Author: Xian Lai
Date: Dec.21, 2017
"""


from Room import Room
from Wall import Wall


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
	- rooms: the rooms in this plan
    - silent
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
	- initialize: initialize a floor with sampled room types and numbers and 
        random assigned room locations and areas.
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
        self.silent = silent
        self.rooms = []
        self.initialize(rm_functions, rm_nums)
        self.stats  = {
            'rm_functions':rm_functions, 
            'rm_nums':rm_nums,
            'walls': [],
            'total_area': 100.0,
            'n_rm_outOfBound': 0,
            'space_eff': 0.4, 
            'objective': 100.0
        }
        

    def initialize(self, rm_functions, rm_nums):
        """ Initialize a plan with given room functions and room numbers.
        """
        # determine the number of room types in the plan
        # initialize all the rooms as 3.0*3.0 squares, each type in a row.
        n_functions = len(rm_functions)
        _ = (rm_functions, rm_nums, range(n_functions))
        for typ, num, r in zip(_):
        	for q in range(num):
        		cnrs = [(3.0*q, 3.0*r + 3), (3.0*q + 3, 3.0*r + 3), 
        				(3.0*q, 3.0*r), (3.0*q + 3, 3.0*r)]
        		walls = [Wall() for cnr in cnrs]
        		room = Room(rm_type=typ, rm_id=typ+'_'+str(i), walls=walls)
        		self.rooms.append(room)
        
        # parse the state of this plan and evaluate the score.
        self.parse()
        self.evaluate()


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


    def parse(self,):
        """ Parse the state and return the stats.
    	"""
        
        pass


    def evaluate(self, ):
        """ Use the objective function to evaluate the stats and return the
    	objective value.
    	"""
        
    	pass
  

    def plot(self,):
        """ Plot the rooms' tags, walls and openings.
        """
        pass


    def print_stats(self,):
        """
        """
        pass


def main():

    pass

if __name__ == "__main__":
    main()