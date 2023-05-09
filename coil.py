import sympy as smp
import matplotlib.pyplot as plt
import numpy as np
import sympy as smp
from segment import Segment

class Coil:
    '''
    A class used to represent the simulated scanners

    ...

    Attributes
    ----------
    piecewise : boolean
        Toggle for type of function required to plot coil (e.g., True for rectangle, False for circle)
    coords : np.array
        Numpy array containing a matrix representing the x-, y-, and z-coordinates in the first, second, and third column respectively
    
    Methods
    -------
    '''
    def __init__(self):
        self.segments = [] # List of line segments
    
    def plot_coil(self, ax : plt.axes) -> bool:
        '''Generate a 3D plot of a coil on a passed pyplot axis

        Parameters
        ----------
        ax : plt.axes
            Pyplot axis upon which to plot
        
        Returns
        -------
        True
            If plotting is complete without problems
        '''

        for segment in self.segments:
            x_coords, y_coords, z_coords = segment.get_coords()
            ax.plot(x_coords, y_coords, z_coords, c='m')

        return True

    def add_segment(self, segment : Segment):
        '''
        INSERT DOCUMENTATION
        '''

        # Check that object passed is a segment
        if type(segment) != Segment:
            raise TypeError('Segment object not passed as argument. Ensure passed argument is a segment object')

        # Append segment to segments list, once type has been validated
        self.segments.append(segment)

        return True

        