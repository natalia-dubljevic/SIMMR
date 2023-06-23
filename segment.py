import sympy as smp
from lines import Straight, Curved
import numpy as np

class Segment():
    '''
    A class used to represent a line segment as a sympy function

    Parameters
    ----------
    line_fn : Curved | Straight
        Line function (currently, only Straight and Curved are supported)
    low_lim : float
        The lower limit of the parameter for the calculation of the segment; integration limit
    up_lim : float
        The upper limit of the parameter for the calculation of the segment; integration limit

    Methods
    -------
    set_fn(self, fn : Curved | Straight) -> Curved | Straight
        Validate and set line function
    get_coords(self) -> list, list, list
        Generate 3D coordinates of segment
    '''

    def __init__(self, fn : Curved | Straight, low_lim : float, up_lim : float):
        '''
        Parameters
        ----------
        fn : Curved | Straight
            Either a curved or straight line function
        low_lim : float
            Low parameter (i.e., 't') limit to plot the segment in 3D space
        up_lim : float
            Upper parameter (i.e., 't') limit to plot the segment in 3D space
        '''
        self.line_fn = self.set_fn(fn)
        self.low_lim = low_lim
        self.up_lim = up_lim

        from coil import Coil
        self.coil : Coil = None # Link to the 'parent' coil the segment is a part of

    def set_fn(self, fn : Curved | Straight) -> Curved | Straight:
        '''
        Validate that a supported line type has been passed and return if so

        Parameters
        ----------
        fn : Curved | Straight
            Line object intended as the line_fn for the segment object

        Returns
        -------
        Curved | Straight
            If line has been successfully validated
        TypeError
            Otherwise 
        '''

        if (type(fn) == Straight) | (type(fn) == Curved):
            return fn
        else:
            raise TypeError("Unsupported segment type passed")
        
    def get_coords(self):
        '''
        Get the x-, y-, and z-coordinates in 3D space of a segment object

        Returns
        -------
        list, list, list
            X-, y-, and z-coordinates of segment
        '''
        t_range = np.linspace(self.low_lim, self.up_lim, 50)
        coords = [[], [], []]

        fn = smp.lambdify(self.line_fn.parameter, self.line_fn.fn, modules=['numpy'])

        for element in t_range:
            coords[0].extend(fn(element)[0])
            coords[1].extend(fn(element)[1])
            coords[2].extend(fn(element)[2])

        return coords[0], coords[1], coords[2]