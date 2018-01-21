#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Floor class.

Author: Xian Lai
Date: Dec.21, 2017
"""
from math import factorial as f
from collections import Counter
from LocalSearch import LocalSearch
from Evaluator import Evaluator
import random

from Room import Room
from Wall import Wall


class Floor(object):

	"""
	This class defines floor objects for high-rise office buildings.(For now, 
    it just means cores) A floor is identified by a collection of Room objects 
    it contains. And it has some associated stats describing its properties 
    like space efficiency, escape distance etc.

    Inputs:
    -------
    - rm_type: the types of rooms in function model
    - rm_num: the initial numbers of rooms corresponding to each type. (this 
        number will change in search process)
    - silent: do not print out the searching process

	Attributes:
	-----------
	- state: the rooms in this floor
	- stats: a dictionary of properties of this floor

	Methods:
	--------
	- initialize: initialize a floor with sampled room types and numbers and 
        random assigned room locations and areas.
	- update_stats: calculate and update the stats based on current state.
	- swap_rooms: swap the name of 2 rooms
	- change_room: change 1 room by doing any of the following: moving one of 
        its walls, move one portion of the wall(require the wall be to split 
        first) or move its openings.
    """

    def __init__(self, rm_type=[], rm_num=[], silent=False):
        """ Initialize a floor objects with given room types and numbers.

        """
        self.initialize()
        self.stats  = {'rm_types':rm_type, 'rm_nums':rm_num}
        self.state  = []
        self.silent = silent
        self.objVal = 0
        

    def initialize(self):
        """ Initialize the plan with rooms and walls. Return the init_state.
        """
        # determine the number of room types in the plan
        # initialize all the rooms as 3.0*3.0 squares, each type in a row.
        type_num = len(self.stats['rm_types'])
        _ = (self.stats['rm_types'], self.stats['rm_nums'], range(type_num))
        for typ, num, r in zip(_):
        	for q in range(num):
        		cnrs = [(3.0*q, 3.0*r + 3), (3.0*q + 3, 3.0*r + 3), 
        				(3.0*q, 3.0*r), (3.0*q + 3, 3.0*r)]
        		walls = [Wall() for cnr in cnrs]
        		room = Room(rm_type=typ, rm_id=typ+'_'+str(i), walls=walls)
        		self.state.append(room)
        
        # parse the state of this plan and evaluate the score.
        self.parse()
        self.evaluate()


    def parse(self, ):
        """ Parse the state and return the stats.
        Besides the init stats room types and room numbers, the stats contains
        predefined features like space efficiency, escape distance etc.
    	"""
        
        pass


    def evaluate(self, ):
        """ Use the objective function to evaluate the stats and return the
    	objective value.
    	"""
        
    	pass
  

    def output_rooms(self,):
        """ output the room'id and their walls's ends, opening for drawing.
        """
        pass



    def output_stats(self,):
        """
        """
        pass

    def draw_rooms(self,):
        """ output the room'id and their walls's ends, opening for drawing.
        """
        pass


def main():

    pass

if __name__ == "__main__":
    main()