#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
This script implements the visualization class to plot the intermediate or
final plan.

Author: Xian Lai
Date: Jan.23, 2017
"""


from matplotlib import pyplot as plt
import matplotlib as mpl
from descartes import PolygonPatch

from matplotlib import gridspec
from matplotlib.colors import ListedColormap, Normalize
from matplotlib import cm

# import seaborn as sns; sns.set()
# %matplotlib inline 
from pprint import pprint
import numpy as np
import json
import math

"""
# abbreviated names:
"a":"alpha", 
"c":"color", 
"lw":"linewidth", 
"ls":"linestyle",
"lc":"line_color"
"label":"label", 
"dashes":"on/off in pts",
"fillstyle":"fill marker",
"marker":"marker style",
"mec":"markeredgecolor",
"mew":"markeredgewidth", 
"mfc":"markerfacecolor", 
"ms":"markersize",}
"""
font = {
    'small' :{'fontsize' : 13, 'fontname' : 'Arial'},
    'median':{'fontsize' : 15, 'fontname' : 'Arial', 'fontweight' : 'bold'},
    'large' :{'fontsize' : 17, 'fontname' : 'Arial', 'fontweight' : 'bold'}
}
grey = {
    'white':'#ffffff', 'light':'#efefef', 'median':'#aaaaaa', 
    'dark':'#282828', 'black':'#000000'
}
DC   = {'blue':'#448afc', 'red':'#ed6a6a', 'green':'#80f442'}
DCM  = ListedColormap(DC.values())
CM   = cm.get_cmap('Spectral')


class _BasePlot():
    
    """ This is the private parent class that implements some attributes and 
    methods inherited by all its public children classes.
    """

    def __init__(self, background='light'):
        """ 
        """
        self.background = background

        # set up the background color of fig and axes
        plt.rcParams['axes.facecolor']   = grey[background]
        plt.rcParams['figure.facecolor'] = grey[background]

        # set interactive mode on so the plotting won't block process
        plt.ion()
        

    def _set_axParam(self, ax, show_grid=True):
        """ Set parameters of given ax
        """
        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
        ax.set_aspect('equal')
        
        # hide axis ticks
        ax.tick_params(
            axis="both", which="both", bottom="off", top="off", 
            labelbottom="on", left="off", right="off", labelleft="on", 
            colors=grey['median']
        )

        # remove axis spines
        ax.spines["top"].set_visible(False)  
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

        # show or hide the grid
        if show_grid: ax.grid(color=grey['median'], linewidth=2, alpha=0.3)
        else:         ax.grid(b=None)


    def _set_axTitle(self, ax, title):
        """ Set title of given ax
        """
        ax.set_title(title, **font['large'])


    def _plot_line(self, ax, x, y, c, lw):
        """ plot scatters of given x and y colored by corresponding labels z
        """
        ax.plot(x, y, '-', color=c, lw=lw)

        return ax


    def _plot_patch(self, ax, patch, color):
        """
        """
        ax.add_patch(PolygonPatch(patch, fc=color))

        return ax


    def _plot_label(self, ax, label, point):
        """
        """
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", lw=0, alpha=0.2)
        ax.text(point.x, point.y, label, fontdict=font['small'], bbox=bbox_props)

        return ax


    @staticmethod
    def show():
        plt.show()


    @staticmethod
    def ioff():
        plt.ioff()
        plt.show()
    


class SingleAxPlot(_BasePlot):
    
    """ This class is the public child class of _BasePlot class implementing
    the plotting figure with a single ax.
    """

    def __init__(self, xy_lims, figsize=(8,8), background='white', 
            show_grid=False):
        """ initialize the single plot object
        """
        _BasePlot.__init__(self, background=background)
        self.xlim, self.ylim = xy_lims
        self.fig, self.axes = self._plot_base(figsize, show_grid)

        if not show_grid: self.axes.grid(b=None)
        

    def _plot_base(self, figsize, show_grid):
        """ Create and set up the fig and ax
        """
        fig = plt.figure(figsize=figsize)
        ax  = fig.add_subplot(111)
        self._set_axParam(ax, show_grid=show_grid)

        return fig, ax


    def plot_lines(self, X, Y, title, c='k', lw=2, show=True):
        """ plot line if given vectors of x and y
        """
        for i in range(len(X)):
            self.axes = self._plot_line(self.axes, X[i], Y[i], c, lw)
        self._set_axTitle(self.axes, title)
        
        if show: plt.show()


    def plot_plan_intermediate(self, centers, functions, patches, colors, 
            title="intermediate plan", show=True):
        """ Plot the intermediate plan in process of searching.
        This intermediate plan only includes color patch and room function 
        label for each room.
        """
        self.axes.patches = []
        self.axes.texts   = []

        for patch, color in zip(patches, colors):
            self.axes = self._plot_patch(self.axes, patch, color)
        for function, center in zip(functions, centers):
            self.axes = self._plot_label(self.axes, function, center)
        
        plt.pause(2)



def main():
    pass

if __name__ == "__main__": main()
