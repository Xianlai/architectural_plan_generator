#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the agent that generate architectural plans.
Here we instantialize a plan object either with grid coordiantes 
inside given boundary and randomly generate initial state or with a given 
initial state assigned by human designer. Then we instruct the agent to 
perform searching algorithm to find better plan state that satisfies a certain
objective score threshold.

Author: Xian Lai
Date: Feb.03, 2017
"""


from pprint import pprint
import pickle
from Transition import Transition
from Plan import Plan


def main():
    # read in functional requirements from a pickle file.
    with open('../data/function_params.pickle', 'rb') as handle:
        fn_params = pickle.load(handle)
    print("Functional requirements:")
    pprint(fn_params)

    """
    # init with boundary grids
    with open('../data/grid_coords.pickle', 'rb') as handle:
        grid_coords = pickle.load(handle)
    """

    # read in initial state from a pickle file. 
    with open('../data/initial_state.pickle', 'rb') as handle:
        init_state = pickle.load(handle)
    print("\nGiven initial plan state:")
    pprint(init_state)

    # init an architectural plan generator agent with initial state.
    plan = Plan(function_params=fn_params, grid_coords=None, 
        init_state=init_state, silent=False
    )
    plan.random_walk(iters=20)



if __name__ == "__main__":
    main()