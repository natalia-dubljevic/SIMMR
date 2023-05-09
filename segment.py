import sympy as smp
from lines import Straight, Curved
import numpy as np

class Segment():
    '''
    A class used to represent a line segment as a sympy function

    Parameters
    ----------
    type : str
        Line type (currently, only Straight and Curved are supported)
    low_lim : float
        The lower limit of the parameter for the calculation of the segment
    up_lim : float
        The upper limit of the parameter for the calculation of the segment
    '''

    def __init__(self, fn : Curved | Straight, low_lim : float, up_lim : float):
        '''
        INSERT DOCUMENTATION
        '''
        self.line_fn = self.set_fn(fn)
        self.low_lim = low_lim
        self.up_lim = up_lim

    def set_fn(self, fn : Curved | Straight):
        '''
        INSERT DOCUMENTATION
        '''

        if (type(fn) == Straight) | (type(fn) == Curved):
            return fn
        else:
            raise TypeError("Unsupported segment type passed")
        
    def get_coords(self):
        '''
        INSERT DOCUMENTATION
        '''
        t_range = np.linspace(self.low_lim, self.up_lim, 50)
        coords = [[], [], []]

        fn = smp.lambdify(self.line_fn.parameter, self.line_fn.fn, modules=['numpy'])

        for element in t_range:
            coords[0].extend(fn(element)[0])
            coords[1].extend(fn(element)[1])
            coords[2].extend(fn(element)[2])

        return coords[0], coords[1], coords[2]