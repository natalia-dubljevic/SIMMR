import sympy as smp
import matplotlib.pyplot as plt
import numpy as np
import sympy as smp
from segment import Segment
import sim_utils

import time

class Coil:
    '''
    A class used to represent the simulated scanners

    ...

    Attributes
    ----------
    segments : List[Segment]
        List of line segments that plot the coil
    scanner : Scanner
        The 'parent' scanner which the coil object is a part of
    
    Methods
    -------
    plot_coil(self, ax : plt.axes) -> bool
        Plots coil on passed axis; True if successful
    add_segment(self, segment : Segment) -> bool
        Adds segment that forms (a part of) the coil; True if successful
    B_volume(self) -> np.ndarray
        Calculate magnetic field at every point in bbox volume resulting from coil
    '''

    def __init__(self):
        '''
        Parameters
        ----------
        segments : list[Segment]
            List of line segments that plot the coil; defaults to an empty list
        '''
        self.segments = [] # List of line segments
        from scanner import Scanner
        self.scanner : Scanner = None # Link coil to its 'parent' scanner - for access to bbox, vol_res, etc.
    
    def plot_coil(self, ax : plt.axes) -> bool:
        '''
        Generate a 3D plot of a coil on a passed pyplot axis

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

    def add_segment(self, segment : Segment) -> bool:
        '''
        Validate and append a passed segment to the coil attribute segments

        Parameters
        ----------
        segment : Segment
            Segment object to add

        Returns
        -------
        TypeError
            If passed argument is not a segment
        True
            If segment successfully appended to segment list
        '''

        # Check that object passed is a segment
        if type(segment) != Segment:
            raise TypeError('Segment object not passed as argument. Ensure passed argument is a segment object')

        # Append segment to segments list, once type has been validated
        self.segments.append(segment)

        segment.coil = self

        return True # If addition of segment was successful / didn't throw any errors

    def B_volume(self) -> np.ndarray:
        ''' 
        Calculate the B field at every point in a volume resulting from a coil

        Given a variable l that represents the distance from the origin to a piece 
        of wire, integrate along that wire to find the B (magnetic) field at each
        point within a defined volume. The volume is bounded by a bbox and space
        is discretized based on the volume resolution.

        Returns
        -------
        np.ndarray
            4D volume of magnetic field components at each point in space. Last 
            dimension is size 3 representing x, y, and z components
        '''

        B_fields = []
        
        for segment in self.segments:

            fn = segment.line_fn.fn

            x, y, z = smp.symbols(['x', 'y', 'z'])
            r = smp.Matrix([x, y, z])
            sep = r - fn

            t = segment.line_fn.parameter
            
            # Define the integrand
            integrand = smp.diff(fn, t).cross(sep) / sep.norm()**3
            # Get the x, y, and z components of the integrand
            dBxdt = smp.lambdify([t, x, y, z], integrand[0])
            dBydt = smp.lambdify([t, x, y, z], integrand[1])
            dBzdt = smp.lambdify([t, x, y, z], integrand[2])

            # Add small tolerance to endpoint so it's included
            x_dim = np.arange(self.scanner.bbox[0], self.scanner.bbox[3] + 1e-10, self.scanner.vol_res[0])
            y_dim = np.arange(self.scanner.bbox[1], self.scanner.bbox[4] + 1e-10, self.scanner.vol_res[1])
            z_dim = np.arange(self.scanner.bbox[2], self.scanner.bbox[5] + 1e-10, self.scanner.vol_res[2])
            xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

            B_fields.append(sim_utils.B(segment.low_lim, segment.up_lim, dBxdt, dBydt, dBzdt, xv, yv, zv))

        return sum(B_fields)