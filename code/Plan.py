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

from Room import Room
from Grid import Grid
from Wall import Wall
from Visual import SingleAxPlot


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
    - function_params: requirements for each room function as a dict
        {
            'room':{
                'n_room':number of rooms in each function, 
                'color_code':color coding for plotting, 
                'area':total area of each function, 
                'pr_merge':probability of being picked in merge action,
                ...
                }, 
            ...
        }
    - grid_coords: the x's and y's of grids inside boundary
    - silent: do not print out the searching process

    Attributes:
    -----------
    - grids: a dict containing the grids in this plan keyed by (x,y), namely  
        the coordinates of each grid. These grids are fixed once initialized.

    - rooms: a list containing the rooms in this plan. Each room has a rid for
        fast retrieval. If a room is deleted, we replace this room with None 
        object rather than delete it from the list in order to keep the indices
        of previous rooms unchanged.

    - actions: a list of possible actions that can change the state. For now,
        it's just ['expand', 'swap', 'split', 'merge']. We will add actions to
        manipulate walls when the walls attributes are added.

    - pr_actions: the probability distribution used when randomly pick action
        in random walk process. This won't be in use in search process.

    - room_count: the counter of room. Each time we create a room, we assign 
        the counter state at that time as rid. And then increment the counter 
        by 1.

    - silent: do not plot plans or print stats in the middle of searching

    - plot_freq: the frequency of plotting. (e.g. 4 if plot once every 4 steps)

    - objective: the objective value of this plan

    - stats: a dictionary of properties of this plan:
        {
            'rm_areas': area of each room in this plan,
            'n_rooms': total number of rooms in this plan,
            'rm_convex_aspect': convex aspect ratio of each room in this plan,
            'pl_space_eff': the ratio of non-corridor area and total area, 
            ...
        }

    Methods:
    --------
    # initialize
    - __init__: instantialize a Plan object

    - _initialize: initialize a random generated state.

        - _extract_function_params: extract each requirement for all functions 
            as a separate attribute.

        - _make_grids_from_coords: make a fixed list of grid objects from 
            given grid coordinates.

        - _divide_xys_into_rooms: Randomly divide existing grids into groups 
            and create a room for each group.

        - _divide_xys: randomly divide the xys into n continuous groups.


    # operations
    - random_walk: Random walk and stop after given iterations. 

    - _parse: Parse the stats from states.

    - _evaluate: Evaluate the objective value from stats.


    # actions and supporting methods
    - _expand: Expand a random portion of boundary of a random room.

        - _slice_a_subsequence: Randomly slice a consecutive subsequence out 
            of given sequence.

        - _group_xys_by_room: Group the given xys by room rids.

        - _check_continuous: Check whether the xys in the given room forms a 
            continuous area. If not, split the room into n rooms with 
            continuous xys.

        - _split_group: Pick the last xy from group_old and move it and all 
            adjacent xys to group_new.

    - _swap: Swap the functions of 2 random picked rooms

    - _split: Split a room into 2 same-function rooms by a random x or y axis
        inside this room's x, y ranges. 

    - _merge: Merge 2 same-function, adjacent rooms together.

        - _group_rooms_by_function: Group the valid rooms(not None) by their 
        functions.

    - _move_door: Move the location of door on the boundary. 

    - _change_wall: change the wall type from wall to door or from door to 
        wall. To be added later.
        Possible opening types: 
        {0:’wall’, 1:’window’, 2:’door’, 3:'entrance'}


    # general supporting methods
    - _purge_room: Return a list of valid rooms(not None) in this plan.

    - _pick_a_room: Randomly pick a valid room.

    - _plot_intermediate: Plot the plan.
    
    - _pprint_rooms: pprint the states of all rooms in this plan.

    """

    # -------------------------- init state ----------------------------------
    def __init__(self, function_params, grid_coords, silent=False):
        """ 
        """
        self.silent     = silent
        self.plot_freq  = 1
        self.unit       = 1
        self.actions    = ['_expand', '_swap', '_split', '_merge']
        self.pr_actions = [0.5, 0.2, 0.15, 0.15]
        self.plot_fig   = SingleAxPlot(figsize=(6,6))
        self._initialize(function_params, grid_coords)
 

    def _initialize(self, function_params, grid_coords):
        """ Initiate the plan state with given grid coordinates and functional
        requirements.

        Args:
            function_params (dict): the requirements for each function
            grid_coords (list): the list of grid coordinates as tuples

        """
        self._extract_function_params(function_params)
        self.total_area = sum(self.areas.values())
        self._make_grids_from_coords(grid_coords)
        self._divide_xys_into_rooms()
        
        self._parse()
        self._evaluate()
        self._plot_intermediate(0)


    def _extract_function_params(self, function_params):
        """ Extract each requirement for all functions as a separate attribute.

        Args:
            function_params (dict): the requirements for each function

        """
        self.functions = list(function_params.keys())  # all functions as a list
        self.n_rooms   = {}  # number of rooms for each function
        self.colors    = {}  # color coding for each function used for plotting
        self.areas     = {}  # area for each function
        self.pr_merge  = {}  # pick probability in merge action for each function

        for function, params in function_params.items():
            self.n_rooms[function] = params['n_room']
            self.colors[function]  = params['color_code']
            self.areas[function]   = params['area']
            self.pr_merge[function] = params['pr_merge']

        self.pr_merge = list(self.pr_merge.values())


    def _make_grids_from_coords(self, grid_coords):
        """ Make a fixed list of grid objects from given grid coordinates.
        
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



    # --------------------------- searching ----------------------------------
    def random_walk(self, iters):
        """ Random walk and stop after given iterations. 

        Note that this is not searching because the walking is not directed by
        the objective value.

        Args:
            iters (int): how many steps before stopping
        """
        for i in range(iters):
            print("\n\n------------------- Iter: %d --------------------" % i)
            print("Room states before action:"); self._pprint_rooms()
            # randomly pick a action with different weighting
            # apply the picked action to picked room and get new state
            action = random_pick(self.actions, p=self.pr_actions)
            print("\nSelected action:", action)
            getattr(self, action)()
            print("\nRoom states after action:"); self._pprint_rooms()
            # parse the stats and evaluate the stats
            # plot the plan every 20 iterations
            self._parse()
            self._evaluate()
            # plot the plan every 2 step, change this number to control the 
            # plot frequency
            if i % 2 == 0: self._plot_intermediate(i)

        self.plot_fig.ioff()


    def _pprint_rooms(self,):
        """ pprint the states of all rooms in this plan.
        """
        f = lambda x: {'rid':x.rid, 'function':x.function, 'xys':x.xys}
        pprint(["None" if room is None else f(room) for room in self.rooms])


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
        print("\nPlan Stats:"); pprint(self.stats)


    def _evaluate(self, ):
        """ Evaluate the objective value from stats.

        """
        n_rooms          = self.stats['n_rooms']
        avg_area         = sum(self.stats['rm_areas']) / n_rooms
        avg_convex_ratio = sum(self.stats['rm_convex_aspect']) / n_rooms
        efficiency       = self.stats['pl_space_eff']
        # the weighting for each term is just assigned randomly for debuging
        self.objective = 2 * avg_area + 3 * avg_convex_ratio + 4 * efficiency
        print("\nObjective Value:", self.objective)
  


    # ---------------------------- actions -----------------------------------
    def _expand(self,):
        """ Expand a random portion of boundary of a random room.

        """
        # randomly pick a room
        # find outward grids of boundary grids of the picked room
        # randomly select a consecutive portion of outward grids
        room = self._pick_a_room()
        print("Pick room: %d" % room.rid)
        _, outward_xys = room.find_boundary_xys(self.xys)
        if len(outward_xys) == 0: 
            print("This room has no outward xys.")
            return
        outward_xys = self._slice_a_subsequence(outward_xys)

        # update grids and rooms
        # group the outward xys by rooms and iterate through each outward room
        outward_groups = self._group_xys_by_room(flatten(outward_xys))
        for rid, xys in outward_groups.items():
            # add this xy into this room's xys list
            room.xys += xys
            # remove this xy from its corresponding outward room
            for xy in xys: self.rooms[rid].xys.remove(xy)
            print(xys, "in Room %d is taken by this expand" % rid)
            print(self.rooms[rid].xys, "is the xys left in this room.")
            # if the outward room's xys list is empty after removing, change 
            # this room to None.
            if not self.rooms[rid].xys: 
                print("Room %d is eaten up by this expand" % rid)
                self.rooms[rid] = None
            # if the outward room's xys list doesn't parse to a single Polygon 
            # which means it's split by this expand action, split it to 2 rooms
            else: self._check_continuous(self.rooms[rid])
            # update the rid of this xy
            for xy in xys: self.grids[xy].rid = room.rid


    def _slice_a_subsequence(self, seq):
        """ Randomly slice a consecutive subsequence out of given sequence.
        """
        n = len(seq)
        if n == 1:
            return seq
        else:
            start  = random_pick(n)
            length = random_pick(range(1, n))
            end = start + length
            if end < n:
                sub_seq = seq[start:end]
            else:
                sub_seq = seq[start:n] + seq[0:end - n - 1]

            return sub_seq


    def _group_xys_by_room(self, xys):
        """ Group the given xys by room rids.
        """
        groups = {}

        for xy in xys:
            key = self.grids[xy].rid
            if key not in groups: groups[key] = [xy]
            else: groups[key].append(xy)

        return groups


    def _check_continuous(self, room):
        """ Check whether the xys in the given room forms a continuous area.
        If not, split the room into n rooms with continuous xys.

        Args:
            room (Room): the room to check
        """
        xys = room.xys
        # move connecting xys into a new group
        # if old group is empty, then xys is continuous, change nothing
        group_new, group_old = self._split_group(xys)
        if group_old == []: 
            print("Room %d is still a whole piece" % room.rid)
            return

        # otherwise, keep spliting xys until old group is empty.
        # the new groups are the xys for new rooms
        groups = [group_new]
        while group_old:
            group_new, group_old = self._split_group(group_old)
            groups.append(list(group_new))

        # create new rooms and set old room to None
        for group in groups:
            # add new room to self.rooms
            room_new = Room(
                function=room.function, 
                rid=self.room_count,
                xys=group
            )
            self.rooms.append(room_new)
            print("Room %d is split out" % room_new.rid)
            # update the rid of xys
            for xy in group:
                self.grids[xy].rid = self.room_count

            self.room_count += 1

        self.rooms[room.rid] = None


    def _split_group(self, group_old):
        """ Pick the last xy from group_old and move it and all adjacent xys 
        to group_new.

        Args: 
            group_old (list): the group of xys we want to split

        Returns:
            group_new (list): one group of continuous xys split from group_old
            group_old (list): the remaining group of xys(may contain 
                un-continuous xys)

        """
        # move the last xy of group_old into group_new
        group_old = list(group_old)
        group_new = [group_old.pop()]

        # iter through group_old and group_new, if there are 1 xy in group_old
        # and 1 xy from group_new has l1 distance 1, then these 2 xys are 
        # adjacent and add this xy in group_old to group_new
        for i in group_old:
            for k in group_new:
                if l1_dist((i, k)) == 1:
                    group_new.append(i)
                    break

        # remove all the elements in group_new from group_old
        for k in group_new[1:]: group_old.remove(k)

        return group_new, group_old



    def _swap(self,):
        """ Swap the functions of 2 random picked rooms
        """
        room_1 = self._pick_a_room()
        room_2 = self._pick_a_room()
        while room_2 is room_1: room_2 = self._pick_a_room()

        print("Pick 2 rooms: %d and %d" % (room_1.rid, room_2.rid))
        print("Swap functions: %s and %s" % (room_1.function, room_2.function))
        room_1.function, room_2.function = room_2.function, room_1.function



    def _split(self,):
        """ Split a room into 2 same-function rooms by a random x or y axis
        inside this room's x, y ranges. 

        """
        room = self._pick_a_room()
        axis = random_pick(['x', 'y'])
        print("Split room:", room.rid)

        # randomly pick a split line
        left  = room.stats["min_"+axis] + 0.5
        right = room.stats["max_"+axis] - 0.5
        if right - left == 0: 
            print("This room has width 1 at axis %s" % axis)
            return
        split_line = random_pick(np.arange(left, right))

        # split the grids
        xys_1, xys_2 = [], []
        for xy in room.xys:
            if getattr(self.grids[xy], axis) <= split_line: 
                xys_1.append(xy)
            else: 
                xys_2.append(xy)

        # create 2 new rooms based on split 2 groups of xys
        # append the new rooms to self.rooms and set original room to None
        room_1 = Room(function=room.function, xys=xys_1, rid=self.room_count)
        room_2 = Room(function=room.function, xys=xys_2, rid=self.room_count + 1)
        self.rooms += [room_1, room_2]
        self.rooms[room.rid] = None

        self.room_count += 2

        # update the rids of split xys 
        for xy in xys_1: self.grids[xy].rid = room_1.rid
        for xy in xys_2: self.grids[xy].rid = room_2.rid

        print("Into 2 rooms: %d and %d" % (room_1.rid, room_2.rid))



    def _merge(self, ):
        """ Merge 2 same-function, adjacent rooms together.

        """
        # find all pairs of adjacent, same-function rooms keyed by function
        groups = self._group_rooms_by_function()
        pairs  = {function:[] for function in self.functions}
        for function in self.functions:
            for rid in groups[function]:
                for adjacent_rid in self.rooms[rid].find_adjacent_rids(self.grids):
                    if adjacent_rid in groups[function]:
                        pairs[function].append((rid, adjacent_rid))

        # purge the function without adjacent pairs
        # if no function contains adjacent pairs, exit this action.
        pairs = purge_dict(pairs)
        if not pairs: 
            print("No pairs of adjacent same-function rooms found.")
            return

        # randomly pick a function by weighting. (we may want to using weights
        # to control the chance of merge for different room function)
        # redo picking if the picked function has no adjacent pairs
        picked_function = ""
        while picked_function not in pairs.keys():
            picked_function = random_pick(self.functions, p=self.pr_merge)

        # randomly pick a pair of adjacent rooms
        # create a new room with same function and merged xys
        picked_pair = random_choice(pairs[picked_function])
        room_new    = Room(
            function=picked_function, 
            rid = self.room_count,
            xys=self.rooms[picked_pair[0]].xys + self.rooms[picked_pair[1]].xys
        )
        self.room_count += 1
        print("Merge rooms %d and %d" % (self.rooms[picked_pair[0]].rid,
            self.rooms[picked_pair[1]].rid))

        # update self.rooms
        self.rooms[picked_pair[0]] = None
        self.rooms[picked_pair[1]] = None
        self.rooms.append(room_new)
        print("into room %d" % room_new.rid)

        # update the rid of merged xys
        for xy in room_new.xys:
            self.grids[xy].rid = room_new.rid


    def _group_rooms_by_function(self, ):
        """ Group the valid rooms(not None) by their functions. The result is 
        a dictionary.

        """
        rooms = self._purge_room()
        groups = {function:[] for function in self.functions}
        for room in rooms:
            groups[room.function].append(room.rid)
            
        return groups


    def _move_door(self,):
        """ Move the location of door on the boundary. 
        """

        pass


    def _change_wall(self,):
        """ Change the wall type
        """
        
        pass



    # ----------------------- supporting methods -----------------------------
    def _purge_room(self,):
        """ Return a list of valid rooms(not None) in this plan.
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
            i: the iteration
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
     


def main():
    grid_coords = (
        (0,3), (0,4),
        (1,3), (1,4), (1,5),
        (2,0), (2,1), (2,2), (2,3), (2,4), (2,5),
        (3,0), (3,1), (3,2), (3,3), (3,4), (3,5),
        (4,0), (4,1), (4,2), (4,3), 
        (5,2), (5,3),  
    )
    function_params = {
        'bedroom':{
            'n_room':2, 
            'color_code':"#4286f4", 
            'area':14, 
            'pr_merge':0.5
            }, 
        'living_room':{
            'n_room':1, 
            'color_code':"#ff908e", 
            'area':9, 
            'pr_merge':0.5
            },
    }
    plan = Plan(function_params=function_params, grid_coords=grid_coords)
    plan.random_walk(iters=40)



if __name__ == "__main__":
    main()