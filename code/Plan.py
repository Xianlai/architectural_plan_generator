#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Plan class for architectural_plan_generator.

Author: Xian Lai
Date: Dec.21, 2017
"""


from pprint import pprint
import numpy as np
from numpy.random import choice as random_pick

from Transition import Transition
from Room import Room
from Grid import Grid
from Wall import Wall
import Visual


# ---------------------------- global functions ------------------------------
indices    = lambda seq: range(len(seq))
flatten    = lambda l: list(set([item for sublist in l for item in sublist]))
purge_dict = lambda d: dict((k, v) for k, v in d.items() if v)
l1_dist    = lambda xys: abs(xys[0][0] - xys[1][0]) + abs(xys[0][1] - xys[1][1])
random_choice = lambda seq: seq[random_pick(indices(seq))]


class Plan(object):

    """
    The plan class implements the real-world plan objects. It's consisted of 
    different types of rooms, and each room is consisted of a number of unit 
    grids and enclosing walls. Besides the state attributes, it also has stats 
    attribtues like total area, space efficiency etc.

    Inputs:
    -------
    - function_params (dict): requirements for each function as a dict
        {
            'function':{
                'area':total area of each function, 
                'n_room':number of rooms in each function, 
                'pr_merge':probability of being picked in merge action,
                ...
                }, 
            ...
        }
    - grid_coords (list): the x's and y's of grids inside boundary
    - silent (bool): do not print out the searching process
    - init_state (dict): a initial plan state encoded as a dictionary of 
        function/grid-coordinates pairs assigned by human designer.
        {
            "bedroom":[(x,y), (x,y), (x,y), (x,y), ],
            "bedroom":[(x,y), (x,y), (x,y), (x,y), ],
            "living_room":[(x,y), (x,y), (x,y), (x,y)]
        }

    Attributes:
    -----------
    - grids: a dict containing the grids in this plan keyed by (x,y), namely  
        the coordinates of each grid. These grids are fixed once initialized.
    - rooms: a list containing the rooms in this plan. Each room has a rid for
        fast retrieval. If a room is deleted, we replace this room with None 
        object rather than delete it from the list in order to keep the indices
        of previous rooms unchanged.
    - xys: simply the coordinates of each grid
    - room_count: the counter of room. Each time we create a room, we assign 
        the counter state at that time as rid. And then increment the counter 
        by 1.
    - objective: the objective value of this plan
    - stats: a dictionary of properties of this plan:
        {
            'rm_areas': area of each room in this plan,
            'n_rooms': total number of rooms in this plan,
            'rm_convex_aspect': convex aspect ratio of each room in this plan,
            'pl_space_eff': the ratio of non-corridor area and total area, 
            ...
        }
    - plot_fig: the matplotlib figure object to plot plans on.
    - unit: the size of unit grids
    - total_area: the total area of plan
    - functions: all the functions in this plan
    - n_rooms: the number of rooms in this plan
    - areas: the areas for each function
    - pr_merge: pick probability in merge action for each function
    - n_functions: the number of functions in this plan
    - colors: the color of each function used in plotting
    - silent: do not plot plans or print stats in the middle of searching
    - plot_freq: the frequency of plotting. (e.g. 4 if plot once every 4 steps)
    

    Methods:
    --------
    # Initialize
    - _extract_function_params：Extract each requirement for all functions as 
        a separate attribute.
    - _parse_init_state：Parse the given init state into rooms and grids.
    - _random_initialize: Initiate the plan state with given grid coordinates‘ 
    - _make_grids_from_coords: Make a fixed list of grid objects from given 
        grid coordinates.
    - _divide_xys_into_rooms: Randomly divide existing grids into groups and 
        create a room for each group.
    - _divide_xys: Randomly divide the xys into n continuous groups.
    - _find_xy_lims: Find the bounding x and y values of this plan.

    # Searching(will be seperated as a searching class in the future)
    - random_walk: Random walk and stop after given iterations. 

    # Evaluating(will be seperated as a Objective class in the future)

    # Supporting methods:
    - _parse: Parse the stats from states.
    - _evaluate: Evaluate the objective value from stats.
    - _purge_room: Return a list of valid rooms(not None) in this plan.
    - _pick_a_room: Randomly pick a valid room.
    - _plot_intermediate: Plot the plan.
    - _pprint_rooms: pprint the states of all rooms in this plan.
    
    """

    
    def __init__(self, function_params, grid_coords=None, init_state=None, 
            silent=False):

        self._extract_function_params(function_params)

        # if init_state parameter is given, we parse it as the initial state
        # else, the grid coordinates must be given, and we generate initial
        # state randomly.
        if init_state: self._parse_init_state(init_state)
        else: self._random_initialize(grid_coords)

        self.silent     = silent
        self.unit       = 1
        self.total_area = sum(self.areas.values())
        self.plot_freq  = 1
        self.plot_fig   = Visual.SingleAxPlot(xy_lims=self._find_xy_lims())
        
        self._parse()
        self._evaluate()
        self._plot_intermediate(0)
 

# -------------------------- init state --------------------------------------
    def _extract_function_params(self, function_params):
        """ Extract each requirement for all functions as a separate attribute.

        Args:
            function_params (dict): the requirements for each function

        """
        self.functions = list(function_params.keys())  # all functions as a list
        self.n_rooms   = {}  # number of rooms for each function
        self.areas     = {}  # area for each function
        self.pr_merge  = {}  # pick probability in merge action for each function

        for function, params in function_params.items():
            self.n_rooms[function] = params['n_room']
            self.areas[function]   = params['area']
            self.pr_merge[function] = params['pr_merge']

        self.pr_merge = list(self.pr_merge.values())
        self.n_functions = len(self.functions)
        self.colors = {f:Visual.CM(i/self.n_functions) for i, f in \
            enumerate(self.functions)}


    def _parse_init_state(self, init_state):
        """ Parse the given initial state into rooms and grids.

        Args:
            init_state (dict): initial state encoded as a dictionary.

        """
        self.room_count = 0
        self.grids = {}
        self.rooms = []
        self.xys   = []

        # for each room state namely each function:grid_coords pair in init_state
        for function, grid_coords in init_state.items():
            # instantialize this room and add it to self.rooms
            room = Room(
                    rid=self.room_count, 
                    function=function, 
                    xys=grid_coords
            )
            self.rooms.append(room)

            # instantialize the grids from this group of grid coordinates
            for xy in grid_coords:
                self.grids[xy] = Grid(xy=xy, rid=self.room_count)

            self.room_count += 1
            self.xys += grid_coords
 

    def _random_initialize(self, grid_coords):
        """ Randomly generate an initial plan state with given grid coordinates.

        Args:
            grid_coords (list): the list of grid coordinates as tuples

        """
        self._make_grids_from_coords(grid_coords)
        self._divide_xys_into_rooms()


    def _make_grids_from_coords(self, grid_coords):
        """ Make a fixed dictionary of grid objects keyed by their coordinates
        from given grid coordinates.
        
        Args:
            grid_coords (list): the list of grid coordinates as tuples

        """
        # the coordiates are used as the key for fast retrieval.
        # the rid are temporarily none and everything else is immutable.
        self.grids = {coord:Grid(xy=coord, rid=None) for coord in grid_coords}
        self.xys   = grid_coords


    def _divide_xys_into_rooms(self, ):
        """ Randomly divide existing grids into groups and create a room for 
        each group.
        """
        self.rooms      = []
        self.room_count = 0

        # divide xys into n groups, n equals to the total number of rooms
        groups = self._divide_xys(sum(self.n_rooms.values()))
        
        # for each group, we create a room with function and rid
        for function, n_rooms in self.n_rooms.items():
            for i in range(n_rooms):
                room = Room(
                    rid=self.room_count, 
                    function=function, 
                    xys=groups[self.room_count]
                )
                self.rooms.append(room)
                # update the rid of xys in this newly created room
                for xy in room.xys:
                    self.grids[xy].rid = self.room_count

                self.room_count += 1


    def _divide_xys(self, n):
        """ Randomly divide the xys into n continuous groups.
        
        Args:
            n (int): number of groups to have

        Returns:
            groups (list): the list of divided xys groups

        """
        groups = [[] for i in range(n)]

        # randomly pick n xys(points) in plan 
        xys    = list(self.grids.keys())
        idx    = random_pick(indices(xys), size=n, replace=False)
        points = [xys[i] for i in idx]

        # assign each xy to the nearest point(l1 version of voronoi).
        for xy in xys:
            dists    = [l1_dist((xy, point)) for point in points]
            min_dist = min(dists)
            groups[dists.index(min_dist)].append(xy)
            
        return groups


    def _find_xy_lims(self,):
        """ Find the bounding x and y values of this plan.
        """
        xs = [xy[0] for xy in self.xys]
        ys = [xy[1] for xy in self.xys]
        return ((min(xs)-1, max(xs)+1), (min(ys)-1, max(ys)+1))


# --------------------------- searching --------------------------------------
    def random_walk(self, iters):
        """ Generate new plan states by random walking and stop after given 
        iterations. 

        Note that this is not searching because the walking is not directed by
        the objective value.

        Args:
            iters (int): how many steps before stopping

        """
        # instantialize a transition object to handle actions
        transition = Transition(silent=self.silent, pr_actions=[1., 0., 0., 0.])

        for i in range(iters):
            if not self.silent:
                print("\n\n------------------- Iter: %d --------------------" % i)
            # randomly pick a action with different weighting
            # apply the picked action to picked room and get new state
            action = random_pick(transition.actions, p=transition.pr_actions)
            if not self.silent:
                print("\nSelected action:", action)
            getattr(transition, action)(self)
            if not self.silent:
                print("\nRoom states after action:"); self._pprint_rooms()
            # parse the stats and evaluate the stats
            # plot the plan every 20 iterations
            self._parse()
            self._evaluate()
            if i % self.plot_freq == 0: self._plot_intermediate(i)

        self.plot_fig.ioff()


# ----------------------- evaluating methods ---------------------------------
    def _evaluate(self, ):
        """ Evaluate the objective value from stats.

        """
        n_rooms          = self.stats['n_rooms']
        avg_area         = sum(self.stats['rm_areas']) / n_rooms
        avg_convex_ratio = sum(self.stats['rm_convex_aspect']) / n_rooms
        efficiency       = self.stats['pl_space_eff']
        # the weighting for each term is just assigned randomly for debuging
        self.objective = 2 * avg_area + 3 * avg_convex_ratio + 4 * efficiency
        if not self.silent:
            print("\nObjective Value:", self.objective)


# ----------------------- supporting methods ---------------------------------
    def _parse(self,):
        """ Parse the stats from states.
        """
        rooms = self._purge_room()
        for room in rooms: room._parse()

        corridors  = [room for room in rooms if room.function == "hall_way"]
        corr_area  = sum([corr.stats['area'] for corr in corridors])
        self.stats = {
            'rm_areas':[room.stats['area'] for room in rooms],
            'n_rooms':len(rooms),
            'rm_convex_aspect':[room.stats['convex_aspect'] for room in rooms],
            'pl_space_eff': 1 - corr_area / self.total_area, 
        }
        if not self.silent:
            print("\nPlan Stats:"); pprint(self.stats)


    def _purge_room(self,):
        """ Return a list of valid rooms(rooms are not None) in this plan.
        """
        return [room for room in self.rooms if room is not None]


    def _pick_a_room(self, ):
        """ Randomly pick a valid room.
        """
        rooms = self._purge_room()
        return random_pick(rooms)


    def _plot_intermediate(self, i):
        """ Plot the plan.

        Args:
            i (int): the iteration

        """
        rooms     = self._purge_room()
        centers   = [room.stats['center'] for room in rooms]
        functions = [room.function for room in rooms]
        patches   = [room.geom for room in rooms]
        colors    = [self.colors[function] for function in functions]
            
        
        self.plot_fig.plot_plan_intermediate(
            centers=centers, 
            functions=functions, 
            patches=patches, 
            colors=colors, 
            title="plan_searching(round %d)" % i
        )


    def _pprint_rooms(self,):
        """ pprint the states of all rooms in this plan.
        """
        f = lambda x: {'rid':x.rid, 'function':x.function, 'xys':x.xys}
        pprint(["None" if room is None else f(room) for room in self.rooms])
     


def main():

    pass


if __name__ == "__main__":
    main()