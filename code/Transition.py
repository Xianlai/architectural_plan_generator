#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the Transition class for architectural_plan_generator.

Author: Xian Lai
Date: Dec.21, 2017
"""

from pprint import pprint
import numpy as np
from numpy.random import choice as random_pick
from Room import Room
from collections import defaultdict
from itertools import groupby


# ---------------------------- global functions ------------------------------
indices    = lambda seq: range(len(seq))
flatten    = lambda l: list(set([item for sublist in l for item in sublist]))
purge_dict = lambda d: dict((k, v) for k, v in d.items() if v)
l1_dist    = lambda xys: abs(xys[0][0] - xys[1][0]) + abs(xys[0][1] - xys[1][1])


def random_choice(seq, n=1):
    """
    """
    if n == 1:
        return seq[random_pick(indices(seq))]
    else:
        return [seq[i] for i in random_pick(indices(seq), size=n)]


def any_in_any(a, b):
    """ return true if any element in iterable a is in iterable b.
    """
    for i in a:
        if i in b: 
            return True

    return False


class Transition(object):

    """
    The transition class implements the transition model and available actions.
    The actions that can change the plan state are: expand, swap, split and 
    merge. This class provides method to randomly pick one of them, pick one of
    them by different probabilities or pick all of them.

    Inputs:
    -------
    - silent (bool): whether print the immediate process to screen.
    - pr_actions (list): the probability for each action when using 
        stratified sampling.

    Attributes:
    -----------
    - actions: a list of possible actions that can change the state. For now,
        it's just ['expand', 'swap', 'split', 'merge']. We will add actions to
        manipulate walls when the walls attributes are added.
    - pr_actions: the probability distribution used when randomly pick action
        in random walk process. This won't be in use in search process.
    - silent (bool): do not print out the searching process

    Methods:
    --------
    - expand: Expand a random portion of boundary of a random room.
    - _group_xys_by_room: Group the given xys by room rids.
    - _group_xys_by_adjacency: Get the groups of consective tuples given 
        scattered tuples.
    - _group_by_consective_x: group the points by whether they have consective
        x values.
    - _get_component_bounds: Get the maximal y value and x values of a given 
        component.
    - _check_room_continuity: Check whether the xys in given room are still 
        continuous. If yes, keep it, else, split it into new rooms and set it 
        to None.
    - _random_pick_walls_to_expand: Randomly pick {a portion of a wall, a wall,
        multiple walls} by probabilities {0.2, 0.7, 0.1} to expand outward
    - _slice_a_subsequence: Randomly slice a consecutive subsequence out of 
        given sequence.
    - swap: Swap the functions of 2 random picked rooms
    - split: Split a room into 2 same-function rooms by a random x or y axis
        inside this room's x, y ranges. 
    - merge: Merge 2 same-function, adjacent rooms together.
    - _group_rooms_by_function: Group the valid rooms(not None) by their 
        functions.
    - move_door: Move the location of door on the boundary. 
    - change_wall: change the wall type from wall to door or from door to 
        wall. To be added later.
        Possible opening types: 
        {0:’wall’, 1:’window’, 2:’door’, 3:'entrance'}
    """
    
    def __init__(self, silent=False, pr_actions=[1, 0, 0, 0]):

        self.silent     = silent
        self.actions    = ['expand', 'swap', 'split', 'merge']
        self.pr_actions = pr_actions
 

# ---------------------------- expand ----------------------------------------
    def expand(self, plan):
        """ Expand a random portion of boundary of a random room.
        
        Args:
            plan (Plan): the plan we are operating on.
        """
        # randomly pick a room from given plan and find its surrounding xys
        room = plan._pick_a_room()
        _, srd_xys = room.find_boundary_xys(plan.xys)
        if not self.silent: print("Pick room: %d" % room.rid)

        # if there is no surrounding xys found, return. This is a rare 
        # situation when this room occupies the whole plan.
        if len(srd_xys) == 0: 
            if not self.silent: print("This room has no surrounding xys.")
            return

        # group the surrounding xys into surrounding walls(only the xys 
        # connecting by convex corners are seperated)
        srd_walls = self._group_xys_by_adjacency(flatten(srd_xys))
        if not self.silent: print("outward walls: ", srd_walls)

        # randomly pick a portion of 1 wall, 1 wall or multiple walls to 
        # expand outward
        outward_xys = self._random_pick_walls_to_expand(srd_walls)

        # group the outward xys by rooms and iterate through each group to 
        # update the grids and rooms.
        outward_groups = self._group_xys_by_room(outward_xys, plan)
        if not self.silent: print("Outward groups:", outward_groups)
        for rid, xys in outward_groups.items():
            # add this xy into this room's xys list
            room.xys += xys

            # remove this xy from its corresponding outward room
            for xy in xys: plan.rooms[rid].xys.remove(xy)
            if not self.silent:
                print(xys, "in Room %d is taken by this expand" % rid)
                print(plan.rooms[rid].xys, "is the xys left in this room.")

            # if the outward room's xys list is empty after removing, change 
            # this room to None.
            if not plan.rooms[rid].xys: 
                if not self.silent:
                    print("Room %d is eaten up by this expand" % rid)
                plan.rooms[rid] = None

            # if the outward room's xys list doesn't parse to a single Polygon 
            # which means it's split by this expand action, split it to n rooms.
            # here n refers to the number of continuous groups of grids it has.
            else:
                self._check_room_continuity(rid, plan)

            # update the rid of this xy
            for xy in xys: plan.grids[xy].rid = room.rid


    def _group_xys_by_room(self, xys, plan):
        """ Group the given xys by room rids.

        Args:
            xys (tuple): the xys to be grouped
            plan (Plan): the plan those xys belong to

        """
        # group the xys by their rid
        groups = defaultdict(list)
        for xy in xys: groups[plan.grids[xy].rid].append(xy)
        
        # remove duplicated xys in the groups
        for k, v in groups.items(): groups[k] = list(set(v))

        return groups


    def _group_xys_by_adjacency(self, xys):
        """ Get the groups of consective xys given scattered xys.

        Args:
            xys (list): the xys to be grouped

        """
        d = defaultdict(list)
        # divide the xys into rows by their y values
        for x, y in xys: 
            d[y].append((x,y))

        # divide the xys in each room into consective components
        for k, v in d.items(): 
            d[k] = self._group_xys_by_consective_x(v)

        ys = sorted(d.keys())
        # set the components in first row as groups
        groups = [component for component in d[ys[0]]]

        # for each component in upper rows, if there is one group right below 
        # it(group_maxy = component_maxy - 1) and their x values overlap. Then
        # this component is connecting to that group and will be merged to it.
        # if there is no such group, make a new group with this component.
        for i in ys[1:]:
            for component in d[i]:
                connecting = False
                c_y, c_xs = self._get_component_bounds(component)
                for group in groups:
                    g_y, g_xs = self._get_component_bounds(group)
                    if (c_y == g_y + 1) and (any_in_any(c_xs, g_xs)):
                        connecting = True
                        group += component
                        break
                if not connecting:
                    groups.append(component)
        
        return groups


    def _group_xys_by_consective_x(self, xys):
        """ Group given xys by consective x values

        Args:
            xys: the xys to be grouped.
            
        """
        # the key function is index - element, for every group of consective
        # elements, this function should have same result
        groupby_key = lambda x: x[0] - x[1][0]
        gb = groupby(enumerate(sorted(xys, key=lambda xy: xy[0])), groupby_key)

        return [[x[1] for x in list(g)] for _,g in gb]


    def _get_component_bounds(self, component):
        """ Get the maximal y value and x values of a given component.

        Args:
            component: the horizontal band of xys we want to parse
        """
        maxy = component[-1][1]
        xs   = [xy[0] for xy in component]

        return maxy, xs 


    def _check_room_continuity(self, rid, plan):
        """ Check whether the xys in given room are still continuous. If yes,
        keep it, else, split it into new rooms and set it to None.

        Args:
            rid (int): the rid of room to check
            plan (Plan): the plan contains this given room
        """
        groups = self._group_xys_by_adjacency(plan.rooms[rid].xys)
        if len(groups) == 1:
            if not self.silent:
                print("Room %d is still a whole piece" % rid)
        else:
            if not self.silent:
                print("Room %d is divided into %d pieces" % (rid, len(groups)))
            # create new rooms and set old room to None
            for group in groups:
                # add new room to self.rooms
                room_new = Room(
                    function=plan.rooms[rid].function, 
                    rid=plan.room_count,
                    xys=group
                )
                plan.rooms.append(room_new)
                if not self.silent:
                    print("Room %d is split out" % room_new.rid)
                # update the rid of xys
                for xy in group:
                    plan.grids[xy].rid = plan.room_count

                plan.room_count += 1

            plan.rooms[rid] = None
            if not self.silent:
                print("Room %d is reset to None" % rid)


    def _random_pick_walls_to_expand(self, walls):
        """ Randomly pick {a portion of a wall, a wall, multiple walls} by 
        probabilities {0.2, 0.7, 0.1} to expand outward
        """
        
        # choose whether to expand multiple walls or just one wall. The prob 
        # of picking 1 is 0.9, and the rest 0.1 prob is evenly distributed 
        # among 2 to n_walls.
        n_walls = len(walls)
        pr_pick = [0.9]+[0.1/(n_walls-1) for i in range(n_walls-1)]
        n_pick  = random_pick(range(n_walls), p=pr_pick)

        # if we select multiple walls to expand:
        if n_pick > 1:
            outward_xys = flatten(random_choice(walls, n=n_pick))
            if not self.silent: 
                print("Selected number of walls to expand:", n_pick)
                print("Surrounding xys to be taken: ", outward_xys)

        # if we select 1 wall to expand, we further choose whether to expand
        # the whole wall or a portion of wall. The prob to select whole wall
        # is 0.7, and select a portion is 0.3.
        else:
            n_pick = random_pick(["portion", "whole"], p=[0.3, 0.7])
            if n_pick == "whole":
                outward_xys = random_choice(walls)
                if not self.silent: 
                    print("Selected number of walls to expand:", 1)
                    print("Surrounding xys to be taken: ", outward_xys)
            else:
                outward_xys = self._slice_a_subsequence(random_choice(walls))
                if not self.silent: 
                    print("A portion of 1 wall to expand.")
                    print("Surrounding xys to be taken: ", outward_xys)

        return outward_xys


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


# ---------------------------- swap ------------------------------------------
    def swap(self, plan):
        """ Swap the functions of 2 random picked rooms
        """
        room_1 = plan._pick_a_room()
        room_2 = plan._pick_a_room()
        while room_2 is room_1: room_2 = plan._pick_a_room()

        if not self.silent:
            print("Pick 2 rooms: %d and %d" % (room_1.rid, room_2.rid))
            print("Swap functions: %s and %s" % (room_1.function, room_2.function))
        room_1.function, room_2.function = room_2.function, room_1.function


# ---------------------------- split -----------------------------------------
    def split(self, plan):
        """ Split a room into 2 same-function rooms by a random x or y axis
        inside this room's x, y ranges. 

        """
        room = plan._pick_a_room()
        axis = random_pick(['x', 'y'])
        if not self.silent:
            print("Split room:", room.rid)

        # randomly pick a split line
        left  = room.stats["min_"+axis] + 0.5
        right = room.stats["max_"+axis] - 0.5
        if right - left == 0: 
            if not self.silent:
                print("This room has width 1 at axis %s" % axis)
            return
        split_line = random_pick(np.arange(left, right))

        # split the grids
        xys_1, xys_2 = [], []
        for xy in room.xys:
            if getattr(plan.grids[xy], axis) <= split_line: 
                xys_1.append(xy)
            else: 
                xys_2.append(xy)

        # create 2 new rooms based on split 2 groups of xys
        # append the new rooms to self.rooms and set original room to None
        room_1 = Room(function=room.function, xys=xys_1, rid=plan.room_count)
        room_2 = Room(function=room.function, xys=xys_2, rid=plan.room_count + 1)
        plan.rooms += [room_1, room_2]
        plan.rooms[room.rid] = None

        plan.room_count += 2

        # update the rids of split xys 
        for xy in xys_1: plan.grids[xy].rid = room_1.rid
        for xy in xys_2: plan.grids[xy].rid = room_2.rid

        if not self.silent:
            print("Into 2 rooms: %d and %d" % (room_1.rid, room_2.rid))


# ---------------------------- merge -----------------------------------------
    def merge(self, plan):
        """ Merge 2 same-function, adjacent rooms together.

        """
        # find all pairs of adjacent, same-function rooms keyed by function
        groups = self._group_rooms_by_function(plan)
        pairs  = {function:[] for function in plan.functions}
        for function in plan.functions:
            for rid in groups[function]:
                for adjacent_rid in plan.rooms[rid].find_adjacent_rids(plan.grids):
                    if adjacent_rid in groups[function]:
                        pairs[function].append((rid, adjacent_rid))

        # purge the function without adjacent pairs
        # if no function contains adjacent pairs, exit this action.
        pairs = purge_dict(pairs)
        if not pairs: 
            if not self.silent:
                print("No pairs of adjacent same-function rooms found.")
            return

        # randomly pick a function by weighting. (we may want to using weights
        # to control the chance of merge for different room function)
        # redo picking if the picked function has no adjacent pairs
        picked_function = ""
        while picked_function not in pairs.keys():
            picked_function = random_pick(plan.functions, p=plan.pr_merge)

        # randomly pick a pair of adjacent rooms
        # create a new room with same function and merged xys
        picked_pair = random_choice(pairs[picked_function])
        room_new    = Room(
            function=picked_function, 
            rid = plan.room_count,
            xys=plan.rooms[picked_pair[0]].xys + plan.rooms[picked_pair[1]].xys
        )
        plan.room_count += 1
        if not self.silent:
            print("Merge rooms %d and %d" % (plan.rooms[picked_pair[0]].rid,
                plan.rooms[picked_pair[1]].rid))

        # update self.rooms
        plan.rooms[picked_pair[0]] = None
        plan.rooms[picked_pair[1]] = None
        plan.rooms.append(room_new)
        if not self.silent:
            print("into room %d" % room_new.rid)

        # update the rid of merged xys
        for xy in room_new.xys:
            plan.grids[xy].rid = room_new.rid


    def _group_rooms_by_function(self, plan):
        """ Group the valid rooms(not None) by their functions. The result is 
        a dictionary.

        """
        rooms = plan._purge_room()
        groups = {function:[] for function in plan.functions}
        for room in rooms:
            groups[room.function].append(room.rid)
            
        return groups


# ---------------------------- move door -------------------------------------
    def _move_door(self,):
        """ Move the location of door on the boundary. 
        """

        pass


# ---------------------------- change wall -----------------------------------
    def _change_wall(self,):
        """ Change the wall type
        """
        
        pass



def main():
    pass


if __name__ == "__main__":
    main()